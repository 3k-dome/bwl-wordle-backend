from pathlib import Path

from flask import Flask

# the magic to associate our 'db' object with all our needed models happens
# in 'models.__init__.py', this means 'db.create_all()' already knows about them
from models import db


def create_app_with_db() -> Flask:
    """Sets up our database and binds it to the flask app."""
    app = Flask(__name__)
    filepath = Path(__file__).parent / "database" / "wordle.db"
    filepath.parent.mkdir(exist_ok=True)
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        db.create_all()
        app.db = db
    return app


# create app and bind database
app = create_app_with_db()
app.run(host="0.0.0.0", port=8000)
