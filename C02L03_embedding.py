from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from itertools import groupby
from typing import List
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi

#sent request to get exercise token
token = get_token("embedding")

#send request to get task content
task = get_task(token, True)

#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new OpenAI instance
client = ChatOpenAI(api_key=open_api_key)

#construct answer for task
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="embedding")
embeddings_array = api_openai.embeddings(content="Hawaiian pizza")[0]['embedding']
answer = {"answer": embeddings_array}

#sent answer
#send_task(token,answer)
api_aidevs.respond(answer=answer)
