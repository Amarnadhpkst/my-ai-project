from flask import Flask
from routes.auth_routes import auth_blueprint
import logging

app = Flask(__name__)

# ✅ Logging (ONLY HERE)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Register blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)