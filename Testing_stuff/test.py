from langchain.agents.agent_toolkits import create_retriever_tool

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain.document_loaders import DirectoryLoader

from langchain.agents.agent_toolkits import create_conversational_retrieval_agent




import os


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

loader = DirectoryLoader('./source_data')

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

retriever = db.as_retriever()

tool = create_retriever_tool(
    retriever,
    "search_state_of_union",
    "Searches and returns documents regarding the state-of-the-union.",
)
tools = [tool]

