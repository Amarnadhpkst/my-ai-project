from flask import Blueprint, request, jsonify

predict_routes = Blueprint("predict", __name__)

@predict_routes.route("/predict", methods=["POST"])
def predict():
    data = request.json
    value = data.get("value", 0)

    result = "High" if value > 10 else "Low"

    return jsonify({"prediction": result})