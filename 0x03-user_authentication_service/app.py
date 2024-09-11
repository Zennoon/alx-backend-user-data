#!/usr/bin/env python3
"""
Contains:
    Module level
    ============
    app - A flask application
"""
from flask import Flask, jsonify, request

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Handles GET requests to the root (/) route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Handles POST requests the the /users route"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
