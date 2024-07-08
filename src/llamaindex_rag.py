from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from dotenv import load_dotenv
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
import os
load_dotenv()

base_dir = os.path.dirname(__file__)[:-4]
file_path = os.path.join(base_dir, 'data', 'my_diary').replace('\\', '/')
documents = SimpleDirectoryReader(input_dir=file_path, required_exts=[".pdf"]).load_data()

text_splitter = SentenceSplitter(chunk_size=200, chunk_overlap=30)
nodes = text_splitter.get_nodes_from_documents(documents=documents)

chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("diary_app")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model=OpenAIEmbedding())

query_engine = index.as_query_engine()

