#!/usr/bin/env python3
""" A basic Flask app """
from flask import (Flask, jsonify,
                   request, abort,
                   make_response, redirect)
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
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
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
