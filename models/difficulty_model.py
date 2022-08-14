from . import db


class Difficulty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    tries = db.Column(db.Integer, unique=True, nullable=False)
