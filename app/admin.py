from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from .models import User, Log, Document, db
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Geen toegang tot het adminpaneel.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('admin.html')

@admin_bp.route('/admin/logs')
@login_required
def logs():
    if not current_user.is_admin:
        flash('Geen toegang.', 'danger')
        return redirect(url_for('main.dashboard'))
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)

@admin_bp.route('/admin/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('Geen toegang.', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('users.html', users=users)

@admin_bp.route('/admin/make_admin/<int:user_id>')
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash('Geen toegang.', 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        flash(f'{user.username} is nu admin.', 'success')
    else:
        flash('Gebruiker niet gevonden.', 'danger')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Geen toegang.', 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'Gebruiker {user.username} verwijderd.', 'success')
    else:
        flash('Gebruiker niet gevonden.', 'danger')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/documents')
@login_required
def admin_documents():
    if not current_user.is_admin:
        flash('Geen toegang.', 'danger')
        return redirect(url_for('main.dashboard'))
    documents = Document.query.all()
    return render_template('admin_documents.html', documents=documents)

@admin_bp.route('/admin/reset')
@login_required
def reset_database():
    if not current_user.is_admin:
        flash('Geen toegang tot resetfunctie.', 'danger')
        return redirect(url_for('main.dashboard'))

    db_path = os.path.join(current_app.instance_path, 'app.db')

    try:
        db.session.remove()
        db.engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)
            flash('Database verwijderd.', 'info')

        db.create_all()

        username = 'Admin'
        password = 'AdminIllya'
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_admin = User(username=username, password=hashed_pw, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()

        flash('Database gereset en nieuwe admin aangemaakt.', 'success')
    except Exception as e:
        flash(f'Fout bij resetten: {e}', 'danger')

    return redirect(url_for('admin.admin'))
