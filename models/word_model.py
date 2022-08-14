from email.policy import default
from . import db


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    used = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=None)
