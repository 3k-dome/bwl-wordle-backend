from enum import Enum, auto
from hashlib import sha256
from typing import Tuple

from flask import Flask
from models import User


class Status(Enum):
    Empty = auto()
    Error = auto()
    Ok = auto()


class UserService:
    """Service to manage user accounts."""

    def __init__(self, app: Flask) -> None:
        self.app = app

    @staticmethod
    def encrypt(message: str) -> str:
        """Encrypts a string with sha256."""
        encryption = sha256()
        encryption.update(message.encode("utf_8"))
        return encryption.hexdigest()

    def add_user(self, username: str = None, password: str = None, **kwargs) -> Tuple[bool, Status]:
        """Adds a user to the db if no user with this name already exist."""
        if not username or not password:
            return False, Status.Empty
        if User.query.filter_by(username=username).first():
            return False, Status.Error
        with self.app.app_context():
            self.app.db.session.add(User(username=username, password=UserService.encrypt(password)))
            self.app.db.session.commit()
            return True, Status.Ok

    def get_user(self, username: str = None, password: str = None, **kwargs) -> Tuple[bool, Status]:
        """Checks wether a user exists, login method."""
        if not username or not password:
            return False, Status.Empty
        if User.query.filter_by(username=username).filter_by(password=UserService.encrypt(password)).first():
            return True, Status.Ok
        return False, Status.Error

    def del_user(self, username: str = None, password: str = None, **kwargs) -> Tuple[bool, Status]:
        """Deletes a user if it exists."""
        if not username or not password:
            return False, Status.Empty
        user = User.query.filter_by(username=username).filter_by(password=password).first()
        if not user:
            return False, Status.Error
        with self.app.app_context():
            self.app.db.session.delete(user)
            self.app.db.session.commit()
            return True, Status.Ok
