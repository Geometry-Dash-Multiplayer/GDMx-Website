import os
from flask import Flask, render_template, request, redirect, url_for, session
from models.users import db, User


from models.users import db as user_db

basedir = os.path.abspath(os.path.dirname(__file__))

# Create an instance of the Flask class
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'users.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    user_db.init_app(app)
    user_db.create_all()

# Define a route and a function to handle it
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/privacy')
def privacy():
    return render_template("Privacy.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Store user session data (you might want to use Flask-Login for session management)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
            return render_template("login.html", error=error)

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Create a new User instance and add it to the database
            new_user = User(siteUsername=username, email=email)
            # Store the hashed password securely (you would use proper password hashing here)
            new_user.password = password
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
    