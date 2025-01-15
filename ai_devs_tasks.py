import json
import requests
import os

#api_key = None
#Get API keys
def get_api_key():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(current_dir, 'secrets.json')
    try:
        with open(secrets_file,'r') as file:
            data = json.load(file)
            api_key = data['api_key']
            if api_key is None:
                raise ValueError("API key not found in secrets.json")
    except json.JSONDecodeError:
        print("Could not decode JSON file!")
    except FileNotFoundError:
        print("File not found!")
    except ValueError as e:
        print(e)
    #data = {"apikey": os.getenv("AI_DEVS_CODE")}
    return api_key

api_key = get_api_key()

def get_open_api_key():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(current_dir, 'secrets.json')
    try:
        with open(secrets_file,'r') as file:
            data = json.load(file)
            open_api_key = data['open_api_key']
            if open_api_key is None:
                raise ValueError("API key not found in secrets.json")
    except json.JSONDecodeError:
        print("Could not decode JSON file!")
    except FileNotFoundError:
        print("File not found!")
    except ValueError as e:
        print(e)
    #data = {"apikey": os.getenv("AI_DEVS_CODE")}
    return open_api_key

open_api_key = get_open_api_key()

#Send request for task
def get_token(task):
    url = "https://tasks.aidevs.pl/token/" + task
    payload = {"apikey" : api_key}
    response = requests.post(url, json = payload)
    data = response.json()
    #print("Response data:{}".format(data))
    if data ['code'] == 0:
        token = data['token']
        print("Token status: {}{}{}, for token: {}".format('\033[92m',data['msg'],'\033[0m',data['token']))
    else:
        print("Token status: {}{}{}, for token: {}".format('\033[91m',data['msg'],'\033[0m',data['token']))
    return data.get("token")

#new_token = get_token("blogger")

def get_task(token, debug = False):
    url = f"https://tasks.aidevs.pl/task/{token}"
    response = requests.get(url)
    data = response.json()
    if data ['code'] == 0:
        #token = data['token']
        print("Task: {}".format(data['msg']))
    else:
        print("Task: {}".format(data['msg']))
    #return data.get("token")
    return data

#new_task = get_task(new_token,True)

#sent answer
def send_task(token,answer):
    url = f"https://tasks.aidevs.pl/answer/{token}"
    payload = {"answer" : answer}
    response = requests.post(url, json = payload)
    data = response.json()
    if data ['code'] == 0:
        print("Answer: {}{}{}".format('\033[92m',data['msg'],'\033[0m'))
    else:
        print("Answer: {}{}{}".format('\033[91m',data['msg'],'\033[0m'))
    return data

#new_answer = send_task(new_token,"Answer")
