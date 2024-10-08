#!/usr/bin/env python3
"""
Contains:
    Module level
    ============
    app - A flask application
"""
from flask import abort, Flask, jsonify, redirect, request, url_for

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


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Handles DELETE requests to the /sessions route
    Handles user logout and session deletion"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for("index"))
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Handles GET requests to the /profile route
    Returns basic info about the requesting user"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Handles POST requests to the /reset_password route
    Handles requests for password reset tokens"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Handles PUT requests to the /reset_password route
    Handles requests for password resets"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
