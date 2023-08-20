from extensions import app, db, bcrypt, mail, oauth
from models.config import Configuration

app.config.from_object(Configuration)

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
oauth.init_app(app)
