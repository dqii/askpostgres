import os
import psycopg2

DATABASE_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}


def traverse_directory(directory_path, insert_file_into_db):
    conn = psycopg2.connect(**DATABASE_CONFIG)

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            insert_file_into_db(conn, file_path)

    conn.close()
