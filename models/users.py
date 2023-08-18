from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    siteUsername = db.Column(db.String(512), unique=True, nullable=False)
    gameUsername = db.Column(db.String(512), unique=False, nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    # Robtop IDs
    playerId = db.Column(db.BigInteger, unique=True, nullable=False)
    accountId = db.Column(db.BigInteger, unique=True, nullable=False)

    tier = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"