from models.app import app, db
import json
import routes

# Initialize SQLAlchemy with the app context and create tables
with app.app_context():
    db.create_all()

with open('data/emojis.json', 'r', encoding='utf-8') as file:
    emoji_data = json.load(file)

EMOJI_MAP = {}
for category, emojis in emoji_data.items():
    for emoji_info in emojis:
        key = emoji_info["description"].lower().replace(" ", "_")
        EMOJI_MAP[key] = emoji_info["emoji"]

if __name__ == '__main__':
    print(app.template_folder)
    app.run(debug=True)

