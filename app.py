from flask import Flask, request
from datetime import datetime
import psycopg2
from psycopg2.errors import UniqueViolation
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

import os
from helpers import db

app = Flask(__name__)


@app.get("/")
def get_home():
    return "Welcome to the Smart Security Mailbox Application", 200


@app.get("/mail")
def get_mail():
    try:
        query = "SELECT * FROM mail"
        result = db.select_database(query)
        return result, 200
    except Exception as e:
        return f"Internal Server Error", 500


@app.get("/mail/<start_date>/<end_date>")
def get_mail_range(start_date, end_date):
    try:
        start_date_epoch = int(start_date) / 1000
        end_date_epoch = int(end_date) / 1000
    except:
        return "Start Date or End Date is not a valid epoch timestamp", 400
    try:
        start_date_utc = datetime.fromtimestamp(start_date_epoch)
        end_date_utc = datetime.fromtimestamp(end_date_epoch)
        query = f"SELECT * FROM mail WHERE mail.time >= '{start_date_utc}' AND mail.time <= '{end_date_utc}'"
        result = db.select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/mail/<start_date>/<end_date>/<uid>")
def get_mail_range_uid(start_date, end_date, uid):
    try:
        start_date_epoch = int(start_date) / 1000
        end_date_epoch = int(end_date) / 1000
    except:
        return "Start Date or End Date is not a valid epoch timestamp", 400

    try:
        start_date_utc = datetime.fromtimestamp(start_date_epoch)
        end_date_utc = datetime.fromtimestamp(end_date_epoch)
        query = f"SELECT * FROM mail WHERE mail.time >= '{start_date_utc}' AND mail.time <= '{end_date_utc}' AND mail.uid = {uid}"
        result = db.select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/mail/<uid>")
def get_user_mail(uid):
    try:
        query = f"SELECT * FROM mail WHERE uid={uid}"
        result = db.select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.post("/mail")
def post_mail():
    try:
        uid = int(request.get_json()["uid"])
    except:
        return "User id is an invalid type", 400

    try:
        count = db.select_database(
            f"SELECT COUNT(*) + 1 as count FROM mail WHERE mail.uid = {uid}"
        )[0]["count"]
        query = f"INSERT INTO mail (mid, time, count, uid) VALUES(DEFAULT, '{datetime.utcnow()}', '{count}', '{uid}') RETURNING *;"
        result = db.insert_database(query)
        return result, 200
    except UniqueViolation as err:
        return err.pgerror, 400
    except Exception as err:
        return "Internal Server Error", 500


@app.get("/users")
def get_users():
    try:
        query = "SELECT * FROM users"
        result = db.select_database(query)
        return result, 200
    except Exception as e:
        return f"{e}", 500


@app.get("/users/<uid>")
def get_user_uid(uid):
    try:
        uid = int(uid)
    except:
        return "User id is an invalid type", 400

    try:
        query = f"SELECT * FROM users WHERE uid = {uid}"
        result = db.select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.get("/users/email/<email>")
def get_user_email(email):
    try:
        query = f"SELECT * FROM users WHERE email = '{email}'"
        result = db.select_database(query)
        return result, 200
    except:
        return "Internal Server Error", 500


@app.post("/users")
def post_new_user():
    request_json = request.get_json()
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "mac_address",
        "service_uuid",
        "ssid_characteristic_uuid",
        "password_characteristic_uuid",
        "uid_characteristic_uuid",
        "wifi_ssid",
        "wifi_password",
    ]

    if any(
        (field not in request_json or not isinstance(request_json[field], str))
        for field in required_fields
    ):
        return "A field is not valid or present", 400
    try:
        (
            email,
            first_name,
            last_name,
            mac_address,
            service_uuid,
            ssid_characteristic_uuid,
            password_characteristic_uuid,
            uid_characteristic_uuid,
            wifi_ssid,
            wifi_password,
        ) = (
            request_json["email"],
            request_json["first_name"],
            request_json["last_name"],
            request_json["mac_address"],
            request_json["service_uuid"],
            request_json["ssid_characteristic_uuid"],
            request_json["password_characteristic_uuid"],
            request_json["uid_characteristic_uuid"],
            request_json["wifi_ssid"],
            request_json["wifi_password"],
        )
        query = f"""
            INSERT INTO users (
                uid, email, first_name, last_name, mac_address,
                service_uuid, ssid_characteristic_uuid, password_characteristic_uuid,
                uid_characteristic_uuid, wifi_ssid, wifi_password
            ) VALUES (
                DEFAULT, '{email}', '{first_name}', '{last_name}', '{mac_address}',
                '{service_uuid}', '{ssid_characteristic_uuid}', '{password_characteristic_uuid}',
                '{uid_characteristic_uuid}', '{wifi_ssid}', '{wifi_password}'
            ) RETURNING *;
        """
        result = db.insert_database(query)
        return result, 200
    except UniqueViolation as err:
        return err.pgerror, 400
    except Exception as err:
        return f"Internal Server Error", 500


@app.route("/users/<email>", methods=["DELETE"])
def delete_user_email(email):
    try:
        query = f"DELETE FROM users WHERE email='{email}' RETURNING *"
        result = db.select_database(query)
        return result, 200
    except Error as e:
        return f"{e}", 500


if __name__ == "__main__":
    app.run()
