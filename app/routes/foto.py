from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Photo, Album, db
import os
from werkzeug.utils import secure_filename

foto_bp = Blueprint('foto_bp', __name__)

@foto_bp.route('/photos')
@login_required
def photos():
    user_photos = Photo.query.filter_by(user_id=current_user.id).all()
    return render_template('photos.html', photos=user_photos)

@foto_bp.route('/photos/new', methods=['GET', 'POST'])
@login_required
def upload_photo():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            title = request.form.get('title')
            description = request.form.get('description')
            album_id = request.form.get('album_id')
            
            new_photo = Photo(title=title, description=description, file_path=file_path, album_id=album_id, user_id=current_user.id)
            db.session.add(new_photo)
            db.session.commit()
            flash('Photo uploaded successfully!', 'success')
            return redirect(url_for('foto_bp.photos'))

    albums = Album.query.filter_by(user_id=current_user.id).all()
    return render_template('upload_photo.html', albums=albums)

@foto_bp.route('/photos/<int:photo_id>')
@login_required
def photo_detail(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('You do not have permission to view this photo', 'danger')
        return redirect(url_for('foto_bp.photos'))
    return render_template('photo_detail.html', photo=photo)

@foto_bp.route('/photos/<int:photo_id>', methods=['PUT'])
@login_required
def update_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('You do not have permission to update this photo', 'danger')
        return redirect(url_for('foto_bp.photos'))
    
    photo.title = request.form.get('title')
    photo.description = request.form.get('description')
    db.session.commit()
    flash('Photo updated successfully!', 'success')
    return redirect(url_for('foto_bp.photo_detail', photo_id=photo.id))

@foto_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.user_id != current_user.id:
        flash('You do not have permission to delete this photo', 'danger')
        return redirect(url_for('foto_bp.photos'))
    
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted successfully!', 'success')
    return redirect(url_for('foto_bp.photos'))