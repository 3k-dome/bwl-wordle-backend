from flask import Flask, jsonify
from pathlib import Path

# import our db context and associate all models,
# this is necessary because the models rely on 'db'
from database import db
from models import *


def bind_database() -> None:
    """Sets up our database and binds it to the flask app."""
    filepath = Path(__file__).parent / "database" / "wordle.db"
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        db.create_all()

# create app and database
app = Flask(__name__)
bind_database()

from blueprints import *

app.register_blueprint(test_blueprint)

app.run(host="0.0.0.0", port=8000)
