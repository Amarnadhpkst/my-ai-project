def login_user(username, password):

    # Dummy user (for now)
    if username == "admin" and password == "admin123":
        return {
            "status": True,
            "message": "Login successful"
        }

    return {
        "status": False,
        "message": "Invalid credentials"
    }