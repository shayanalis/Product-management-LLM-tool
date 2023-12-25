import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
# import pdfminer
import pdfminer.high_level
from pdfminer.high_level import extract_text


# import pdfminer.six
# print(dir(pdfminer))


openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = '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'

# Enable to save to disk & reuse the model (for repeated queries on the same data)

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if os.path.exists("persist"):
  print("Warning: Overwriting persist directory. note this does not always work")
#   vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
#   index = VectorStoreIndexWrapper(vectorstore=vectorstore)

#loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
loader = DirectoryLoader("data/")

index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-4", temperature=0.1),# OpenAI(temperature=0), 
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)
