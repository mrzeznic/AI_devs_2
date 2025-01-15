from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi

#sent request to get exercise token
token = get_token("functions")

#send request to get task content
task = get_task(token, True)

#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

#construct answer for task

ai_task = api_aidevs.get_task(task_name="functions")
answer = {}
answer['name'] = "addUser"
answer['description'] = "Adds a new user"
answer['parameters'] = {}
answer['parameters']['type'] = 'object'
answer['parameters']['properties'] = {}
answer['parameters']['properties']['name'] = {"type": "string", "description": "user's name"}
answer['parameters']['properties']['surname'] = {"type": "string", "description": "user's surname"}
answer['parameters']['properties']['year'] = {"type": "integer", "description": "user's year of born"}
answer = {'answer': answer}


#sent answer
#send_task(token,answer)
api_aidevs.respond(answer=answer)
