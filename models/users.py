from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, app, bcrypt


class User(db.Model):
    # General Website details
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(512), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)  # Rename to password_hash
    gameUsername = db.Column(db.String(512), unique=False, nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())

    # Robtop IDs
    playerId = db.Column(db.Integer, unique=True, nullable=True)
    accountId = db.Column(db.Integer, unique=True, nullable=True)

    # Patreon sub Tier
    patreon_tier = db.Column(db.Integer, unique=False, nullable=False)

    # Settings
    port = db.Column(db.String, unique=False, nullable=False)
    serverIp = db.Column(db.String, unique=False, nullable=False)
    renderCustomIcons = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

        # Defaults

        self.port = "7777"
        self.serverIp = "176.106.224.146"
        self.renderCustomIcons = False
        self.playerId = None
        self.accountId = None
        self.patreon_tier = 0
        self.gameUsername = ""

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expires_sec=900):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"<User {self.siteUsername}>"
