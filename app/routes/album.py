from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Album, db

album_bp = Blueprint('album_bp', __name__)

@album_bp.route('/albums')
@login_required
def albums():
    user_albums = Album.query.filter_by(user_id=current_user.id).all()
    return render_template('albums.html', albums=user_albums)

@album_bp.route('/album/new', methods=['GET', 'POST'])
@login_required
def new_album():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        new_album = Album(name=name, description=description, user_id=current_user.id)
        db.session.add(new_album)
        db.session.commit()
        flash('Album created successfully!', 'success')
        return redirect(url_for('album_bp.albums'))

    return render_template('new_album.html')

@album_bp.route('/album/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('You do not have permission to edit this album', 'danger')
        return redirect(url_for('album_bp.albums'))

    if request.method == 'POST':
        album.name = request.form.get('name')
        album.description = request.form.get('description')
        db.session.commit()
        flash('Album updated successfully!', 'success')
        return redirect(url_for('album_bp.albums'))

    return render_template('edit_album.html', album=album)

@album_bp.route('/album/<int:album_id>/delete', methods=['POST'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        flash('You do not have permission to delete this album', 'danger')
        return redirect(url_for('album_bp.albums'))

    db.session.delete(album)
    db.session.commit()
    flash('Album deleted successfully!', 'success')
    return redirect(url_for('album_bp.albums'))