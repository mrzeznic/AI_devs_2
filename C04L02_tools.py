from ai_devs_tasks import get_task,get_token, send_task, get_api_key, get_open_api_key
from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
from langchain_core.pydantic_v1 import BaseModel, Field
import time


#sent request to get exercise token
token = get_token("tools")

#send request to get task content
task = get_task(token, True)
print(task)
#send request to get api key
api_key = get_api_key()
open_api_key = get_open_api_key()

#call new instance
api_openai = OpenAIApi()
api_aidevs = AiDevsApi()

ai_task = api_aidevs.get_task(task_name="tools")

#construct answer for task
class ToDo(BaseModel):
    """Add note or task to todo list"""

    desc: str = Field(..., description="Description of the task")

    def to_json(self):
        return {"tool": "ToDo", "desc": self.desc}


class Calendar(BaseModel):
    """Add event to the calendar if the day is given"""

    desc: str = Field(..., description="Short description of the event")
    date: str = Field(..., description=f'Today is {time.strftime("%A %Y-%m-%d")}, '
                                       f'get the date user provided in YYYY-MM-DD format. Only future dates')

    def to_json(self):
        return {"tool": "Calendar", "desc": self.desc, "date": self.date}


def tools():
    api_aidevs = AiDevsApi()
    api_openai = OpenAIApi()

    task = api_aidevs.get_task(task_name="tools")
    question = task["question"]

    matched_function = api_openai.function_calling(question, [ToDo, Calendar])
    if len(matched_function) == 0:
        print("[ERROR] Something went wrong none of functions matched (did you pass proper function list?)")
        exit(15)
    elif len(matched_function) > 1:
        print("[ERROR] Possibly invalid prompt, more than one function matched")
        exit(15)

    answer = matched_function[0].to_json()
    api_aidevs.respond(answer={'answer': answer})
    return answer
tools()
#print(answer)
#sent answer
#send_task(token,search)
#api_aidevs.respond(answer=tools())
