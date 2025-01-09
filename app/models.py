from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'gallery_user'
    id = db.Column('UserID', db.Integer, primary_key=True)
    username = db.Column('Username', db.String(255), unique=True, nullable=False)
    password = db.Column('Password', db.String(255), nullable=False)
    email = db.Column('Email', db.String(255), unique=True, nullable=False)
    full_name = db.Column('NamaLengkap', db.String(255), nullable=False)
    address = db.Column('Alamat', db.Text)

    # Relationships
    albums = db.relationship('Album', backref='user', lazy=True)
    photos = db.relationship('Photo', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


class Album(db.Model):
    __tablename__ = 'gallery_album'
    id = db.Column('AlbumID', db.Integer, primary_key=True)
    name = db.Column('NamaAlbum', db.String(255), nullable=False)
    description = db.Column('Deskripsi', db.Text)
    created_date = db.Column('TanggalDibuat', db.Date, default=datetime.utcnow)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('gallery_user.UserID'), nullable=False)

    # Relationship
    photos = db.relationship('Photo', backref='album', lazy=True)


class Photo(db.Model):
    __tablename__ = 'gallery_foto'
    id = db.Column('FotoID', db.Integer, primary_key=True)
    title = db.Column('JudulFoto', db.String(255), nullable=False)
    description = db.Column('DeskripsiFoto', db.Text)
    upload_date = db.Column('TanggalUnggah', db.Date, default=datetime.utcnow)
    file_path = db.Column('LokasiFile', db.String(255), nullable=False)
    album_id = db.Column('AlbumID', db.Integer, db.ForeignKey('gallery_album.AlbumID'))
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('gallery_user.UserID'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='photo', lazy=True)
    likes = db.relationship('Like', backref='photo', lazy=True)


class Comment(db.Model):
    __tablename__ = 'gallery_komentarfoto'
    id = db.Column('KomentarID', db.Integer, primary_key=True)
    content = db.Column('IsiKomentar', db.Text, nullable=False)
    comment_date = db.Column('TanggalKomentar', db.Date, default=datetime.utcnow)
    photo_id = db.Column('FotoID', db.Integer, db.ForeignKey('gallery_foto.FotoID'), nullable=False)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('gallery_user.UserID'), nullable=False)


class Like(db.Model):
    __tablename__ = 'gallery_likefoto'
    id = db.Column('LikeID', db.Integer, primary_key=True)
    like_date = db.Column('TanggalLike', db.Date, default=datetime.utcnow)
    photo_id = db.Column('FotoID', db.Integer, db.ForeignKey('gallery_foto.FotoID'), nullable=False)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('gallery_user.UserID'), nullable=False)