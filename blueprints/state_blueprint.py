from typing import Tuple

from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import StateService


def create_state_blueprint(app: Flask, daily: bool, interval: int) -> Tuple[Blueprint, StateService]:

    state_service = StateService(app, daily, interval)

    # state blueprint

    state_blueprint = Blueprint("State", __name__, url_prefix="/state")

    @state_blueprint.route("/save", methods=["POST"])
    @jwt_required()
    def save():
        username = get_jwt_identity()
        state_service.save_state(username, request.json)
        return jsonify({"msg": "Successfully saved."}), 201

    @state_blueprint.route("/load", methods=["GET"])
    @jwt_required()
    def load():
        username = get_jwt_identity()
        state = state_service.load_state(username)
        if state:
            return jsonify(state), 200
        return jsonify({"msg": "No save for this session was fund."}), 404

    return state_blueprint, state_service
