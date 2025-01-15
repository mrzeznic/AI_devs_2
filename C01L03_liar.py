import json
import requests
import os
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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
url = "https://tasks.aidevs.pl/token/liar"
payload = {"apikey" : api_key}

response = requests.post(url, json = payload)
data = response.json()
print("Response data:{}".format(data))

if data ['code'] == 0:
    token = data['token']
    print("token:{}".format(data['msg']))
else:
    print("token:{}".format(data['msg']))

def get_answer(token, debug=False):
    url = f"https://tasks.aidevs.pl/task/{token}"
    response = requests.post(url, data = {"question": "What is capital of Poland?"})
    response.raise_for_status()
    if debug:
        print(response.json())
    return response.json()
    data = response.json()

answer = get_answer(token, True)

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=open_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                You are working a censor system.
                Check if this sentence is the answer to question about capital city of Poland.
                Answer only Yes or No.
            """,
        ),
        ("user","{input}"),
    ]
)
#print(prompt)

chain = prompt | model
response = chain.invoke({"input": answer["answer"]})
print(response.content)

#sent answer
url = f"https://tasks.aidevs.pl/answer/{token}"

payload = {"answer" : response.content}
#print(payload)

response = requests.post(url, json = payload)
data = response.json()

if data ['code'] == 0:
    print("Answer:{}".format(data['msg']))
else:
    print("Answer:{}".format(data['msg']))
