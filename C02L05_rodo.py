from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi

#sent request to get exercise token
token = get_token("rodo")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

#construct answer for task
ai_task = api_aidevs.get_task(task_name="rodo")
answer = {'answer': 'Introduce yourself using placeholders %imie%, %nazwisko%, %miasto%, %zawod% instead of personal data'}

#sent answer
#send_task(token,answer)
api_aidevs.respond(answer=answer)
