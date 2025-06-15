import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

try:
    with app.app_context():
        # Gebruik een absoluut pad dat altijd werkt (beter dan instance_path op Render)
        db_path = os.path.abspath("app.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Verwijder de bestaande database (optioneel)
        if os.path.exists(db_path):
            db.session.remove()
            db.engine.dispose()
            os.remove(db_path)
            print(f"Database '{db_path}' verwijderd.")
        else:
            print(f"Database '{db_path}' bestond nog niet, wordt nu aangemaakt.")

        # Maak de nieuwe database aan
        db.create_all()
        print("Nieuwe database en tabellen aangemaakt.")

        # Voeg admin gebruiker toe
        username = 'Admin'
        password = 'AdminIllya'
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
            new_admin = User(username=username, password=hashed_pw, is_admin=True)
            db.session.add(new_admin)
            db.session.commit()
            print(f"Admin '{username}' aangemaakt met wachtwoord '{password}'.")
        else:
            print(f"ℹ Admin '{username}' bestaat al.")

except Exception as e:
    print(f"❌ Fout tijdens reset_and_create_admin.py: {e}")
    exit(1)
