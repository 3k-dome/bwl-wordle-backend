from dataclasses import asdict

from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import ScoreService
from services.user_service import Status


def create_score_blueprint(app: Flask, ip: str, port: str, daily: bool, interval: int) -> Blueprint:

    score_service = ScoreService(app, ip, port, daily, interval)

    # score blueprint

    score_blueprint = Blueprint("Score", __name__, url_prefix="/score")

    @score_blueprint.route("/add", methods=["POST"])
    @jwt_required()
    def add():
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
        username = get_jwt_identity()
        return jsonify([asdict(summary) for summary in score_service.get_summery(username)])

    return score_blueprint
