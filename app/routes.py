from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Je moet ingelogd zijn om het dashboard te bekijken.', 'warning')
        return redirect(url_for('auth.login'))

    return render_template('dashboard.html', user=current_user)
