#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv("AUTH_TYPE", None)
if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth

        auth = BasicAuth()
    elif auth == "session_auth":
        from api.v1.auth.session_auth import SessionAuth

        auth = SessionAuth()
    elif auth == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth

        auth = SessionExpAuth()
    elif auth == "session_db_auth":
        from api.v1.auth.session_db_auth import SessionDBAuth

        auth = SessionDBAuth()
    else:
        from api.v1.auth.auth import Auth

        auth = Auth()


@app.before_request
def before_req():
    """Executed before every request"""
    if auth:
        require_auth = auth.require_auth(request.path,
                                         [
                                             "/api/v1/status/",
                                             "/api/v1/unauthorized/",
                                             "/api/v1/forbidden/",
                                             "/api/v1/auth_session/login/"
                                         ])
        if require_auth:
            if not (auth.authorization_header(request)
                    or auth.session_cookie(request)):
                abort(401)
            if not auth.current_user(request):
                abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_resource(error) -> str:
    """ Forbidden resource handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
