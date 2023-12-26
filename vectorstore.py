# https://github.com/techleadhd/chatgpt-retrieval/blob/main/chatgpt.py

import os
import shutil
import openai
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
# from langchain.llms import OpenAI
# import pdfminer.high_level
# from pdfminer.high_level import extract_text
# import pdfminer
# import pdfminer.six
# print(dir(pdfminer))
from langchain.text_splitter import CharacterTextSplitter

from my_secrets import OPENAI_API_KEY
from constants import VECTORSTORE_DIRECTORY_NAME, CHUNK_OVERLAP, CHUNK_SIZE

def create_vectorstore():

  openai.api_key = OPENAI_API_KEY
  os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
  if os.path.exists(VECTORSTORE_DIRECTORY_NAME):
    print("Deleting current vector store:{}...\n".format(VECTORSTORE_DIRECTORY_NAME))
    shutil.rmtree(VECTORSTORE_DIRECTORY_NAME)

  print('creating new store')

  loader = DirectoryLoader('source_data')
  documents = loader.load()
  text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
  docs = text_splitter.split_documents(documents)

  embeddings = OpenAIEmbeddings()
  vectorstore = Chroma.from_documents(
      docs, embeddings, persist_directory=VECTORSTORE_DIRECTORY_NAME
  )

  print('Verifying vector store against: "grade the use cases"')
  for res in vectorstore.similarity_search('grade the use cases'):
    print (res,'\n')