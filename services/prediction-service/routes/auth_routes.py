from flask import Blueprint, request, jsonify

predict_blueprint = Blueprint("predict", __name__)

# Health check
@predict_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "prediction service running"})


# Prediction API
@predict_blueprint.route("/predict", methods=["POST"])
def predict():
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