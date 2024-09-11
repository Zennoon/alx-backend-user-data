#!/usr/bin/env python3
"""
Contains:
    Module level
    ============
    app - A flask application
"""
from flask import abort, Flask, jsonify, request

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Handles GET requests to the root (/) route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Handles POST requests to the /users route.
    Handles user registration"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Handles POST requests to the /sessions route
    Handles user login and session creation"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
