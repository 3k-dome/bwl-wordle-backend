from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from services import Status, UserService


def create_user_blueprint(app: Flask) -> Blueprint:
    """User management blueprint."""

    user_service = UserService(app)

    # user blueprint

    user_blueprint = Blueprint("User", __name__, url_prefix="/auth")

    @user_blueprint.route("/register", methods=["POST"])
    def register():
        """Registers a new user account."""
        _, status = user_service.add_user(**request.json)
        match status:
            case Status.Empty:
                return jsonify({"msg": "Username or password was empty."}), 400
            case Status.Error:
                return jsonify({"msg": "Username already exist."}), 400
            case Status.Ok:
                return jsonify({"msg": "Successfully registered."}), 201

    @user_blueprint.route("/login", methods=["POST"])
    def login():
        """Tries to login a calling user, returns his jwt if successful."""
        _, status = user_service.get_user(**request.json)
        match status:
            case Status.Empty:
                return jsonify({"msg": "Username or password was empty."}), 400
            case Status.Error:
                return jsonify({"msg": "No matching user was found."}), 400
            case Status.Ok:
                return (
                    jsonify(
                        {
                            "msg": "Successfully logged in.",
                            "token": create_access_token(identity=request.json["username"]),
                        }
                    ),
                    200,
                )

    @user_blueprint.route("/delete", methods=["POST"])
    @jwt_required()
    def delete():
        """Allows a user to delete his account."""
        _, status = user_service.del_user(**request.json)
        match status:
            case Status.Empty:
                return jsonify({"msg": "Username or password was empty."}), 400
            case Status.Error:
                return jsonify({"msg": "No matching user was found."}), 400
            case Status.Ok:
                return unset_jwt_cookies(jsonify({"msg": "Successfully deleted."})), 200

    @user_blueprint.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        """Logout by disabling the given jwt."""
        response = jsonify({"msg": "Successfully logged out."})
        unset_jwt_cookies(response)
        return response

    return user_blueprint
