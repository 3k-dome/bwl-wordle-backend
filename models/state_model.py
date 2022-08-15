from datetime import datetime

from . import db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now)
    json = db.Column(db.PickleType, unique=False, nullable=False)
    # relationships
    user = db.relationship("User", backref=db.backref("state", lazy=True))
