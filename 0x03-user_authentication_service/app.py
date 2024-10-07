#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request, abort, redirect, url
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
    if request.method == "DELETE":
        session_id = request.cookies.get("session_id", None)
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            AUTH.destroy_session(session_id)
            return redirect("/")
        abort(403)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
