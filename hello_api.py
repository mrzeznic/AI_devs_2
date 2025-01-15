import json
import requests

try:
    with open('secrets.json','r') as file:
        data = json.load(file)
    api_key = data['api_key']
except json.JSONDecodeError:
    print('Could not decode JSON file.')
except FileNotFoundError:
    print('File not found.')

url = "https://tasks.aidevs.pl/token/helloapi"
payload = {"apikey"}