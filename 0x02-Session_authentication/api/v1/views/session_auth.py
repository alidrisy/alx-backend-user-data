#!/usr/bin/env python3
"""
Module of SessionAuth views
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route("/auth_session/login/", methods=["POST"],
                 strict_slashes=False)
def login():
    """ POST /api/v1//auth_session/login/
    FORM body:
      - email
      - password
    Return:
      - User object JSON represented based on the email
      - 400 if no email or password
      - 404 If no User found
      - 401 If the password is not the one of the User found
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if type(email) != str or (email and len(email) == 0):
        return jsonify({"error": "email missing"}), 400
    if type(password) != str or (password and len(password) == 0):
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
        user = users[0]
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(getenv("SESSION_NAME"), session_id)
    return resp
