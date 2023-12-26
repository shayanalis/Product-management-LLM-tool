COURSE_SPR_FILENAME = './SPRs/0_spr_all_data_files.txt'
MODEL_NAME = 'gpt-4-1106-preview'
# gpt-4-1106-preview


# Controlling the parameters of the retrieval
## RETRIEVER_SEARCH_DEPTH * chunk_size => characters per DB query 
## 1 token  ~= 4 characters
## so it 500*4/4 -> 500 tokens added in the context for GPT query

RETRIEVER_SEARCH_DEPTH = 5
TOP_K_SEARCH_RESULTS = 7
CHUNK_SIZE = 800 
CHUNK_OVERLAP = 200

VECTORSTORE_DIRECTORY_NAME = 'vectorstore'