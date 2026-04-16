from models.model import User

def login_user(username, password):

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return {
            "status": True,
            "message": "Login successful"
        }

    return {
        "status": False,
        "message": "Invalid credentials"
    }