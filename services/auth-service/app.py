from flask import Flask
from routes.auth_routes import auth_blueprint

app = Flask(__name__)

# Register routes
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(port=5001, debug=True)