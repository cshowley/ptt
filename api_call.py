import requests
# import argparse
import os
import json
from dotenv import load_dotenv

load_dotenv()


import requests


# parser = argparse.ArgumentParser()
# parser.add_argument('query', default=None)
# parser.add_argument('document', default=None)
# parser.add_argument('model', default='venice-uncensored')
# args = parser.parse_args()

url = "https://api.venice.ai/api/v1/chat/completions"

# query = args.query
# if args.document is not None:
#     with open(args.document, 'r') as f:
#         doc = f.read()
#     query += f'\n\n{doc}'

def make_request(query, model='venice-uncensored'):
    payload = {
        "model": model,
        "frequency_penalty": 0,
        "n": 1,
        "presence_penalty": 0,
        "temperature": 0.3,
        "top_p": 1,
        "messages": [
            {
                "role": 'user',
                "content": query
            }
        ],
        "venice_parameters": {
            "include_venice_system_prompt": True,
            "enable_web_search": "auto"
            },
    }
    headers = {
        "Authorization": f"Bearer {os.environ['VENICE_API_KEY']}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()['choices'][0]['message']['content']
