from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

# Initialisaties
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Zorg dat instance-map bestaat
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuratie
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://projectgebruiker:Antonadik23@localhost/groepsproject'
    )
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    # Initialiseer extensies
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

        # Voeg admin toe als hij nog niet bestaat
        if not User.query.filter_by(username='AdminIllya').first():
            hashed_pw = generate_password_hash('Illyaaa23', method='pbkdf2:sha256')
            admin = User(username='AdminIllya', password=hashed_pw, is_admin=True)
            db.session.add(admin)
            db.session.commit()
            print("✅ AdminIllya toegevoegd (wachtwoord: Illyaaa23)")

    # Registreer Blueprints
    from .auth import auth_bp
    from .routes import main_bp
    from .admin import admin_bp
    from .documents import documents_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(documents_bp)

    return app
