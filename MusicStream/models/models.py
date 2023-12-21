from .database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    is_active = db.Column(db.Boolean())
   # carts = db.relationship('Cart', backref='user', lazy=True)
    creator = db.relationship('Creator', backref='user', lazy=True , uselist=False)
    playlist = db.relationship('Playlist', backref='user', lazy=True)

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    album_name = db.Column(db.String(150))
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'), nullable=False)
    songs = db.relationship('Song', backref='album', lazy=True, cascade='all, delete-orphan')

class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    song_name = db.Column(db.String(150))
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id', ondelete='CASCADE'), nullable=False)
    lyrics = db.Column(db.String(150))
    artist = db.Column(db.String(150))
    audio = db.Column(db.LargeBinary)

'''
class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='carts', lazy=True)'''

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'))
    songs = db.relationship('Song', backref='playlists', lazy=True)

class Creator(db.Model):
    creator_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    creator_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, unique=True)
    album = db.relationship('Album', backref='creator', lazy=True, cascade='all, delete-orphan')



