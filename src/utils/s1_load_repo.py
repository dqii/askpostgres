import os
import psycopg2

DATABASE_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}


def insert_file_into_db(conn, directory_path, file_path, get_document_type, get_document_url):
    repo_name = directory_path.split('/')[-1]
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        document_type = get_document_type(file_path)
        if not document_type:
            return
        content = file.read()
        repo_path = file_path.replace(directory_path + '/', '')
        url = get_document_url(document_type, repo_path)

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO documents (repo_name, document_type, repo_path, url, contents) VALUES (%s, %s, %s, %s, %s)",
            (repo_name, document_type, repo_path, url, content)
        )
        conn.commit()


def traverse_directory(directory_path, get_document_type, get_document_url):
    conn = psycopg2.connect(**DATABASE_CONFIG)

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            insert_file_into_db(conn, directory_path,
                                file_path, get_document_type, get_document_url)

    conn.close()
