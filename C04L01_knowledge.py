from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

#sent request to get exercise token
token = get_token("knowledge")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="knowledge")

#construct answer for task
task = api_aidevs.get_task(task_name="knowledge")
question = task["question"]

system = """
Skategoryzuj zapytanie użytkownika bazując na jego treści. Użyj tylko jednej z kategorii: waluta, populacja, inne

Przykłady```
U: Czego stolicą jest Rzym?
A: inne

U: Jaki jest kurs USD/PLN?
A: waluta

U: Jaka jest populacja Australii?
A: populacja
```
"""
category = api_openai.chat(prompt=question, system=system)

if category == "inne":
    system = "Odpowiadaj zwięźle na pytania użytkownika"
    response = api_openai.chat(prompt=question, system=system)
    api_aidevs.respond(answer={'answer': response})
elif category == "waluta":
    system = """
Podaj kod waluty i nic więcej

Przykłady```
U: Po ile stoi euro?
A: EUR

U: Ile wart dolar?
A: USD

U: A hrywna?
A: UAH
```
"""
    currency_code = api_openai.chat(prompt=question, system=system)
    table_a = requests.get("http://api.nbp.pl/api/exchangerates/tables/A").json()
    for rate in table_a[0]["rates"]:
        if rate["code"].upper() == currency_code.upper():
            api_aidevs.respond(answer={'answer': rate["mid"]})
            exit(0)
    print("[ERROR] Currency code not found in the table A, possible invalid chat response")
    print(f"[ERROR] Expected currency code (ex. USD|EUR) received \"{currency_code}\"")
    exit(15)
elif category == "populacja":
    system = """
Podaj pełną nazwę kraju w języku angielskim i nic więcej

Przykłady```
U: Ile mieszkańców mają Czechy?
A: Czech Republic

U: What is the population of USA?
A: United States of America

U: Ile ludzi mieszka w Iraku?
A: Republic of Iraq```

Bez komentarzy.
"""
    country_name = api_openai.chat(prompt=question, system=system)
    populations = requests.get("https://restcountries.com/v3.1/all?fields=name,population").json()
    for population in populations:
        if population['name']['common'].lower() == country_name.lower() or \
        population['name']['official'].lower() == country_name.lower():
            api_aidevs.respond(answer={'answer': population["population"]})
            exit(0)
    print("[ERROR] Country name not found in the populations list, possible invalid chat response")
    print(f"[ERROR] Expected official country name (ex. \"United States of America\"|\"Czech Republic\") received \"{country_name}\"")
    exit(15)
else:
    print("[ERROR] Something went wrong, unexpected category in the chat response")
    print(f"[ERROR] Expected (kraj|waluta|inne) received \"{category}\"")
    exit(14)


#print(answer)
#sent answer
#send_task(token,search)
#api_aidevs.respond(answer=search)
