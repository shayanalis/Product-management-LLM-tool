import openai
import streamlit as st
import os
from langchain.chains import ConversationalRetrievalChain #RetrievalQA
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage

import random

from system_prompt\
  import create_system_prompt, GUIDE_FOR_USERS
from constants import RETRIEVER_SEARCH_DEPTH, VECTORSTORE_DIRECTORY_NAME
from my_secrets import OPENAI_API_KEY
MODEL = "gpt-4"

print("Make sure you run setup.py with updated source data, and SPRs")

if "openai_api_key" not in st.session_state:
    # random_number = random.random()
    # print(random_number)
    # if random_number <= 1:
    #   openai_api_key = shayan_key
    #   print('Setting key shayan')
      
    # else: 
    #   openai_api_key = jim_key
    #   print('Setting key jim')
    openai.api_key = OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    st.session_state['openai_api_key'] = OPENAI_API_KEY

if os.path.exists(VECTORSTORE_DIRECTORY_NAME):
  # print("loading up vec database..\n")
  vectorstore = Chroma(persist_directory=VECTORSTORE_DIRECTORY_NAME, embedding_function=OpenAIEmbeddings())
  loader = DirectoryLoader("source_data/")
  index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":VECTORSTORE_DIRECTORY_NAME}).from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm= ChatOpenAI(model=MODEL, temperature=0),
  retriever=index.vectorstore.as_retriever(
     search_kwargs={"k": RETRIEVER_SEARCH_DEPTH}, 
     search_type='mmr'
    ),
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
      # print(result)
      st.session_state.chat_history.append((result['question'], result['answer']))

      print(cb)
      st.chat_message("debugger").write(cb)
      st.session_state.messages.append({"role": "debugger", "content": cb})

    response = result['answer'].strip()
    msg = {
        "content": response,
        "role": "assistant"
    }
    
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])