import os, requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
from models.users import db, User
from data.patreon import *
from flask_oauthlib.client import OAuth
from app import app, oauth, db, mail

# Initialize SQLAlchemy with the app context and create tables
with app.app_context():
    db.create_all()

patreon = oauth.remote_app(
    'patreon',
    consumer_key='tWe8WLdrzldJNM1W2wwQO47x6w3V-jXKWHxqoKpAEQYkstEXQHJndxUN01qvSw2n',
    consumer_secret='nddXb3R832dFtzEo62RBwRX6BIXK86NpeE5dXGrbbTAsUPCEvZYy5A3E8yz8BKSa',
    request_token_params={
        'scope': 'users pledges-to-me my-campaign',  # Adjust scopes as needed
    },
    base_url='https://www.patreon.com/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.patreon.com/api/oauth2/token',
    authorize_url='https://www.patreon.com/oauth2/authorize',
)


# Define a route to display the index page
@app.route('/')
def index():
    return render_template("index.html")


@app.context_processor
def inject_user():
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.get(user_id)
        return {"current_user": user}
    return {"current_user": None}


# Define a route to display the privacy page
@app.route('/privacy')
def privacy():
    return render_template("Privacy.html")

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    return render_template("profile.html", user=user,
                        client_id = PATREON_CLIENT_ID,
                        redirect_uri = PATREON_REDIRECT_URI)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))

    gd_username = request.form.get('gd_username')
    email = request.form.get('email')
    password = request.form.get('password')

    if gd_username:
        user.gameUsername = gd_username
    if email:
        user.email = email
    if password:
        user.set_password(password)

    db.session.commit()
    return redirect(url_for('profile'))


@app.route('/connect_patreon')
def connect_patreon():
    code = request.args.get("code")
    # Prepare the payload for token exchange

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": PATREON_CLIENT_ID,
        "client_secret": PATREON_CLIENT_SECRET,
        "redirect_uri": PATREON_REDIRECT_URI
    }    # Set the headers for the POST request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the POST request to exchange code for tokens
    response = requests.post("https://www.patreon.com/api/oauth2/token", data=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        # You can store the tokens on your server for the user

        # TODO send user to their profile
        return jsonify(token_data)  # Return token data as JSON response
    else:
        # TODO add error page
        return "Token exchange failed", response.status_code


@app.route('/login/patreon/authorized')
def patreon_authorized():
    response = patreon.authorized_response()
    if response is None or response.get('access_token') is None:
        return "Access denied: reason={} error={}".format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['patreon_token'] = (response['access_token'], '')

    # Fetch Patreon user details
    patreon_user = patreon.get('current_user', token=session['patreon_token']).data

    # Extract user's Patreon subscription tier from the response (this might be different based on the actual response format from Patreon)
    tier = patreon_user.get('tier', 0)

    # Update user's Patreon tier in the database
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            user.patreon_tier = tier
            db.session.commit()

    return redirect(url_for('profile'))


# Define a route for user login, supporting both GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Use the check_password method
            # Store user session data (might want to use Flask-Login for session management later)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate and send the password reset email
            token = user.generate_reset_token()
            reset_link = url_for('reset_password', token=token, _external=True)

            subject = 'Password Reset Request'
            body = f"""
            To reset your password, visit the following link: {reset_link}
            If you did not make this request then simply ignore this email and no changes will be made.
            """
            msg = Message(subject, recipients=[user.email], body=body)
            mail.send(msg)

            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('login'))
        else:
            flash('That email does not exist.', 'warning')
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from the session
    return redirect(url_for('index'))


# Define a route for user registration, supporting both GET and POST methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user_by_username = User.query.filter_by(username=username).first()
        existing_user_by_email = User.query.filter_by(email=email).first()

        if existing_user_by_username:
            error = "Username already exists. Please choose another."
            return render_template("register.html", error=error)

        if existing_user_by_email:
            error = "Email already registered. Please use another or login."
            return render_template("register.html", error=error)

        if password == confirm_password:
            # Create a new User instance and add it to the database
            new_user = User(username=username, email=email)
            # Store the hashed password securely using the set_password method
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Redirect to log in after successful registration
        else:
            error = "Passwords do not match"
            return render_template("register.html", error=error)

    return render_template("register.html")



# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
