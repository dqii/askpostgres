import os
import psycopg2
from ..utils.chunk import chunk_code


REPO_NAME = 'llama_index'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Delete any chunks from DB
sql = """
    DELETE FROM chunks
    WHERE document_id IN (
        SELECT id FROM documents WHERE repo_name = %s
    )
"""
cur.execute(sql, (REPO_NAME,))

# Select all documents from DB
sql = """
    SELECT id, contents FROM documents WHERE repo_name = %s AND document_type = 'code'
"""
cur.execute(sql, (REPO_NAME,))
documents = cur.fetchall()

# For all documents , chunk them and insert them into DB
for document_id, document_contents in documents:
    chunks = chunk_code(document_contents, "py")
    for chunk in chunks:
        sql = """
            INSERT INTO chunks (document_id, contents)
            VALUES (%s, %s)
        """
        cur.execute(sql, (document_id, chunk))

conn.commit()
cur.close()
conn.close()
