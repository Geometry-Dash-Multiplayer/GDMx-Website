import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.users import db as user_db

basedir = os.path.abspath(os.path.dirname(__file__))

# Create an instance of the Flask class
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define a route and a function to handle it
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/privacy')
def privacy():
    return render_template("Privacy.html")


# Run the app if this script is executed directly
if __name__ == '__main__':
    user_db.init_app(app)
    app.run(debug=True, host="0.0.0.0")
    