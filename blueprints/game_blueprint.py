from typing import Tuple

from flask import Blueprint, Flask, jsonify, request
from interfaces import jsonify_interface
from services import GameService


def create_game_blueprints(app: Flask, daily: bool, interval: int) -> Tuple[Blueprint, Blueprint]:

    game_service = GameService(app, daily, interval)

    # game blueprint

    game_blueprint = Blueprint("Game", __name__, url_prefix="/game")

    @game_blueprint.route("/new_game", methods=["GET"])
    @jsonify_interface
    def new_game():
        return game_service.get_word_length()

    @game_blueprint.route("/validate_input", methods=["POST"])
    @jsonify_interface
    def validate_input():
        return game_service.get_validated_word(**request.json)

    # debug blueprint

    debug_blueprint = Blueprint("Game-Debug", __name__, url_prefix="/game")

    @debug_blueprint.route("/get_word", methods=["GET"])
    @jsonify_interface
    def get_word():
        return game_service.get_word_info()

    @debug_blueprint.route("/set_word", methods=["GET"])
    @jsonify_interface
    def set_word():
        return game_service.force_reset()

    return game_blueprint, debug_blueprint
