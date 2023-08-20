from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
oauth = OAuth()
