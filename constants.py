COURSE_SPR_FILENAME = './SPRs/0_spr_all_data_files.txt'
MODEL_NAME = 'gpt-4'


# Controlling the parameters of the retrieval
## RETRIEVER_SEARCH_DEPTH * chunk_size => characters per DB query 
## 1 token  ~= 4 characters
## so it 500*4/4 -> 500 tokens added in the context for GPT query

RETRIEVER_SEARCH_DEPTH = 4
TOP_K_SEARCH_RESULTS = 6
chunk_size = 500 
chunk_overlap = 20

VECTORSTORE_DIRECTORY_NAME = 'vectorstore'