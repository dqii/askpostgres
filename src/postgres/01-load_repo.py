import os
from ..utils import traverse_directory


DIRECTORY_PATH = "/app/repo/postgresql"
FILE_TYPES = {
    '.sgml': 'docs',
    '.c': 'code',
}


def get_document_type(filename):
    ext = os.path.splitext(filename)[1]
    return FILE_TYPES.get(ext)


def get_document_url(document_type, file_path):
    if document_type == 'code':
        return "https://github.com/postgres/postgres/blob/master/" + file_path
    if document_type == 'docs':
        basename = os.path.basename(file_path).split('.')[0]
        if '/ref/' in file_path:
            return f"https://www.postgresql.org/docs/15/sql-{basename.replace('_', '')}.html"
        else:
            return f"https://www.postgresql.org/docs/15/{basename}.html"


def insert_file_into_db(conn, file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        document_type = get_document_type(file_path)
        if not document_type:
            return
        content = file.read()
        repo_path = file_path.replace(DIRECTORY_PATH + '/', '')
        url = get_document_url(document_type, repo_path)

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO postgres_documents (document_type, repo_path, url, contents) VALUES (%s, %s, %s, %s)",
            (document_type, repo_path, url, content)
        )
        conn.commit()


if __name__ == "__main__":
    traverse_directory(DIRECTORY_PATH, insert_file_into_db)
