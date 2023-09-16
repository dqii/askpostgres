import os
import psycopg2
from ..utils.generate_embeddings import generate_embedding


REPO_NAME = 'llama_index'

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Select all documents from DB
sql = """
    SELECT id, contents FROM documents WHERE repo_name = %s AND document_type = 'code'
"""
cur.execute(sql, (REPO_NAME,))
documents = cur.fetchall()

# For all documents, generate embeddings for them and insert the embeddings into DB
for document_id, document_contents in documents:
    embedding = generate_embedding(document_contents)
    sql = """
        UPDATE documents SET embedding = %s WHERE id = %s
    """
    cur.execute(sql, (embedding, document_id))

# Select all chunks from DB
sql = """
    SELECT id, contents FROM chunks WHERE document_id IN (
        SELECT id FROM documents WHERE repo_name = %s
    )
"""
cur.execute(sql, (REPO_NAME,))
chunks = cur.fetchall()

# For all chunks, generate embeddings for them and insert the embeddings into DB
for chunk_id, chunk_contents in chunks:
    embedding = generate_embedding(chunk_contents)
    sql = """
        UPDATE chunks SET embedding = %s WHERE id = %s
    """
    cur.execute(sql, (embedding, chunk_id))

conn.commit()
cur.close()
conn.close()
