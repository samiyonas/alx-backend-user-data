#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """ home page """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ register user """
    email = request.form["email"]
    password = request.form["password"]

    if not email or not password:
        abort(400)

    try:
        new_user = AUTH.register_user(email, password)
        payload = {"email": email, "message": "user created"}
        payload = jsonify(payload)
        return payload, 200
    except ValueError:
        payload = {"message": "email already registered"}
        payload = jsonify(payload)
        payload.status_code = 400
        return payload


@app.route("/sessions", methods=["POST", "DELETE"], strict_slashes=False)
def login():
    """ login route """
    email = request.form["email"]
    password = request.form["password"]

    if not email or not password:
        abort(401)

    try:
        new_user = AUTH.valid_login(email, password)
        if not new_user:
            abort(401)
        session = AUTH.create_session(email)
        response = {"email": email, "message": "logged in"}
        response = jsonify(response)
        response.set_cookie("session_id", session)
        return response
    except Exception:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ let user into his/her profile page """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password():
    """ reset password if the user already exists """
    email = request.form["email"]

    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    response = {"email": email, "reset_token": token}
    return jsonify(response), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ update password """
    email = request.form["email"]
    new_password = request.form["new_password"]
    reset_token = request.form["reset_token"]

    stored_token = AUTH.get_reset_password_token(email)
    if stored_token != reset_token:
        abort(403)

    AUTH.update_password(reset_token, password)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
