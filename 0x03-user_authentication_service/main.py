#!/usr/bin/env python3
"""
Main model
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ test the POST /users endpoint """
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/users", data=data)
    assert response.json() == {"email": email, "message": "user created"}
    assert response.status_code == 200
    response = requests.post("http://127.0.0.1:5000/users", data=data)
    assert response.json() == {"message": "email already registered"}
    assert response.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """ test the POST /sessions endpoint withe wrong password """
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """ test the GET /profile endpoint """
    response = requests.get("http://127.0.0.1:5000/profile")
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """ test the POST /sessions endpoint """
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """ test the GET /profile endpoint """
    response = requests.get("http://127.0.0.1:5000/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ test the DELETE /sessions endpoint """
    headers = {"Content-Type": "application/json"}
    response = requests.delete("http://127.0.0.1:5000/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ test the POST /reset_password endpoint """
    response = requests.post("http://127.0.0.1:5000/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert response.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """ test the PUT /reset_password endpoint """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }
    response = requests.put("http://127.0.0.1:5000/reset_password", data=data)
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
