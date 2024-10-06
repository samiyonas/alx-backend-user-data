#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
