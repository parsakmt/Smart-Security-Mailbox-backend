import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

import os
from dotenv import load_dotenv

load_dotenv()


# HELPER FUNCTIONS
def insert_database(query):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            dbname=os.getenv("DATABASE_NAME"),
            sslmode=os.getenv("DATABASE_SSLMODE"),
            sslrootcert=os.getenv("DATABASE_SSL_CERT_ROOT"),
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        connection.commit()
        return dict(cursor.fetchone())
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
            sslrootcert=os.getenv("DATABASE_SSL_CERT_ROOT"),
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        connection.commit()
        results = [dict(dict_row) for dict_row in cursor.fetchall()]
        return results
    except (Exception, Error) as error:
        print(f"Table Selection Error: {error}")
        raise error
