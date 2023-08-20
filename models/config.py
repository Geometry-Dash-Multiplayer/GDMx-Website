import os

class Configuration:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "b'\xab\x06d\x87\x87\xc2\x0b\x13\x9aB\x9b\x9bW\x98\x91\x88\x0e1\x80\xb3\x02\xd5\x02Z'"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gdmultiplayerx.raa@gmail.com'
    MAIL_PASSWORD = "vjaxdtyvpyaixljz"
    MAIL_DEFAULT_SENDER = 'gdmultiplayerx.raa@gmail.com'
