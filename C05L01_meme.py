from AiDevsApi import AiDevsApi
import os
import requests


def meme():
    api_aidevs = AiDevsApi()

    task = api_aidevs.get_task(task_name="meme")
    img_url = task['image']
    text = task['text']

    json = {
        "template": "hairy-griffins-shrink-hourly-1221",
        "data": {
            "text.text": text,
            "pic.image": img_url
        }
    }

    r = requests.post('https://api.renderform.io/api/v2/render?output=json',
                      headers={'X-API-Key': os.environ['RENDERFORM_API_KEY']},
                      json=json)
    if r.status_code != 200:
        print(f"[ERROR] Failed to generate a meme, status code {r.status_code}")
        print(f"[ERROR] {r.content}")
        exit(19)
    print(r.content)
    api_aidevs.respond(answer={"answer": r.json()["href"]})
    
meme()