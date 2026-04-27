from flask import Flask
from routes.predict_routes import predict_blueprint
from prometheus_client import generate_latest

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

app.register_blueprint(predict_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)