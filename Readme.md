# Product Management Retrieval Augment Generation System with agents
This tool is used to help students understand the course material and also product management faster by providing information and quick feedback on concepts and application of the concepts.
Teaching Assistants can use this tool to grade students' work making and also provide feedback.


## What it can do:
Answer queries such as:
1. "What is a Job to be done"
2. "Tell me if my job to be done is good?"
3. "what grade would I get on my outcomes..."

Grade stuff:
1. "For the Actor "Pilot" is "Onboarding Passengers" a good JTBD?"
2. "Can you grade this: Actor "Pilot" is "Onboarding Passengers" a good JTBD?"
3. "Help me grade this student's outcome: Desired outcome: Avg trip time, Actual outcome: decreased trip time"

Come up with new examples and ideas:
[Note: this is still in the experimental phase]
1. "Give me examples of JTBD's for the Actor Passenger."
2. "Give me examples of outcomes I should measure for..."
3. "Give me some use cases for..."

What it can't do:
1. It can't hold a conversation for now
2. It can't talk about concepts outside of the problem space section of the course

Intermediate steps 


## How it works

#### There are 4 components to this system:
1. **Openai API**: Used as a large language model (LLM).
3. **Agent**: Decision maker that has access to tools like Querying a vector database.
4. **RAG**: Retrieval-augmented generation with a Vector database - Think of this as a database that can do a semantic search.
5. **SPR**: [Sparse Priming Representations]([url](https://github.com/daveshap/SparsePrimingRepresentations/pulse)) - Think of this as a smart summary of course material that activates the LLM better.
6. **Streamlit**: the app front-end is made with Streamlit and is hosted on the Streamlit cloud for free (at least until they let us).

#### Step by Step process:
**Step 0:** Before a user asks a question the LLM is given a few hundred words of SPR of the course material. The LLM now understands an overview of the course material in a condensed form.

**Step 1:** When a user asks a question, The agent gets the question and uses the LLM to decide whether it can answer the question or if it needs more information. 

**Step 2:** If the agent decides that it needs to look up information on, say, "the definition of JTBD". It will then request the RAG vector database and find relevant information. This usually searches for the top 4-5 semantically related chunks of text.

**Step 3:** Based on this information the Agent then "thinks", about what to do next. It might decide to look for more information or construct a final answer for the user.

**Step 4:** After Constructing the final answer the Agent then replies to the user.

## Future work:
Test cases: Adding test cases for prompts and answers is important because changes in prompts can cause regressions.
Improved Agent prompting: Agents also use prompts to decide what to do, They need good prompting to get the best out of the tool.


## How to Setup
use Python version: `3.9.6`
`pip install -r requirements.txt`

## Step 1
Add data to each file based on the concepts.
Concepts are ordered to be SPR'ed, which makes a summary of the concepts in a way that utilizes the llm's training instead of relying on retrieval
Read more here: 

## Step 2
Create the SPRs and the vector database
`Run the script setup.py`

This will update the folder SPRs and remove any existing files.
Note that SPRs should be created by the LLM for best recall
Change the data folder to influence changes in the SPR files

## creates a new vector database:
setup will run the file `vectorestore.py > create_vectorstore()`
Persist = False creates a new database from the source data folder

Read API documentation:
https://platform.openai.com/docs/introduction

## Step 4: Run streamlit.py
`streamlit run streamlit.py`

