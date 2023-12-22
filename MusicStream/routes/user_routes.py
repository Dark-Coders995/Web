from flask import Blueprint, request, render_template, redirect, session, url_for , flash

from models.database import db
from models.models import Song,  User , Playlist

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/add_to_playlist/<int:song_id>', methods=['GET', 'POST'])
def add_to_playlist(song_id):
    user_id = session['user_id']
    existing_entry = Playlist.query.filter_by(user_id=user_id, song_id=song_id).first()

    if existing_entry:
        flash('Song is already in the playlist.')
    else:
        playlist_item = Playlist(user_id=user_id, song_id=song_id)
        db.session.add(playlist_item)
        db.session.commit()
        flash('Song added to the playlist successfully.')

    return redirect(url_for('routes.logged_in'))

@user_routes.route('/playlist', methods=['GET', 'POST'])
def playlist():
    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'remove':
            playlist_item_id = request.form.get('playlist_item_id')
            if playlist_item_id:
                playlist_item_id = int(playlist_item_id)
                playlist_item = Playlist.query.get(playlist_item_id)
                db.session.delete(playlist_item)
                db.session.commit()
        return redirect(url_for('user_routes.playlist'))

    playlist_items = Playlist.query.filter_by(user_id=user_id).all()

    return render_template('user/playlist.html', user=user, playlist_items=playlist_items)