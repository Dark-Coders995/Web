import os

from flask import Flask

from config.config import LocalDevelopmentConfig
from models.database import db
from routes.manager_routes import manager_routes
from routes.routes import routes
from routes.user_routes import user_routes


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

if __name__ == '__main__':
    # Run the Flask app
    app.run()
