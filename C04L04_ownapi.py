from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import threading
from time import sleep
import os
from flask import Flask, request
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pyngrok import ngrok


#sent request to get exercise token
token = get_token("ownapi")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="ownapi")

#construct answer for task

openai_client = ChatOpenAI(model="gpt-4",openai_api_key=open_api_key, temperature=0)
app = Flask(__name__)
##llm = ChatOpenAI(model='gpt-3.5-turbo', )


def ask_gpt(question):
    answer = openai_client.invoke(
        [HumanMessage(
            content=[
                {"type": "text", "text": question},
            ])]
    )

    return answer.content


@app.route('/', methods=['POST'])
def api():
    question = request.json['question']
    answer = ask_gpt(question)

    print(f"{question}: {answer}")

    response = {
        "reply": ask_gpt(question),
    }

    return response


def start_ngrok():
    connection = ngrok.connect(addr="127.0.0.1:5000")
    public_url = connection.public_url
    print(" * ngrok URL: " + public_url + " *")
    return public_url


def send_api_url_with_delay(delay, public_url):
    def send_api_url(public_url: str):
        ##api_aidevs.send_answer(token, public_url, debug=True)
        ##api_aidevs.respond(answer=public_url)
        send_task(token,public_url)

    sleep(delay)  # Delay execution for a specified number of seconds
    send_api_url(public_url)  # Call the function with the provided arguments


if __name__ == '__main__':
    public_api_url = start_ngrok()

    timer = threading.Thread(target=send_api_url_with_delay, args=(4, public_api_url))  # Set a delay of 5 seconds
    timer.start()

    app.run()
    
#sent answer
#send_task(token,answer)
#api_aidevs.respond(answer=answer)
