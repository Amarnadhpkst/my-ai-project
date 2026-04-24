from flask import Blueprint, request, jsonify
import jwt
from dotenv import load_dotenv
import os
#loading of environment variables from .env file
load_dotenv()

predict_blueprint = Blueprint("predict", __name__)

# 🔥 MUST MATCH auth service key
SECRET_KEY = os.getenv("SECRET_KEY")
print("PREDICTION SERVICE SECRET_KEY:", SECRET_KEY)  # 👈 ADD HERE

# ✅ Health Check
@predict_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "prediction service running"})


# 🤖 Prediction API
@predict_blueprint.route("/predict", methods=["POST"])
def predict():

    # 🔍 Get header
    auth_header = request.headers.get("Authorization")
    print("AUTH HEADER:", auth_header)  # Debug

    if not auth_header:
        return jsonify({
            "success": False,
            "message": "Token missing"
        }), 401

    try:
        # 🔍 Split Bearer token
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({
                "success": False,
                "message": "Invalid token format"
            }), 401

        token = parts[1]

        # 🔐 Validate token
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Invalid token",
            "error": str(e)
        }), 401

    # 📊 Process input
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