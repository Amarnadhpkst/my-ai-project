from flask import Blueprint, jsonify, request
from services.logic import process_data

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

    # Handle browser GET request
    if request.method == "GET":
        return jsonify({
            "success": False,
            "message": "Use POST method with JSON body"
        })

    # Read input JSON
    data = request.get_json()

    # Validation
    if not data or "value" not in data:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid input. 'value' is required"
        }), 400

    # Call service logic
    result = process_data(data)

    # Standard response
    return jsonify({
        "success": True,
        "data": {
            "input": data,
            "prediction": result
        },
        "error": None
    })