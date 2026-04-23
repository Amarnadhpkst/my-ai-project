from flask import Blueprint, request, jsonify
import jwt
import datetime
import bcrypt
from db import get_connection

auth_blueprint = Blueprint("auth", __name__)

SECRET_KEY = "my_super_secret_key_12345"


# Health
@auth_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "auth service running"})


# 🔐 REGISTER API
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password.decode('utf-8'))
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "User registered successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# 🔑 LOGIN API
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        stored_password = user[0]

        # check password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):

            token = jwt.encode({
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            return jsonify({
                "success": True,
                "token": token
            })

        else:
            return jsonify({"success": False, "message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})