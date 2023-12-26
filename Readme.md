
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
Create the SPRs and the vector database
`Run the script setup.py`

This will update the folder SPRs and remove any existing files.
Note that SPRs should be created by the LLM for best recall
Change data folder to influence changes in the SPR files

## creates a new vector database:
setup will run the file `vectorestore.py > create_vectorstore()`
Persist = False creates a new database from the source data folder

read api documentation:
https://platform.openai.com/docs/introduction


## Step 4: Run streamlit.py
Replace the open ai api keys in both files liquid_text.ipynb and streamlit.py

