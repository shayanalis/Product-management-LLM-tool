
## Setup
unfortunately I did not track all the other dependencies that were installed, 
you can open the file pip_list to check which package I had installed in my local env

Python version: 3.9.6

Pipeline:
## Step 1
Add data to each file based on the concepts.
Concepts are ordered to be SPR'ed, which makes a summary of the concepts in a way that utilizes the llm's training instead of relying on retrieval

Read more here: https://github.com/daveshap/SparsePrimingRepresentations/pulse

## Step 2
Create the SPRs
`Run the script CreateSPRs.py`

This will update the folder SPRs and remove any existing files.
Note that SPRs should be created by the LLM for best recall
Change data folder to influence changes in the SPR files


## Step 3:

## running on existing vector database:
There is already a vector database in the persist folder that can be used to query answers.
run `streamlit run streamlit.py` and it will open up a page on localhost with the webapp.

read api documentation:
https://platform.openai.com/docs/introduction


## creating new vector database:
run the file `create_vectorStore.py`
Persist = False creates a new database from the source data folder

## Step 4: Run streamlit.py
Replace the open ai api keys in both files liquid_text.ipynb and streamlit.py

