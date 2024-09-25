#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """add new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        try:
            user = AUTH.register_user(email=email, password=password)
            return jsonify({"email": email, "message": "user created"}), 201
        except ValueError as err:
            return jsonify({"message": "email already registered"}), 400

    return jsonify({"message": "email and password required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
