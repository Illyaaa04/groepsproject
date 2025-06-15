import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

DB_PATH = os.path.join(app.instance_path, 'app.db')

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)

    if os.path.exists(DB_PATH):
        try:
            db.session.remove()
            db.engine.dispose()
            os.remove(DB_PATH)
            print(f"📂 Database '{DB_PATH}' verwijderd.")
        except Exception as e:
            print(f"❌ Fout bij verwijderen database: {e}")
    else:
        print(f"📂 Database '{DB_PATH}' bestaat nog niet, wordt aangemaakt.")

    # Maak de database aan
    db.create_all()
    print("✅ Nieuwe database en tabellen aangemaakt.")

    # Voeg de admin gebruiker toe (via db.session.query)
    username = 'Admin'
    password = 'AdminIllya'
    existing_user = db.session.query(User).filter_by(username=username).first()
    if not existing_user:
        hashed_pw = generate_password_hash(password)
        new_admin = User(username=username, password=hashed_pw, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        print(f"👤 Admin gebruiker '{username}' is aangemaakt met wachtwoord '{password}'.")
    else:
        print(f"ℹ️ Admin gebruiker '{username}' bestaat al.")
