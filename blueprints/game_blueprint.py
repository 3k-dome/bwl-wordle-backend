from typing import Tuple

from flask import Blueprint, Flask, request
from interfaces import jsonify_interface
from services import GameService


def create_game_blueprints(app: Flask, daily: bool, interval: int) -> Tuple[Blueprint, GameService]:

    game_service = GameService(app, daily, interval)

    game_blueprint = Blueprint("Game", __name__, url_prefix="/game")

    @game_blueprint.route("/new_game", methods=["GET"])
    @jsonify_interface
    def new_game():
        return game_service.get_word_length()

    @game_blueprint.route("/validate_input", methods=["POST"])
    @jsonify_interface
    def validate_input():
        return game_service.get_validated_word(**request.json)

    return game_blueprint, game_service
