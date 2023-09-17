import os
import psycopg2
from ..utils.generate_embeddings import generate_embedding

REPO_NAME = 'llama_index'
BATCH_SIZE = 32


def find_relevant(question):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    question_embedding = generate_embedding(question)
    sql = """
        SELECT contents FROM chunks
        ORDER BY embedding <-> %s
        LIMIT 5
    """
    cur.execute(sql, (question_embedding,))
    documents = cur.fetchall()
    documents = [d[0] for d in documents]

    conn.commit()
    cur.close()
    conn.close()

    return documents
