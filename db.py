import psycopg2
from psycopg2 import Error

import os
from dotenv import load_dotenv

load_dotenv()

def insert_database(query):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            dbname=os.getenv("DATABASE_NAME"),
            sslmode=os.getenv("DATABASE_SSLMODE"),
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except (Exception, Error) as error:
        print(f"Table Insertion Error: {error}")
        raise error


def select_database(query):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            dbname=os.getenv("DATABASE_NAME"),
            sslmode=os.getenv("DATABASE_SSLMODE"),
        )
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except (Exception, Error) as error:
        print(f"Table Selection Error: {error}")
