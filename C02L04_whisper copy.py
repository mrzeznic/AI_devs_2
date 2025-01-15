from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi

#sent request to get exercise token
token = get_token("whisper")

#send request to get task content
task = get_task(token, True)

#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

#construct answer for task
ai_task = api_aidevs.get_task(task_name="whisper")
words = task['msg'].split(' ')
links = [word for word in words if word.endswith('.mp3')]
transcription = api_openai.transcription(links[0])
answer = {'answer': transcription}


#sent answer
#send_task(token,answer)
api_aidevs.respond(answer=answer)
