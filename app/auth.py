from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Succesvol ingelogd als {username}!', 'success')
            # 👑 Check of gebruiker admin is en stuur eventueel door
            if user.is_admin:
                return redirect(url_for('admin.admin'))
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Ongeldige gebruikersnaam of wachtwoord.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if username.lower() == 'admin':
            flash('Registreren met de naam "Admin" is niet toegestaan. Deze naam is gereserveerd.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Gebruikersnaam bestaat al.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_pw, is_admin=False)
        db.session.add(user)
        db.session.commit()

        flash('Registratie gelukt! Je kunt nu inloggen.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent uitgelogd.', 'info')
    return redirect(url_for('auth.login'))
