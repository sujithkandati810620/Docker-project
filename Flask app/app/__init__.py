from flask import Flask
from flask_cors import CORS
from .db.postgresql import pg_conn, pg_cursor
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(main_bp)

    return app
