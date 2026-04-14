from flask import Flask
from routes.api import api_blueprint
from logger import setup_logger

app = Flask(__name__)

# ✅ Enable logging
setup_logger()

# ✅ Register routes
app.register_blueprint(api_blueprint)


# ✅ Global Exception Handling
@app.errorhandler(Exception)
def handle_exception(e):
    return {
        "success": False,
        "data": None,
        "error": str(e)
    }, 500


if __name__ == "__main__":
    app.run(debug=True)