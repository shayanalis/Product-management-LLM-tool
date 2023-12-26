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

from my_secrets import OPENAI_API_KEY
from constants import VECTORSTORE_DIRECTORY_NAME

def create_vectorstore():

  openai.api_key = OPENAI_API_KEY
  os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
  if os.path.exists(VECTORSTORE_DIRECTORY_NAME):
    print("Deleting current vector store:{}...\n".format(VECTORSTORE_DIRECTORY_NAME))
    shutil.rmtree(VECTORSTORE_DIRECTORY_NAME)

  print('creating new store')
  vectorstore = Chroma(persist_directory=VECTORSTORE_DIRECTORY_NAME, embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)

  loader = DirectoryLoader("source_data/")
  index = VectorstoreIndexCreator().from_loaders([loader])

  print('Verifying vector store against: "rubric for jtbd"')
  for res in index.vectorstore.similarity_search('rubric for jtbd'):
    print (res,'\n')