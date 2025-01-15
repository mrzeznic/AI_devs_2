import json
import requests
import os
from openai import OpenAI

# Get the directory of the currently executing script
current_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file = os.path.join(current_dir, 'secrets.json')

api_key = None


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
##print(api_key)
url = "https://tasks.aidevs.pl/token/moderation"
payload = {"apikey" : api_key}

response = requests.post(url, json = payload)
data = response.json()
##print("Response data:{}".format(data))

if data ['code'] == 0:
    token = data['token']
    print("token:{}".format(data['msg']))
else:
    print("token:{}".format(data['msg']))

url = f"https://tasks.aidevs.pl/task/{token}"

response = requests.get(url)
data = response.json()
'''
if data ['code'] == 0:
    sentences = data['input']
    print(print("sentences:{}".format(data['input'])))
else:
    print(print("sentences:{}".format(data['input'])))
'''
client = OpenAI(api_key=open_api_key)

sentences = data['input']
answer = []
# Iterate over each sentence separately
for sentence in sentences:
    print("Processing sentence:", sentence)  # Debugging statement
    try:
        response = client.moderations.create(input=sentence, model="text-moderation-latest")
        #print("Response:", response)  # Debugging statement
        # Append 1 if any of the results in the response are flagged, otherwise append 0
        answer.append(int(any(map(lambda x: x.flagged, response.results))))
    except Exception as e:
        print("Error processing sentence:", e)  # Debugging statement
        answer.append(0)  # Append 0 in case of error

print("Answer from moderation:{}".format(answer))

url = f"https://tasks.aidevs.pl/answer/{token}"

payload = {"answer" : answer}

response = requests.post(url, json = payload)
data = response.json()

if data ['code'] == 0:
    print("Answer:{}".format(data['msg']))
else:
    print("Answer:{}".format(data['msg']))