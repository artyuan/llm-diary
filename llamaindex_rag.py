from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from dotenv import load_dotenv
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.agent import ReActAgent

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from prompts import new_prompt, instruction_str, context
import os
load_dotenv()

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'data', 'my_diary').replace('\\', '/')
documents = SimpleDirectoryReader(input_dir=file_path, required_exts=[".pdf"]).load_data()

# print(documents)
# print(documents[0].text)

text_splitter = SentenceSplitter(chunk_size=200, chunk_overlap=30)
nodes = text_splitter.get_nodes_from_documents(documents=documents)

# print(nodes[0].text)
# print(len(documents))
# print(len(nodes))

chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("diary_app")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model=OpenAIEmbedding())


query_engine = index.as_query_engine()

# tools = [
#     QueryEngineTool(
#         query_engine=query_engine,
#         metadata=ToolMetadata(
#             name="diary_data",
#             description="this gives detailed information about your recorded emotions",
#         ),
#     ),
# ]
#
# llm = OpenAI(model="gpt-3.5-turbo")
# agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)
# prompt = 'How did I feel On June 27th in my work?'
# result = agent.query(prompt)
# print(result)

# https://www.youtube.com/watch?v=tcqEUSNCn8I
# https://www.youtube.com/watch?v=fh6C_4yz5-M
# https://www.youtube.com/watch?v=xEgUC4bd_qI&t=3s