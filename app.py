from flask import Flask, jsonify, request
from datetime import datetime
import json

from db import insert_database, select_database

app = Flask(__name__)


@app.get("/")
def get_home():
    return "Welcome to the Smart Security Mailbox Application", 200


@app.get("/mail")
def get_mail():
    try:
        query = "SELECT * FROM mail"
        result = jsonify(select_database(query))
        return jsonify(result), 200
    except:
        return "Internal Server Error", 500


@app.get("/mail/<start_date>/<end_date>")
def get_mail_range(start_date, end_date):
    try:
        query = f"SELECT * FROM mail WHERE mail.time >= '{start_date}' AND mail.time <= '{end_date}'"
        result = jsonify(select_database(query))
        return jsonify(result), 200
    except:
        return "Internal Server Error", 500


@app.get("/users/<uid>")
def get_mail_user(uid):
    try:
        uid = int(uid)
    except:
        return "User id is an invalid type", 404

    try:
        query = f"SELECT * FROM mail WHERE mail.uid = {uid}"
        result = select_database(query)
        return jsonify(result), 200
    except:
        return "Internal Server Error", 500


@app.get("/users")
def get_users():
    try:
        query = "SELECT * FROM users"
        result = select_database(query)
        return jsonify(result), 200
    except:
        return "Internal Server Error", 500


@app.post("/users")
def post_new_user():
    request_json = request.get_json()
    required_fields = ["first_name", "last_name", "email"]
    if any(
        (field not in request_json or not isinstance(request_json[field], str))
        for field in required_fields
    ):
        return "Invalid first name, last name, or email", 400
    try:
        email, first_name, last_name = (
            request_json["email"],
            request_json["first_name"],
            request_json["last_name"],
        )
        query = f"INSERT INTO users (uid, email, first_name, last_name) VALUES (DEFAULT, '{email}', '{first_name}', '{last_name}');"
        result = insert_database(query)
        return jsonify(result), 200
    except:
        return "Internal Server Error", 500
