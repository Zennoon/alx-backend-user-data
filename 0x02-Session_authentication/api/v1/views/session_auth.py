#!/usr/bin/env python3
""" Module for session authentication views
"""
import hashlib
import os
from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session_login():
    """Logs user in and creates a session for them"""
    attrs = ["email", "password"]
    for idx in range(len(attrs)):
        if request.form.get(attrs[idx]) is None:
            return jsonify({
                "error": attrs[idx] + " missing"
            }), 400
        attrs[idx] = request.form.get(attrs[idx])
    email, password = attrs
    users = User.search({"email": email})
    if not users:
        return jsonify({
            "error": "no user found for this email"
        }), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({
            "error": "wrong password"
        }), 401
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv("SESSION_NAME", "_my_session_id"),
                        session_id)
    return response


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def auth_session_logout():
    """Logs user out (destroys their session)"""
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
