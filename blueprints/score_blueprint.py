from dataclasses import asdict
from typing import Tuple

from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import ScoreService
from services.user_service import Status


def create_score_blueprint(app: Flask, ip: str, port: str, daily: bool, interval: int) -> Tuple[Blueprint, ScoreService]:
    """Blueprint to add and retrieve scores from the database."""

    score_service = ScoreService(app, ip, port, daily, interval)

    score_blueprint = Blueprint("Score", __name__, url_prefix="/score")

    @score_blueprint.route("/add", methods=["POST"])
    @jwt_required()
    def add():
        """Calculates and adds a new score to the database, also returns it."""
        username = get_jwt_identity()
        status = score_service.add_score(username, **request.json)
        match status:
            case Status.Empty:
                return (
                    jsonify({"msg": "One of the fields 'max_tries', 'taken_tries' or 'found_letters' was empty."}),
                    400,
                )
            case Status.Error:
                return jsonify({"msg": "You already added a score for this session."}), 400
            case Status.Ok:
                return jsonify(asdict(score_service.get_latest_score(username)))

    @score_blueprint.route("/summary", methods=["GET"])
    @jwt_required()
    def summary():
        """Returns the summary of all played games of the calling player."""
        username = get_jwt_identity()
        return jsonify({id: asdict(summary) for id, summary in score_service.get_summery(username).items()})

    return score_blueprint, score_service
