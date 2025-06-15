from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
import os
from werkzeug.utils import secure_filename
from .models import Document, db

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/documents', methods=['GET', 'POST'])
@login_required
def documents():
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)  # Zorg dat de uploadmap bestaat

    if request.method == 'POST':
        file = request.files.get('document')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            if os.path.exists(filepath):
                flash(f'⚠️ Document {filename} bestaat al.', 'warning')
            else:
                try:
                    file.save(filepath)
                    doc = Document(filename=filename)
                    db.session.add(doc)
                    db.session.commit()
                    flash(f'✅ Document {filename} succesvol geüpload!', 'success')
                except Exception as e:
                    flash(f'❌ Fout bij uploaden: {str(e)}', 'danger')
        else:
            flash('⚠️ Geen bestand geselecteerd.', 'warning')

    docs = Document.query.all()
    return render_template('documents.html', documents=[doc.filename for doc in docs])

@documents_bp.route('/documents/delete/<filename>')
@login_required
def delete_document(filename):
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    filepath = os.path.join(upload_folder, filename)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            flash(f'🗑️ Document {filename} verwijderd van server.', 'info')
        else:
            flash(f'⚠️ Document {filename} niet gevonden op server.', 'warning')

        doc = Document.query.filter_by(filename=filename).first()
        if doc:
            db.session.delete(doc)
            db.session.commit()
            flash(f'✅ Databasevermelding van {filename} verwijderd.', 'success')
        else:
            flash(f'⚠️ Document {filename} stond niet in database.', 'warning')

    except Exception as e:
        flash(f'❌ Fout bij verwijderen: {str(e)}', 'danger')

    return redirect(url_for('documents.documents'))
