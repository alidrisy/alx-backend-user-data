#!/usr/bin/env python3
""" A basic Flask app """
from flask import (Flask, jsonify,
                   request, abort,
                   make_response, redirect)
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """ Main method """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ POST /users/
    JSON body:
      - email
      - password
    Return:
      - JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ POST /sessions/
    JSON body:
      - email
      - password
    Return:
      - JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ DELETE /sessions
    """
    session_id = request.form.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
    except Exception:
        abort(403)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ GET /profile
    """
    session_id = request.form.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        email = user.email
    except Exception:
        abort(403)
    return jsonify({"email": email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ GET /reset_password
    JSON body:
      - email
    Return:
      - JSON represented
    """
    email = request.form.get("email")
    try:
        reset = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ GET /reset_password
    JSON body:
      - email
    Return:
      - JSON represented
    """
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
