from ai_devs_tasks import get_task,get_token, send_task, get_api_key
from openai import OpenAI

#sent request to get exercise token
token = get_token("blogger")

#send request to get task content
task = get_task(token, True)

#send request to get api key
api_key, open_api_key = get_api_key()

#call new OpenAI instance
client = OpenAI(api_key=open_api_key)

#construct answer for task
answer = []
for chapter in task["blog"]:
    m = [
        {
            "role" : "system",
            "content" : "Jesteś Robertem Makłowiczem. Opisz poszczególne etapy przygotowania pizzy Margherity"
        }
    ]
    for a in answer:
        m.append({"role":"user","content":a[0]})
        m.append({"role":"assistant","content":a[1]})
    m.append(
        {"role":"user","content":chapter}
        )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=m
    )
    #print("# "+ chapter)
    #print(response.choices[0].message.content)
    answer.append(response.choices[0].message.content)

#sent answer
send_task(token,answer)
