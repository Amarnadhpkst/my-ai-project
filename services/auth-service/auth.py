from models.model import User
from utils import generate_token

def login_user(username, password):

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        token = generate_token(username)

        return {
            "status": True,
            "message": "Login successful",
            "token": token
        }

    return {
        "status": False,
        "message": "Invalid credentials"
    }