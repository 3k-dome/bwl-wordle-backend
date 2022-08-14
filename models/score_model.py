from datetime import datetime

from . import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey("difficulty.id"), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now)
    score = db.Column(db.Integer, unique=False, nullable=False)
    won = db.Column(db.Boolean, unique=False, nullable=False)
    taken_tries = db.Column(db.Integer, unique=False, nullable=False)
    hit_rate = db.Column(db.Float, unique=False, nullable=False)
    # relationships
    user = db.relationship("User", backref=db.backref("scores", lazy=True))
    difficulty = db.relationship("Difficulty", backref=db.backref("scores", lazy=True))
