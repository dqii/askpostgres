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
        SELECT id FROM documents WHERE repo_name = %s AND document_type = 'code'
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


"""
askpostgres % python3 -m src.llama_index.s5_ask_llm
To get started with LlamaIndex, you can follow these steps:

1. Install LlamaIndex: Start by installing LlamaIndex using pip:

   ```
   pip install llama-index
   ```

2. Import the necessary modules: Import the required modules in your Python script or notebook:

   ```python
   from llama_index import LlamaIndex, LlamaDataset
   ```

3. Initialize LlamaIndex: Create an instance of LlamaIndex, passing the path to your data directory as an argument:

   ```python
   index = LlamaIndex(data_dir="/path/to/data")
   ```

4. Ingest data: Use the `ingest` method to ingest your data into LlamaIndex. This method takes a LlamaDataset object as an argument, which can be created using the `LlamaDataset.from_csv` or `LlamaDataset.from_pandas` methods:

   ```python
   dataset = LlamaDataset.from_csv("/path/to/data.csv")
   index.ingest(dataset)
   ```

   You can also use other methods like `from_json` or `from_dict` depending on your data format.

5. Structure data: After ingesting the data, you can structure it using indices or graphs. LlamaIndex provides methods like `create_index` and `create_graph` for this purpose. For example, to create an index on a specific column, you can use the `create_index` method:

   ```python
   index.create_index("column_name")
   ```

6. Query data: Once your data is structured, you can query it using LlamaIndex's retrieval/query interface. The `query` method allows you to provide an input prompt and get back the retrieved context and knowledge-augmented output. Here's an example:

   ```python
   input_prompt = "What are songs by Taylor Swift in the pop genre"
   retrieved_context, augmented_output = index.query(input_prompt)
   ```

   You can also specify additional parameters like the number of documents to retrieve using the `top_k` parameter.

7. Customize and extend: LlamaIndex provides both high-level and low-level APIs for customization and extension. Advanced users can customize and extend modules like data connectors, indices, retrievers, query engines, and reranking modules to fit their specific needs.

These are the basic steps to get started with LlamaIndex. You can refer to the LlamaIndex documentation and samples for more detailed information and examples.
"""
