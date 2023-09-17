from llama_index import set_global_service_context, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from ..utils.get_service_context import get_service_context
import chromadb

# Set embedding context
set_global_service_context(get_service_context())

# Load documents
reader = SimpleDirectoryReader(
    '/Users/diqi/lantern/askpostgres/repo/llama_index', required_exts=['.py'], recursive=True)
documents = reader.load_data()
print("Number of documents:", len(documents))

# Build index
db = chromadb.PersistentClient(
    path='/Users/diqi/lantern/askpostgres/src/llama_index/llama_index/chromadb')
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
print("Index built")
