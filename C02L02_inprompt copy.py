from ai_devs_tasks import get_task,get_token, send_task, get_api_key
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from itertools import groupby
from typing import List

#sent request to get exercise token
token = get_token("inprompt")

#send request to get task content
task = get_task(token, True)

#send request to get api key
api_key, open_api_key = get_api_key()

#call new OpenAI instance
client = ChatOpenAI(api_key=open_api_key)

#construct answer for task
system_message = task['msg']
question = task['question']

sentences: List[str] = task['input']
grouped_sentences = {name: list(group) for name, group in groupby(sorted(sentences), key=lambda x: x.split()[0])}

get_name_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are name extractor. Extract names from sentences. Return only first name."),
    ("user", "{input}")
])

get_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "%s context###{database}###" % system_message),
    ("user", "{input}")
])

get_name_chain = get_name_prompt | client
get_answer_chain = get_answer_prompt | client

name = get_name_chain.invoke({"input": question}).content
response = get_answer_chain.invoke({"input": question, "database": grouped_sentences[name]})
answer = response.content

#sent answer
send_task(token,answer)
