import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index import set_global_service_context, VectorStoreIndex
from ..utils.get_service_context import get_service_context
import chromadb

# Set embedding context
set_global_service_context(get_service_context())

# Load Chroma index
db = chromadb.PersistentClient(
    path='/Users/diqi/lantern/askpostgres/src/llama_index/llama_index/chromadb')
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("How can I get started with LlamaIndex?")
print(response)

"""
To get started with LlamaIndex, you can use the data connectors provided in the module. Each connector inherits from a `BaseReader` class and allows you to connect to a data source and load Document objects from that data source. Alternatively, you can manually construct Document objects, as explained in the "Insert How-To Guide" provided. The API definition of a Document is also available, where the minimum requirement is a `text` property.
"""
