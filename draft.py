# ## llama index
# from llama_index.core import PromptTemplate
# from llama_index.readers.file import PyMuPDFReader
# from llama_index.core import VectorStoreIndex
# from llama_index.llms.openai import OpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
# path = os.path.join("data\joy", "joy_diary.pdf")
# loader = PyMuPDFReader()
# diary_pdf = loader.load(file_path=path)
#
# gpt35_llm = OpenAI(model="gpt-3.5-turbo")
#
# index = VectorStoreIndex.from_documents(diary_pdf)
#
# query_str = "What was the best and worst moment of my week as mentioned in the context?"
#
# query_engine = index.as_query_engine(similarity_top_k=3, llm=gpt35_llm)
# prompts_dict = query_engine.get_prompts()
#
# response = query_engine.query(query_str)
# print(str(response))
#
#
# ##--------------------------------------------------------------------------------------------
# import os
# from dotenv import load_dotenv
# import openai
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.core.node_parser import SentenceSplitter
#
# load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
#
# CHROMA_PATH = "chroma"
# DATA_PATH = "data/books"
#
# def main():
#     generate_data_store()
#
# def generate_data_store():
#     documents = load_documents()
#     chunks = split_text(documents)
#     save_to_chroma(chunks)
#
#
# def load_documents():
#     loader = SimpleDirectoryReader(input_dir="../data/joy", required_exts=[".pdf"])
#     documents = loader.load_data()
#     return documents
#
#
# def split_text(documents):
#     text_splitter = SentenceSplitter(chunk_size=200, chunk_overlap=30)
#     nodes = text_splitter.get_nodes_from_documents(documents=documents)
#
#     return nodes
#
#
# def save_to_chroma(chunks: list[Document]):
#     # Clear out the database first.
#     if os.path.exists(CHROMA_PATH):
#         shutil.rmtree(CHROMA_PATH)
#
#     # Create a new DB from the documents.
#     db = Chroma.from_documents(
#         chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
#     )
#     db.persist()
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
#
#
# if __name__ == "__main__":
#     main()
#
#     chroma_client = chromadb.EphemeralClient()
#     chroma_collection = chroma_client.create_collection("diary_app")
#     vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
#     storage_context = StorageContext.from_defaults(vector_store=vector_store)
#
#     index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model=OpenAIEmbedding())
#
#
# #https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent_with_query_engine/
#
#
# ### PDF ----------------------------------------
# import os
# from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
# from llama_index.readers.file import PDFReader
#
# from dotenv import load_dotenv
# import openai
# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')
#
# def get_index(data, index_name):
#     index = None
#     if not os.path.exists(index_name):
#         print("building index", index_name)
#         index = VectorStoreIndex.from_documents(data, show_progress=True)
#         index.storage_context.persist(persist_dir=index_name)
#     else:
#         index = load_index_from_storage(
#             StorageContext.from_defaults(persist_dir=index_name)
#         )
#
#     return index
#
# #if __name__ == '__main__':
# path = os.path.join("data\joy", "joy_diary.pdf")
# diary_pdf = PDFReader().load_data(path)
# diary_index = get_index(diary_pdf, "diary")
# diary_engine = diary_index.as_query_engine()
#
# python -m streamlit run notebooks/investiment_app.py
# https://www.youtube.com/watch?v=dXxQ0LR-3
#
# https://discuss.streamlit.io/t/display-pdf-in-streamlit/62274
# https://pypi.org/project/streamlit-pdf-viewer/
#
#
# def get_emotions_from_text(text, suffix, filter=True):
#     emotions = te.get_emotion(text)
#     emotions = pd.DataFrame(emotions, index=[0])
#     if filter:
#         emotions[f'{suffix}'] = emotions.idxmax(axis=1)
#         emotions = emotions[f'{suffix}']
#         return emotions
#     else:
#         emotions[f'main_emotion'] = emotions.idxmax(axis=1)
#         emotions.columns = [(x + f'_{suffix}').lower() for x in list(emotions.columns)]
#         return emotions

#https://www.youtube.com/watch?v=I20Bli4JOEQ

