import openai
import streamlit as st
import os
import sys
from langchain.chains import ConversationalRetrievalChain #RetrievalQA
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage

import random

from system_prompt\
  import create_system_prompt, GUIDE_FOR_USERS
from constants import RETRIEVER_SEARCH_DEPTH
from my_secrets import OPENAI_API_KEY1

MODEL = "gpt-4-1106-preview"

# gpt-4-1106-preview

if "openai_api_key" not in st.session_state:
    # random_number = random.random()
    # print(random_number)
    # if random_number <= 1:
    #   openai_api_key = shayan_key
    #   print('Setting key shayan')
      
    # else: 
    #   openai_api_key = jim_key
    #   print('Setting key jim')
    openai.api_key = OPENAI_API_KEY1
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1
    st.session_state['openai_api_key'] = OPENAI_API_KEY1

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("loading up vec database..\n")
  ## added key variable to OpenAIEmbeddings(key=
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)

chain = ConversationalRetrievalChain.from_llm(
  llm= ChatOpenAI(model=MODEL, temperature=0), # OpenAI(temperature=0)
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_SEARCH_DEPTH},mmr=True),
  verbose=True,
  # return_intermediate_steps=True
)

st.title("Product Management Essentials - Chat GPT tool") 

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": GUIDE_FOR_USERS}]

if "chat_history" not in st.session_state:
    system_prompt = SystemMessage(content=create_system_prompt())
    st.session_state["chat_history"] = [
      system_prompt
    ]

st.write()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.session_state.openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with get_openai_callback() as cb:
      result = chain({"question": prompt, "chat_history": st.session_state.chat_history})
      print(result)
      st.session_state.chat_history.append((result['question'], result['answer']))

      print(cb)

    response = result['answer'].strip()
    msg = {
        "content": response,
        "role": "assistant"
    }
    
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])