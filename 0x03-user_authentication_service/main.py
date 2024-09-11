#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    register_user - checks the POST /users endpoint
    log_in_wrong_password - checks the POST /sessions endpoint with
    incorrect password
    log_in - checks the POST /sessions endpoint with correct credentials
    profile_unlogged - checks the GET /profile endpoint with no session id
    profile_logged = checks the GET /profile endpoint with a session id
    log_out - checks the DELETE /sessions endpoint
    reset_password_token - checks the POST /reset_password endpoint
    update_password - c
"""
import requests

BASE_URL = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """checks the POST /users endpoint"""
    resp = requests.post(BASE_URL + "users", data={
        "email": email,
        "password": password
    })
    json = resp.json()
    assert (
        resp.status_code == 200 and json == {
            "email": email,
            "message": "user created"
        } or resp.status_code == 400 and json == {
            "message": "email already registered"
        }
    )


def log_in_wrong_password(email: str, password: str) -> None:
    """checks the POST /sessions endpoint with
    incorrect password"""
    resp = requests.post(BASE_URL + "sessions", data={
        "email": email,
        "password": password
    })
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """checks the POST /sessions endpoint with correct credentials"""
    resp = requests.post(BASE_URL + "sessions", data={
        "email": email,
        "password": password
    })
    assert resp.status_code == 200
    json = resp.json()
    assert json == {
        "email": email,
        "message": "logged in"
    }
    session_id = resp.cookies.get("session_id")
    assert isinstance(session_id, str)
    return session_id


def profile_unlogged() -> None:
    """checks the GET /profile endpoint with no session id"""
    resp = requests.get(BASE_URL + "profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    resp = requests.get(BASE_URL + "profile", cookies={
        "session_id": session_id
    })
    assert resp.status_code == 200
    json = resp.json()
    assert (json.get("email") is not None
            and isinstance(json.get("email"), str))


def log_out(session_id: str) -> None:
    """checks the DELETE /sessions endpoint"""
    resp = requests.delete(BASE_URL + "sessions", cookies={
        "session_id": session_id
    }, allow_redirects=True)
    assert (resp.status_code == 403
            or (resp.status_code == 200
                and resp.json() == {
                    "message": "Bienvenue"
                }))


def reset_password_token(email: str) -> str:
    """checks the POST /reset_password endpoint"""
    resp = requests.post(BASE_URL + "reset_password", data={
        "email": email
    })
    assert resp.status_code == 200
    json = resp.json()
    assert (json.get("email") == email
            and isinstance(json.get("reset_token"), str))
    return json.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """checks the PUT /reset_password endpoint"""
    resp = requests.put(BASE_URL + "reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })

    assert resp.status_code == 200
    json = resp.json()
    assert (json.get("email") == email
            and json.get("message") == "Password updated")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
