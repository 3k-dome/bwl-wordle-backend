from flask import Blueprint
from models.user import User
from database import db


test_blueprint = Blueprint("Test", __name__, url_prefix="/test")

@test_blueprint.route("/")
def add_user():
    user = User(username="Test1", password="1234")
    db.session.add(user)
    db.session.commit()