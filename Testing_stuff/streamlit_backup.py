import openai
import streamlit as st
# print(st)


import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain #RetrievalQA
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
# import pdfminer
# import pdfminer.high_level
# from pdfminer.high_level import extract_text


# import pdfminer.six
# print(dir(pdfminer))



# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  # print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  loader = DirectoryLoader("data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

# while True:
#   if not query:
#     # query = 'For the actor "Passenger" and the "job to be done statement":"Find seat number quickly" can you provide feedback?' # input("Prompt: ")
#   # if query in ['quit', 'q', 'exit']:
#     sys.exit()
#   result = chain({"question": query, "chat_history": chat_history})
#   print(result['answer'])

#   chat_history.append((query, result['answer']))
#   query = None

# ConversationalRetrievalChain.from_orm

chain = ConversationalRetrievalChain.from_llm(
  llm= ChatOpenAI(model="gpt-4", temperature=0), # OpenAI(temperature=0)
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

# myllm = ChatOpenAI(model="gpt-4", temperature=0.1)

# with get_openai_callback() as cb:
#   myllm('what is a dog')

st.title("Product Management Essentials - Chat GPT tool") 
system_prompt = '''
you are a helpful assistant for the course called Product Management essentials for engineers.
You are given search results from the course material and you have to understand the material and the user question to answer questions.
If you are given conflicting information try to pick only the most relevant and specific information and then try to answer.
If you are not certain about the correct answer, then say that you don't have the ability to answer this question.
'''

# {"role": self.role,"content": self.content}
chat_history = []
result =  chain({"question": system_prompt, "chat_history": chat_history})
# chat_history.append((, result['answer']))

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I'm here to help you with your course!"}]
    # st.session_state["messages"] = [{"role": "assistant", "content": "I know about the outcomes tool, acronyms, and Kristen's paper on maternal depression"}]

for msg in st.session_state.messages:
    # print('msg',msg)
    # print('msg["content"]',msg["content"])
    st.chat_message(msg["role"]).write(msg["content"])
    # print(chain)


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # print(chain)

    query = prompt

    # print(chat_history)
    # print(prompt)


    with get_openai_callback() as cb:
      print('chat hist',chat_history)

      result = chain({"question": prompt, "chat_history": chat_history})
      # result = chain({"question": prompt})
      print('result',result['answer'])

      print('result',result['answer'])
      print('st.session_state',st.session_state)

      chat_history = chat_history.append((query, result['answer']))
      print(cb)

    response = result['answer'].strip()
    msg = {
        "content": response,
        "role": "assistant"
    }
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])

    # openai.api_key = openai_api_key
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.chat_message("user").write(prompt)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # print('response',response)

    # msg = response.choices[0].message
    # print('msg',msg)

    # st.session_state.messages.append(msg)
    # st.chat_message("assistant").write(msg.content)