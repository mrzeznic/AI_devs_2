from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi

#sent request to get exercise token
token = get_token("whoami")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="whoami")

#construct answer for task
retries = 0
max_retries = 4
hints = []
while retries < max_retries:
    retries += 1
    api_aidevs.authorize(task_name="whoami")
    ai_task = api_aidevs.get_task()
    if ai_task['hint'] in hints:
        continue
    hints.append(ai_task['hint'])
    formatted_hints = '\n'.join('-{}' for _ in range(len(hints))).format(*hints)
    system = f"""
Korzystając z faktów dostarczonych przez użytkownika odpowiadam na pytanie kim była owa postać.
Jeśli nie mogę stwierdzić jednoznacznie kim była postać odpowiadam '...'
Moje odpowiedzi są bardzo zwięzłe, nie dodaję żadnych komentarzy. 

Przykład```
U: był wojownikiem
A: ...
```"""

prompt = f"Fakty o postaci:\n{formatted_hints}\n\nNazwa postaci, albo '...'"
print(prompt)
answer = api_openai.chat(prompt=prompt, system=system)
#print(answer)
#sent answer
send_task(token,answer)
#api_aidevs.respond(answer=answer)
