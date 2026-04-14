import logging
from flask import Blueprint, jsonify, request
from services.logic import process_data
from services.auth import login_user

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "data": {"status": "OK"},
        "error": None
    })


@api_blueprint.route("/api/v1/predict", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        return jsonify({
            "success": False,
            "message": "Use POST method"
        })

    data = request.get_json()

    # ✅ Logging input
    logging.info(f"Received request: {data}")

    if not data or "value" not in data:
        logging.warning("Invalid input received")

        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid input"
        }), 400

    result = process_data(data)

    # ✅ Logging output
    logging.info(f"Prediction result: {result}")

    return jsonify({
        "success": True,
        "data": {
            "input": data,
            "prediction": result
        },
        "error": None
    })
@api_blueprint.route("/api/v1/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No input provided"
        }), 400

    username = data.get("username")
    password = data.get("password")

    result = login_user(username, password)

    if result["status"]:
        return jsonify({
            "success": True,
            "data": result,
            "error": None
        })
    else:
        return jsonify({
            "success": False,
            "data": None,
            "error": result["message"]
        }), 401