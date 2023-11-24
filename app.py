from flask import Flask, request
from psycopg2.errors import UniqueViolation
from datetime import datetime

from db import insert_database, select_database

app = Flask(__name__)


@app.get("/")
def get_home():
    return "Welcome to the Smart Security Mailbox Application", 200


@app.get("/mail")
def get_mail():
    try:
        query = "SELECT * FROM mail"
        result = select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/mail/<start_date>/<end_date>")
def get_mail_range(start_date, end_date):
    try:
        start_date_epoch = int(start_date) / 1000 
        end_date_epoch = int(end_date) / 1000
    except:
        return "Start Date or End Date is not a valid epoch timestamp", 404
    try:
        start_date_utc = datetime.fromtimestamp(start_date_epoch)
        end_date_utc = datetime.fromtimestamp(end_date_epoch)
        query = f"SELECT * FROM mail WHERE mail.time >= '{start_date_utc}' AND mail.time <= '{end_date_utc}'"
        result = select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/mail/<uid>")
def get_user_mail(uid):
    try:
        query = f"SELECT * FROM mail WHERE uid={uid}"
        result = select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.post("/mail")
def post_mail():
    try:
        uid = request.get_json()["uid"]
    except:
        return "User id is an invalid type", 404

    try:
        count = select_database(
            f"SELECT COUNT(*) + 1 as count FROM mail WHERE mail.uid = {uid}"
        )[0]["count"]
        query = f"INSERT INTO mail (mid, time, count, uid) VALUES(DEFAULT, '{datetime.utcnow()}', '{count}', '{uid}') RETURNING *;"
        result = insert_database(query)
        return result, 200
    except UniqueViolation as err:
        return err.pgerror, 400
    except Exception as err:
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
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/users")
def get_users():
    try:
        query = "SELECT * FROM users"
        result = select_database(query)
        return result, 200
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
        query = f"INSERT INTO users (uid, email, first_name, last_name) VALUES (DEFAULT, '{email}', '{first_name}', '{last_name}') RETURNING *;"
        result = insert_database(query)
        return result, 200
    except UniqueViolation as err:
        return err.pgerror, 400
    except Exception as err:
        return "Internal Server Error", 500
    

if __name__ == "__main__":
    app.run()