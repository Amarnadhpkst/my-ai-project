from flask import Blueprint, request, jsonify
import jwt
from dotenv import load_dotenv
import os
import logging
from prometheus_client import Counter, Histogram
import time

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# Blueprint
# =========================
predict_blueprint = Blueprint("predict", __name__)

# =========================
# Secret Key
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")

# =========================
# Logging
# =========================
logging.basicConfig(level=logging.INFO)

# =========================
# Prometheus Metrics
# =========================
REQUEST_COUNT = Counter(
    "prediction_request_count_total",
    "Total prediction requests"
)

REQUEST_LATENCY = Histogram(
    "prediction_request_latency_seconds",
    "Prediction request latency in seconds"
)

# =========================
# Health Check
# =========================
@predict_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "prediction service running"})


# =========================
# Prediction API
# =========================
@predict_blueprint.route("/predict", methods=["POST"])
def predict():

    start_time = time.time()

    logging.info("Prediction request received")

    # =========================
    # Validate request type
    # =========================
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json"
        }), 415

    data = request.get_json()

    # =========================
    # Auth header check
    # =========================
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "success": False,
            "message": "Token missing"
        }), 401

    try:
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({
                "success": False,
                "message": "Invalid token format"
            }), 401

        token = parts[1]

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        logging.info(f"Token valid for user: {decoded.get('user')}")

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Invalid token",
            "error": str(e)
        }), 401

    # =========================
    # Business logic
    # =========================
    try:
        value = int(data.get("value", 0))
        result = "High" if value > 10 else "Low"

        # =========================
        # Metrics (ONLY successful request)
        # =========================
        REQUEST_COUNT.inc()

        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)

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
        }), 400