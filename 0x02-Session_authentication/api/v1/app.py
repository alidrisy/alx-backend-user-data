#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = os.getenv("AUTH_TYPE", None)
if auth_type:
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()


@app.before_request
def authorization():
    """ authorize the user request """
    if not auth:
        return
    pathes = ['/api/v1/status/', '/api/v1/unauthorized/',
              '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if not auth.require_auth(request.path, pathes):
        return
    if auth.authorization_header(request) is None\
            and auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_forbidden(error) -> str:
    """ Not forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
