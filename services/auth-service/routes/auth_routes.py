from flask import Blueprint, request, jsonify
import jwt
import datetime
import bcrypt
from db import get_connection
from dotenv import load_dotenv
import os
import logging

# ✅ Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ✅ Load env variables
load_dotenv()

auth_blueprint = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY")
print("AUTH SERVICE SECRET_KEY:", SECRET_KEY)


# ✅ Health Check
@auth_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "auth service running"})


# 🔐 REGISTER API
@auth_blueprint.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        logging.warning("Invalid JSON in register")
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    logging.info(f"Register attempt for user: {username}")

    if not username or not password:
        logging.warning("Missing username or password")
        return jsonify({"success": False, "message": "Missing fields"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password.decode('utf-8'))
        )

        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"User registered successfully: {username}")

        return jsonify({"success": True, "message": "User registered successfully"})

    except Exception as e:
        logging.error(f"Register error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})


# 🔑 LOGIN API
@auth_blueprint.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        logging.warning("Invalid JSON in login")
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    logging.info(f"Login attempt for user: {username}")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

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
            logging.warning(f"User not found: {username}")
            return jsonify({"success": False, "message": "User not found"}), 404

        stored_password = user[0]

        # 🔐 Validate password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):

            token = jwt.encode({
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")

            # ✅ Ensure token is string
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            logging.info(f"Login success: {username}")

            return jsonify({
                "success": True,
                "token": token
            })

        else:
            logging.warning(f"Invalid password for user: {username}")
            return jsonify({"success": False, "message": "Invalid password"}), 401

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})