from typing import Tuple

from flask import Blueprint, Flask

from interfaces import jsonify_interface
from .game_blueprint import create_game_blueprints
from .score_blueprint import create_score_blueprint
from .user_blueprint import create_user_blueprint
from .state_blueprint import create_state_blueprint


def create_blueprints(app: Flask, ip: str, port: str, daily: bool, interval: int) -> Tuple[Blueprint, Blueprint]:
    """Creates all sub blueprints and registers them on an api blueprint.
    
    This method creates all other blueprints via their own factory methods
    to inject all necessary parameters to those and their inner services. 
    """

    # create main api blue print, which consists of our other blueprints
    api_blueprint = Blueprint("Api", __name__, url_prefix="/api")

    game, game_service = create_game_blueprints(app, daily, interval)
    state, state_service = create_state_blueprint(app, daily, interval)
    score, score_service = create_score_blueprint(app, ip, port, daily, interval)
    user = create_user_blueprint(app)

    api_blueprint.register_blueprint(game)
    api_blueprint.register_blueprint(state)
    api_blueprint.register_blueprint(score)
    api_blueprint.register_blueprint(user)

    # create a simple debug blueprint
    debug_blueprint = Blueprint("Debug", __name__, url_prefix="/debug")

    @debug_blueprint.route("/set_word", methods=["GET"])
    @jsonify_interface
    def set_word():
        state_service.reset()
        score_service.reset()
        return game_service.force_reset()

    @debug_blueprint.route("/get_word", methods=["GET"])
    @jsonify_interface
    def get_word():
        return game_service.get_word_info()

    return api_blueprint, debug_blueprint
