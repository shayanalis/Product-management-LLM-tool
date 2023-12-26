import openai
import streamlit as st
import os
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage


## for Agent
import re
from typing import Union
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.schema import AgentAction, AgentFinish
from langchain.utilities import SerpAPIWrapper
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.agents import (
    AgentExecutor,
    AgentOutputParser,
    LLMSingleActionAgent,
    Tool,
)
from langchain.agents import AgentType, Tool, initialize_agent


## for streaming
from langchain.agents import load_tools
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.callbacks.streamlit import StreamlitCallbackHandler


## helpers
import random

from system_prompt\
  import create_system_prompt, GUIDE_FOR_USERS, TIPS_FOR_USERS, create_agent_react_prompt, get_retrieval_tool_description
from constants import RETRIEVER_SEARCH_DEPTH, VECTORSTORE_DIRECTORY_NAME, TOP_K_SEARCH_RESULTS, MODEL_NAME
from my_secrets import OPENAI_API_KEY
from helpers import CustomOutputParser, CustomPromptTemplate


with st.sidebar:
    st.write(GUIDE_FOR_USERS)

if "openai_api_key" not in st.session_state:
    
    print("Make sure you run setup.py with updated source data, and SPRs")
  
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
      print("loading up vec database..\n")
      vectorstore = Chroma(persist_directory=VECTORSTORE_DIRECTORY_NAME, embedding_function=OpenAIEmbeddings())

    retriever=vectorstore.as_retriever(
     search_kwargs={"k": RETRIEVER_SEARCH_DEPTH, "top_k":TOP_K_SEARCH_RESULTS}, 
    #  search_type='mmr'
    # use mmr with minimum threshold
    # test against "Help me grade this students outcome: "DEsired outcome: average trip time, Actual outcome decreased trip time" 
    # with mmr it wasn't able to search for the rubric because the first result was desired outcome, and then no rubric in the others
    )

    chain = ConversationalRetrievalChain.from_llm(
      llm= ChatOpenAI(model=MODEL_NAME, temperature=0),
      retriever=retriever,
      verbose=True,
      # return_intermediate_steps=True
    )

    st.session_state['chain'] = chain

    llm=ChatOpenAI(model=MODEL_NAME, temperature=0,
                   streaming=True)

    retrieval_chain_tool = RetrievalQA.from_chain_type(
      llm=llm,
      chain_type="stuff",
      retriever=retriever,
      verbose=True,
    )

    tools = [
        Tool(
            name="Product Management Course Concept Search",
            func=retrieval_chain_tool.run,
            description=get_retrieval_tool_description()
        )
    ]

    def get_tools(query):
        # docs = retriever.get_relevant_documents(query)
        return tools

    template = create_system_prompt() + create_agent_react_prompt()

    # Set up a prompt template
    prompt = CustomPromptTemplate(
        template=template,
        tools_getter=get_tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"],
    )

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    llm_chain = LLMChain(
        llm=llm, 
        prompt=prompt,
        verbose=True
    )

    output_parser = CustomOutputParser()

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names,
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )
    
    st.session_state['agent_executor'] = agent_executor

# how do we give it a chat history?


# st.title("Product Management Essentials - Chat GPT tool") 

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I'm ready to help!"}]

if "chat_history" not in st.session_state:
    system_prompt = SystemMessage(content=create_system_prompt())
    st.session_state["chat_history"] = [
      system_prompt
    ]
expander = st.expander("Tips")
expander.write()
st.write()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.session_state.openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # with get_openai_callback() as cb: for prompt tokens and cost
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        agent_response = st.session_state.agent_executor({"input": prompt, "chat_history": st.session_state.chat_history}, callbacks = [st_callback])
        st.session_state.chat_history.append((agent_response['input'], agent_response['output']))

        # st.chat_message("debugger").write(cb)
        # st.session_state.messages.append({"role": "debugger", "content": cb})
        st.session_state.chat_history.append((agent_response['input'], agent_response['output']))

    response = agent_response['output'].strip()
    msg = {
        "content": response,
        "role": "assistant"
    }

    st.session_state.messages.append(msg)
    st.chat_message("assistant").markdown(msg['content'])