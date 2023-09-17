from llama_index import set_global_service_context, ServiceContext, VectorStoreIndex, SimpleDirectoryReader
import time

service_context = ServiceContext.from_defaults(embed_model="local")
set_global_service_context(service_context)

reader = SimpleDirectoryReader(
    'llama_index', required_exts=['.py'], recursive=True)
documents = reader.load_data()
t1 = time.time()
index = VectorStoreIndex.from_documents(documents[:1])
t2 = time.time()
print(t2 - t1)


query_engine = index.as_query_engine()
response = query_engine.query("How can I get started with LlamaIndex?")
print(response)
