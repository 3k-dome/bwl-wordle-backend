from datetime import datetime
from typing import Any, Dict

from flask import Flask
from models import State, User

from services.resettable_base import ResettableBase, depends_on_reset


class StateService(ResettableBase):
    def __init__(self, app: Flask, daily: bool, interval: int) -> None:
        super().__init__(daily, interval)
        self.app = app
        self.reset()

    def reset(self) -> None:
        # if an update happened all saves are invalid so we can just drop them
        self.updated = datetime.now()
        with self.app.app_context():
            State.query.delete()
            self.app.db.session.commit()

    @depends_on_reset
    def save_state(self, username: str, json: Any = None) -> None:
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            old = State.query.filter_by(user_id=user.id).first()
            if old:
                old.json = json
            else:
                self.app.db.session.add(State(user_id=user.id, json=json))
            self.app.db.session.commit()

    @depends_on_reset
    def load_state(self, username: str) -> Dict | None:
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            if user.state:
                return user.state[0].json
            return None
