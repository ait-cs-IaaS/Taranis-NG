from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from publishers.managers import api_manager, publishers_manager, auth_manager


def create_app():
    app = Flask(__name__)
    load_dotenv()

    with app.app_context():
        CORS(app)

        auth_manager.initialize(app)
        api_manager.initialize(app)
        publishers_manager.initialize()
    return app


app = create_app()
