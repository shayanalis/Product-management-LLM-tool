# https://github.com/daveshap/SparsePrimingRepresentations
import os
import openai
from openai import OpenAI
from my_secrets import OPENAI_API_KEY

def create_sprs():
  openai.api_key = OPENAI_API_KEY
  os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

  MODEL_NAME = "gpt-4-1106-preview"

  directory = './source_data'
  save_to ='./SPRs/0_spr_all_data_files.txt'
  print('loading Files... from directory: {}'.format(directory))
  print('')

  client = OpenAI()

  content = ''
  for filename in sorted(os.listdir(directory)):
    print(filename)
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
      content = content + open(file_path).read()

  # print(content)

  print('')
  print('Sending long form content to LLM...')
  print('Waiting for response...')

  SPR_encoder_prompt = '''

  # MISSION
  You are a Sparse Priming Representation (SPR) writer. An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation Large Language Models (LLMs). You will be given information by the USER which you are to render as an SPR.

  # THEORY
  LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind. These are called latent abilities and latent content, collectively referred to as latent space. The latent space of a LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

  # METHODOLOGY
  Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human.

  The input you will get is from a Product management course, all the topics are in the sequence that they are taught to the students.

  The distilled output should be roughly 6% of the input length, don't make it too condensed.

  Take a deep breath before writing the SPR
  '''

  response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.0,
    messages=[
      {"role": "system", "content":SPR_encoder_prompt},
      {"role": "user", "content": "Can you create an SPR for me?"},
      {"role": "assistant", "content": "yes"},
      {"role": "user", "content": content}
    ]
  )
  print('')

  compressed = response.choices[0].message.content
  with open(save_to,'w') as file:
      file.write(compressed)
  print('')
  print('--------------------------------')
  print(compressed)
  print('--------------------------------')
  print('')
  print('')
  print('overwriting to file:{}'.format(MODEL_NAME,save_to))
  print('')
  print('content length:{}'.format(len(compressed)), 'originally:{}'.format(len(content)),'compressed to:{} % goal: 6%'.format(int(len(compressed)*100/len(content))))
