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


def read_history(chat_path):
    # Load full chat history
    if chat_path:
        if os.path.exists(chat_path):
            with open(chat_path, "r", encoding="utf-8") as f:
                chat = json.load(f)
        else:
            chat = []
            if chat_path:
                open(chat_path, "w").close()
    else:
        chat = []
    return chat


def write_history(chat, chat_path, response_message):
    # Append LLM response to chat history
    chat.append({"role": "assistant", "content": response_message})
    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=4)


def make_request(query, model='venice-uncensored', chat_history=None):
    messages = read_history(chat_history)
    messages.append({"role": "user", "content": query})
    payload = {
        "model": model,
        "frequency_penalty": 0,
        "n": 1,
        "presence_penalty": 0,
        "temperature": 0.3,
        "top_p": 1,
        "messages": messages,
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
    response_message = response.json()['choices'][0]['message']['content']
    if chat_history:
        write_history(messages, chat_history, response_message)
    return response_message
