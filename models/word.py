from database import SerializableModelBase, db


class Word(SerializableModelBase, db.Model):
    text = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    used = db.Column(db.Boolean(), nullable=False)
