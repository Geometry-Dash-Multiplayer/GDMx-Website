import os
from flask import Flask, render_template, request, redirect, url_for, session
from models.users import db, User

# Create an instance of the Flask class
app = Flask(__name__)

# Configuration for SQLAlchemy and database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app context and create tables
with app.app_context():
    db.init_app(app)
    db.create_all()

# Define a route to display the index page
@app.route('/')
def index():
    return render_template("index.html")

# Define a route to display the privacy page
@app.route('/privacy')
def privacy():
    return render_template("Privacy.html")

# Define a route for user login, supporting both GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Use the check_password method
            # Store user session data (might want to use Flask-Login for session management later)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
            return render_template("login.html", error=error)

    return render_template("login.html")

# Define a route for user registration, supporting both GET and POST methods
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
