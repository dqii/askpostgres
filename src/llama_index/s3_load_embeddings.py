import os
import psycopg2
from ..utils.generate_embeddings import generate_embeddings

REPO_NAME = 'llama_index'
BATCH_SIZE = 32

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


def process_and_update_batch(table_name, batch):
    ids, contents = zip(*batch)
    embeddings = generate_embeddings(list(contents))
    for i, embedding in enumerate(embeddings):
        sql = f"UPDATE {table_name} SET embedding = %s WHERE id = %s"
        cur.execute(sql, (embedding, ids[i]))


# Select all documents from DB and process in batches
sql = """
    SELECT id, contents FROM documents WHERE repo_name = %s AND document_type = 'code'
"""
cur.execute(sql, (REPO_NAME,))
documents = cur.fetchall()

for i in range(0, len(documents), BATCH_SIZE):
    process_and_update_batch("documents", documents[i:i + BATCH_SIZE])
    print(f"Processed documents {i} - {i + BATCH_SIZE} of {len(documents)}")

# Select all chunks from DB and process in batches
sql = """
    SELECT id, contents FROM chunks WHERE document_id IN (
        SELECT id FROM documents WHERE repo_name = %s
    )
"""
cur.execute(sql, (REPO_NAME,))
chunks = cur.fetchall()

for i in range(0, len(chunks), BATCH_SIZE):
    process_and_update_batch("chunks", chunks[i:i + BATCH_SIZE])
    print(f"Processed chunks {i} - {i + BATCH_SIZE} of {len(chunks)}")

conn.commit()
cur.close()
conn.close()
