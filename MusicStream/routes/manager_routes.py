from flask import Blueprint, redirect
from flask import render_template, request

from models.database import db
from models.models import Album, Song
manager_routes = Blueprint('manager_routes', __name__)


@manager_routes.route('/add_album', methods=['GET', 'POST'])
def add_album():
    if request.method == 'POST':
        album_name = request.form["album_name"]
        if album_name is None:
            return "Enter valid album"
        try:
            album = Album(album_name=album_name)
            db.session.add(album)
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Please try again later."
    return render_template('manager/add_album.html')


@manager_routes.route('/delete_album/<int:album_id>', methods=['POST'])
def delete_album(album_id):
    try:
        album = Album.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()
        else:
            return "Album not found."
    except Exception as e:
        print(e)
        return "Error occurred while deleting the album. Please try again later."
    return redirect('/manager_logged')


@manager_routes.route('/update_album/<int:album_id>', methods=['GET', 'POST'])
def update_album(album_id):
    album = Album.query.get(album_id)
    if not album:
        return "Album not found."

    if request.method == 'POST':
        new_album_name = request.form["new_album_name"]
        if not new_album_name:
            return "Enter a valid album name."

        try:
            album.album_name = new_album_name
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Error occurred while updating the album. Please try again later."

    return render_template('manager/update_album.html', album_id=album_id)


@manager_routes.route('/add_song/<int:album_id>', methods=['GET', 'POST'])
def add_song(album_id):
    album = Album.query.get(album_id)
    if not album:
        return "Album not found."

    if request.method == 'POST':
        song_name = request.form.get('song_name')
        lyrics = request.form.get('lyrics')
        artist = request.form.get('artist')
        audio_file = request.files.get('audio_file')
        if audio_file:
            audio_file = audio_file.read()

            if not all([song_name, lyrics, artist, audio_file]):
                return "Please fill in all the song details."

            try:
                song = Song(song_name=song_name, lyrics = lyrics, artist = artist, audio = audio_file , album_id=album_id)
                db.session.add(song)
                db.session.commit()
                return redirect('/manager_logged')
            except Exception as e:
                print(e)
                return "Error occurred while adding the song. Please try again later."

    return render_template('manager/add_song.html', album=album )


@manager_routes.route('/update_song/<int:song_id>', methods=['GET', 'POST'])
def update_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return "Song not found."

    if request.method == 'POST':
        song_name = request.form.get('song_name')
        lyrics = request.form.get('lyrics')
        artist = request.form.get('artist')
        audio_file = request.files.get('audio_file')
        if audio_file:
            audio_file = audio_file.read()

        if not all([song_name, lyrics , artist , audio_file]):
            return "Please fill in all the song details."

        try:
            song.song_name = song_name
            song.lyrics = lyrics
            song.artist = artist
            song.audio = audio_file
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Error occurred while updating the song. Please try again later."

    return render_template('manager/update_song.html', song=song)


@manager_routes.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    try:
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
        else:
            return "Song not found."
    except Exception as e:
        print(e)
        return "Error occurred while deleting the song. Please try again later."
    return redirect('/manager_logged')


# forms.py

