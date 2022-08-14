from typing import Tuple

from flask import Blueprint, Flask

from .game_blueprint import create_game_blueprints
from .score_blueprint import create_score_blueprint
from .user_blueprint import create_user_blueprint


def create_blueprints(
    app: Flask, ip: str, port: str, daily: bool = True, interval: int = 60
) -> Tuple[Blueprint, Blueprint]:
    api_blueprint = Blueprint("Api", __name__, url_prefix="/api")
    debug_blueprint = Blueprint("Debug", __name__, url_prefix="/debug")

    game, game_debug = create_game_blueprints(app, daily, interval)
    api_blueprint.register_blueprint(game)
    debug_blueprint.register_blueprint(game_debug)

    user = create_user_blueprint(app)
    api_blueprint.register_blueprint(user)

    score = create_score_blueprint(app, ip, port, daily, interval)
    api_blueprint.register_blueprint(score)

    return api_blueprint, debug_blueprint
