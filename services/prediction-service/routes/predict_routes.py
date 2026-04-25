from flask import Blueprint, request, jsonify
import jwt
from dotenv import load_dotenv
import os
import logging

# ✅ Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ✅ Load env
load_dotenv()

predict_blueprint = Blueprint("predict", __name__)

# 🔐 SECRET KEY (must match auth service)
SECRET_KEY = os.getenv("SECRET_KEY")

print("PREDICTION SERVICE SECRET_KEY:", SECRET_KEY)


# ✅ Health Check
@predict_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "prediction service running"})


# 🤖 Prediction API
@predict_blueprint.route("/predict", methods=["POST"])
def predict():

    logging.info("Prediction request received")

    # ✅ Step 1: Check JSON
    if not request.is_json:
        logging.warning("Request is not JSON")
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json"
        }), 415

    # ✅ Step 2: Get Authorization
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        logging.warning("Token missing")
        return jsonify({
            "success": False,
            "message": "Token missing"
        }), 401

    try:
        # ✅ Step 3: Validate format
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            logging.warning("Invalid token format")
            return jsonify({
                "success": False,
                "message": "Invalid token format"
            }), 401

        # ✅ Step 4: Decode token
        token = parts[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        logging.info(f"Token valid for user: {decoded.get('user')}")

    except Exception as e:
        logging.error(f"Token validation failed: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Invalid token",
            "error": str(e)
        }), 401

    # ✅ Step 5: Process data
    data = request.get_json()
    value = data.get("value", 0)

    logging.info(f"Prediction input value: {value}")

    try:
        value = int(value)

        result = "High" if value > 10 else "Low"

        logging.info(f"Prediction result: {result}")

        return jsonify({
            "success": True,
            "data": {
                "input": value,
                "prediction": result
            }
        })

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        })