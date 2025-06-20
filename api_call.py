import requests

import os
from dotenv import load_dotenv

load_dotenv()


import requests

url = "https://api.venice.ai/api/v1/chat/completions"

payload = {
    "model": "venice-uncensored",
    "frequency_penalty": 0,
    "n": 1,
    "presence_penalty": 0,
    "temperature": 0.3,
    "top_p": 1,
    "messages": [
        {
            "role": 'user',
            "content": "hello"
        }
    ],
    "venice_parameters": {"include_venice_system_prompt": False},
}
headers = {
    "Authorization": f"Bearer {os.environ['VENICE_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
