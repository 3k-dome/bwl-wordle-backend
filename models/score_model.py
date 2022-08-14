from . import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey("difficulty.id"), unique=False, nullable=False)
    score = db.Column(db.Float, unique=False, nullable=False)
    # relationships
    user = db.relationship("User", backref=db.backref("scores", lazy=True))
    difficulty = db.relationship("Difficulty", backref=db.backref("scores", lazy=True))
