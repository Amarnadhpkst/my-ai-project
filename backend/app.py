from flask import Flask
from routes.api import api_blueprint
from db import db
from logger import setup_logger
from models.model import User
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ DB CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Initialize DB
db.init_app(app)

# ✅ Logger
setup_logger()

# ✅ Register routes
app.register_blueprint(api_blueprint)

# ✅ Create DB tables + CHECK DATA
with app.app_context():
    db.create_all()


# ✅ Global Exception Handling
@app.errorhandler(Exception)
def handle_exception(e):
    return {
        "success": False,
        "data": None,
        "error": str(e)
    }, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)