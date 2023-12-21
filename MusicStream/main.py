import os

from flask import Flask , send_file
from io import BytesIO

from config.config import LocalDevelopmentConfig
from models.database import db
from routes.manager_routes import manager_routes
from routes.routes import routes
from routes.user_routes import user_routes
from routes.creator_routes import creator_routes
from models.models import Song


def create_app():
    app_create = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app_create.config.from_object(LocalDevelopmentConfig)
    db.init_app(app_create)
    app_create.app_context().push()
    return app_create


app = create_app()
app.register_blueprint(routes)
app.register_blueprint(manager_routes)
app.register_blueprint(user_routes)
app.register_blueprint(creator_routes)


@app.route('/play_audio/<int:song_id>', methods=['GET', 'POST'])
def play_audio(song_id):
    song = Song.query.get(song_id)
    audio_data = song.audio
    print(f"Audio data length: {len(audio_data)} bytes")
    audio_stream = BytesIO(audio_data)
    return send_file(audio_stream, mimetype='audio/mp3')

if __name__ == '__main__':
    # Run the Flask app
    app.run()
