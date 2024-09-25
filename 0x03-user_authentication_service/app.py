#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request, abort,\
    make_response, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        if AUTH.valid_login(email=email, password=password):
            session_id = AUTH.create_session(email=email)
            response = make_response(jsonify({"email": email,
                                              "message": "logged in"}))
            response.set_cookie('session_id', session_id)
            return response
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout user"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
