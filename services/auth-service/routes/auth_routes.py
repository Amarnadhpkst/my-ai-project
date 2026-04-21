from flask import Blueprint, request, jsonify
import jwt
import datetime

auth_blueprint = Blueprint("auth", __name__)

SECRET_KEY = "mysecret"

# Test API
@auth_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "auth service running"})


# Login API
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin":

        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "success": True,
            "token": token
        })

    else:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        })