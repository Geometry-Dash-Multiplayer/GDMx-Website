from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_oauthlib.client import OAuth
import os

app = Flask(__name__)

# Configuration for SQLAlchemy and database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "b'\xab\x06d\x87\x87\xc2\x0b\x13\x9aB\x9b\x9bW\x98\x91\x88\x0e1\x80\xb3\x02\xd5\x02Z'"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'gdmultiplayerx.raa@gmail.com'
app.config['MAIL_PASSWORD'] = "vjaxdtyvpyaixljz"
app.config['MAIL_DEFAULT_SENDER'] = 'gdmultiplayerx.raa@gmail.com'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
oauth = OAuth(app)
