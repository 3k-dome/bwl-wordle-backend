from typing import Dict, List
from flask import Flask
from models import Difficulty


def setup_difficulties(app: Flask, difficulties: List[Dict[str, str | int]]) -> None:
    if not app.db:
        raise Exception(
            "Database context needs to be set on the given app as 'app.db' see 'app.db = db' with 'db = SQLAlchemy()'."
        )
    # setup our basic difficulties if the table is empty
    with app.app_context():
        if not Difficulty.query.all():
            for difficulty in difficulties:
                app.db.session.add(Difficulty(**difficulty))
            app.db.session.commit()
