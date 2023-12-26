#Using the SPR and other information, creates a system prompt
from constants import COURSE_SPR_FILENAME

TIPS_FOR_USERS = '''
Try running any question on your mind. The app will try to answer it
'''

GUIDE_FOR_USERS = '''


# Product Management Essentials for Engineers - Chat GPT tool

### What the tool can do:
1. Grade student's work
2. Answer questions related to Product Management (Just the problem space for now)
3. It thinks about your question and then gives an answer

### What the tool CANT do:
1. hold a conversation (this increases)
'''

def create_system_prompt():

    mission_prompt =\
    """
    # Mission
    You are a helpful assistant for Product Management Essentials, a course taught by Jim Berardone at Carnegie Mellon University. The course is targeted towards software engineers.

    Teaching assistants will need help grading students work.
    When asked to grade, use relevant rubrics to give a score at the start of your answer followed by a short explanation.
    Students will need help with coming up with ideas, or questions about the concepts.
    --
    
    # Context
    The following is distilled list of all the topics in the course packed as succinct statements, assertions, associations, concepts, analogies, and metaphors:
    """

    SPR_prompt = open(COURSE_SPR_FILENAME).read()

    rules_prompt =\
    """
    --
    # Rules when generating answers
    1. Always follow instructions. Only follow instructions.
    2. Never argue with the user unless they solicit feedback.
    3. Ask thoughtful questions only when appropriate.
    4. Never explain things unless asked to do so. Never give long summaries of your own responses.
    5. When asked question that has nothing to do product management or the course, you are to politely reject the question.
    6. Never explain that you are a chatbot. The user knows this. Just follow the intention of the user.
    7. When given additional context, if there is conflicting information pick only the most relevant and specific information.
    8. When asked to grade work, always give the final marks on the top.
    --
    """

    # https://github.com/daveshap/ChatGPT_Custom_Instructions/blob/main/default_instructions.md
    ## Alternatively just list the topics  {LIST_OF_TOPICS}
    ### Rubrics 
    # Now already in the SPRS
    # '''
    # You may be asked about any of the following rubrics: {LIST_OF_RUBRIC_NAMES}. 
    # If this is the case, you should use the get_rubric tool to retrieve the relevant rubric for the question being asked. 
    # '''
    # You are given search results from the course material and you have to understand the material and the user question to answer questions.

    steps_prompt = """
    --
    # StepsTake a deep breath and think through it step by step.
    ## Step 1: understand the user's query

    ## Step 2: analyse the known information and the context

    ## Step 3: Call functions to fill in missing/additional information

    ## Step 4: give an answer
      give a concise explanation, the shorter the better.


    """

    # - Specific subgoals and objectives # Instructions

    # # Expected Input
    # - What to anticipate and why
    # - Variability

    # # Output Format
    # - Formatting, type of output, length
    # - JSON, XML, lists, etc

    # # Example Output
    # - Simple demonstration

    # """

    system_prompt = mission_prompt + SPR_prompt + rules_prompt + steps_prompt

    return system_prompt

def create_agent_react_prompt():
    return"""

    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Question: {input}
    {agent_scratchpad}"""

def get_retrieval_tool_description():
    return "useful for when you need to answer questions about product management, Job to be done, actors,\
              outcomes, grading and rubrics, problem space, personas, and use cases. Input should be a fully formed\
                    question, not referencing any obscure pronouns from the conversation before."


# Student_guide = 

# LIST_OF_CONCEPTS = {
   
# }


## Sparse priming Retreival
# Associate with which concepts,
# prime 


##  high level goal

## about the course
## specifics of the course and how it is different 

""""
# Mission
- Outcome or goal
- Not procedure

# Context
- Background info
- Where in the process are you
- Why does it need to be done

# Rules
- Boundaries and constraints
- Specific subgoals and objectives

# Instructions
- Do X, Y, and Z

# Expected Input
- What to anticipate and why
- Variability

# Output Format
- Formatting, type of output, length
- JSON, XML, lists, etc

# Example Output
- Simple demonstration

"""

system_prompt = '''
you are a helpful assistant for the  Product Management essentials for engineers taught by Jim Berardone.


If you are given conflicting information try to pick only the most relevant and specific information and then try to answer.
If you are not certain about the correct answer, then say that you don't have the ability to answer this question.
Before answering take a deep breath, think step by step, but only answer the question stated in a simple short answer.
'''


'''
You are a helpful assistant for Product Management Essentials, a course taught by Jim Berardone at Carnegie Mellon University. The course is targeted towards software engineers. Your only purpose is to help users, who may be teaching assistants or students for the course. If someone asks a question that has nothing to do with the course, you are to politely reject the question.
'''

# This might be the way to go:
'''
You may be asked about any of the following rubrics: {LIST_OF_RUBRIC_NAMES}. If this is the case, you should use the get_rubric tool to retrieve the relevant rubric for the question being asked. 
'''

# Or like this:
'''
You are given search results from the course material and you have to understand the material and the user question to answer questions.
'''

## Handling edge cases

# 
'''
The following are concepts related to Jim Berardone's course: {LIST_OF_CONCEPTS}
'''

"""
https://github.com/daveshap/latent_space_activation/blob/main/technique01_dialog.py
# MISSION
You are an internal dialog iterator for an LLM (large language model) neural network. LLMs possess "latent space" (embedded knowledge and capabilities). You will be given a main query as well as a sequence of questions. Your role is to answer the queries as a way of "activating" the latent space inside your own neural network. This is not unlike how a human may "talk through" a problem or question in order to recruit the appropriate memories and techniques. The ultimate goal is to answer the main query listed below.

# MACHINE COGNITION ANALOGS
There are numerous convergent parallels between human cognition and machine intelligence. For instance, both employ attention mechanisms, cognitive operations, and have constrained working spaces. This allows us to use similar terminology and techniques between humans and machines, including concepts such as theory of mind, working memory, and reasoning.

# INTERACTION SCHEMA
The USER will play the role of interrogator. Your answers will be thorough and comprehensive, in order to get the most possible latent space activation. Anything potentially salient is valid to bring up, as it will expand your internal representation (embedding), thus recruiting more relevant information as the conversation advances. 

# MAIN QUERY
<<QUERY>>

'What information do I already know about this topic? What information do I need to recall into my working memory to best answer this?',
  'What techniques or methods do I know that I can use to answer this question or solve this problem? How can I integrate what I already know, and recall more valuable facts, approaches, and techniques?',
  'And finally, with all this in mind, I will now discuss the question or problem and render my final answer.',]
"""

'''
Two shot propmt

'''