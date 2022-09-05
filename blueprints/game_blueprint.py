from typing import Tuple

from flask import Blueprint, Flask, request, jsonify
from interfaces import jsonify_interface
from services import GameService
from dataclasses import asdict


def create_game_blueprints(app: Flask, daily: bool, interval: int) -> Tuple[Blueprint, GameService]:
    """Main game blueprint used to initiate and play a game."""

    game_service = GameService(app, daily, interval)

    game_blueprint = Blueprint("Game", __name__, url_prefix="/game")

    @game_blueprint.route("/new_game", methods=["GET"])
    @jsonify_interface
    def new_game():
        """Returns the infos necessary to start a new game."""
        return game_service.get_word_length()

    @game_blueprint.route("/validate_input", methods=["POST"])
    @jsonify_interface
    def validate_input():
        """Returns the validated given input."""
        return game_service.get_validated_word(**request.json)

    @game_blueprint.route("/difficulties", methods=["GET"])
    def difficulties():
        """Returns an overview of all available difficulties."""
        return jsonify([asdict(item) for item in game_service.get_difficulties()])

    return game_blueprint, game_service
