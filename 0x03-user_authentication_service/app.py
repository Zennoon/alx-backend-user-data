#!/usr/bin/env python3
"""
Contains:
    Module level
    ============
    app - A flask application
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Handles GET requests to the root (/) route"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
