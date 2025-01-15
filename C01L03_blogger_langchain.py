import json
import requests
import os
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from operator import itemgetter

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file = os.path.join(current_dir, 'secrets.json')

api_key = None
#Get API keys
try:
    with open(secrets_file,'r') as file:
        data = json.load(file)
        api_key = data['api_key']
        open_api_key = data['open_api_key']
        if api_key is None:
            raise ValueError("API key not found in secrets.json")
except json.JSONDecodeError:
    print("Could not decode JSON file!")
except FileNotFoundError:
    print("File not found!")
except ValueError as e:
    print(e)

#Send request for task
url = "https://tasks.aidevs.pl/token/blogger"
payload = {"apikey" : api_key}

response = requests.post(url, json = payload)
data = response.json()
print("Response data:{}".format(data))

if data ['code'] == 0:
    token = data['token']
    print("token:{}".format(data['msg']))
else:
    print("token:{}".format(data['msg']))

url = f"https://tasks.aidevs.pl/task/{token}"

response = requests.get(url)
data = response.json()

model = ChatOpenAI(api_key=open_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś Robertem Makłowiczem. Opisz poszczególne etapy przygotowania pizzy Margherity",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("user","{input}"),
    ]
)
memory = ConversationBufferMemory(return_messages=True)

chain = (
    RunnablePassthrough.assign(
        history = RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
)

answer = []
for chapter in data["blog"]:
    inputs = {"input": chapter}
    response = chain.invoke(inputs)
    memory.save_context(inputs, {"output": response.content})
    answer.append(response.content)
    print("# "+ chapter)
    print(response.content)
    
#print(answer)

#sent answer
url = f"https://tasks.aidevs.pl/answer/{token}"

payload = {"answer" : answer}

response = requests.post(url, json = payload)
data = response.json()

if data ['code'] == 0:
    print("Answer:{}".format(data['msg']))
else:
    print("Answer:{}".format(data['msg']))
