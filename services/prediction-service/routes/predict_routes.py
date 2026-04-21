from flask import Blueprint, request, jsonify
import jwt

predict_blueprint = Blueprint("predict", __name__)

SECRET_KEY = "mysecret"

# Health check
@predict_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "prediction service running"})


# Prediction API with token validation
@predict_blueprint.route("/predict", methods=["POST"])
def predict():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({
            "success": False,
            "message": "Token missing"
        }), 401

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid token"
        }), 401

    data = request.get_json()
    value = data.get("value", 0)

    try:
        value = int(value)

        if value > 10:
            result = "High"
        else:
            result = "Low"

        return jsonify({
            "success": True,
            "data": {
                "input": value,
                "prediction": result
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })