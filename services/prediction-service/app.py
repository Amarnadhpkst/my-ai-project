from flask import Flask
from routes.predict_routes import predict_blueprint

app = Flask(__name__)

app.register_blueprint(predict_blueprint)

if __name__ == "__main__":
    app.run(port=5002, debug=True)