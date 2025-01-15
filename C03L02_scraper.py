from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

#sent request to get exercise token
token = get_token("scraper")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="scraper")

#construct answer for task
system = ai_task['msg']
resource_url = ai_task['input']
prompt = ai_task['question']


def fetch_file_as_firefox(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
    }
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    return response.text


# Example usage
context = fetch_file_as_firefox(resource_url)
system = f"""
    Based on context below, respond the the user question. Respond ultra-briefly.

    {system}

    context```
    {context}
    ```
    """

response = api_openai.chat(prompt = prompt,system = system)
answer = {'answer': response}

#sent answer
#send_task(token,answer)
api_aidevs.respond(answer=answer)
