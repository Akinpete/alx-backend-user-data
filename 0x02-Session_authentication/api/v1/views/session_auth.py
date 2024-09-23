#!/usr/bin/env python3
"""Views for session Auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
      - returns dictionary rep of user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
        if not users or users == []:
            return jsonify({"error": "no user found for this email"}), 404
        for u in users:
            if u.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(u.id)
                response = jsonify(u.to_json())
                response.set_cookie((getenv('SESSION_NAME')), session_id)
                return response
            return jsonify({"error": "wrong password"}), 401
    except Exception:
        return None


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - returns empty dictionary after session deletion
    """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if not status:
        abort(404)
    return jsonify({}), 200
