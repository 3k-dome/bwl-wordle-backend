from pathlib import Path

from flask import Flask

# the magic to associate our 'db' object with all our needed models happens
# in 'models.__init__.py', this means 'db.create_all()' already knows about them
from blueprints import create_blueprints
from models import db
from util import load_settings_file, setup_difficulties

SETTINGS = load_settings_file(Path(__file__).parent / "settings.json")


def create_app_with_db() -> Flask:
    """Sets up our database and binds it to the flask app."""
    app = Flask(__name__)
    filepath = Path(__file__).parent / "database" / "wordle.sqlite"
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

# setup our basic entries if those are empty
setup_difficulties(app, SETTINGS["difficulties"])

# register all blueprints
[
    app.register_blueprint(blueprint)
    for blueprint in create_blueprints(app, daily=SETTINGS["daily"], interval=SETTINGS["interval"])
]

# start app
app.run(host=SETTINGS["host"], port=SETTINGS["port"])
