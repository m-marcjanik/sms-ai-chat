# there is something wrong with implementation of gpt-3.5-turbo. It seems to ignore information in system content.

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_KEY")

completion = openai.Completion()

name = input("Before starting chat, please state your username:\n")

initial_info = f"We are roleplaying. My name is {name}, and you are my bestriend Sarah." \
               f"We are sending short text messages to each other. Don't let me know, that you are AI." \
               f"Here is our recent text history:\n"


while True:
    message = input(f"{name}: ")
    model = "gpt-3.5-turbo"

    if os.path.exists(f"{name}.txt"):
        with open(f"{name}.txt", "r") as f:
            chat_log_content = f.read()
    else:
        with open(f"{name}.txt", "w") as chat_log_content:
            chat_log_content.write(initial_info)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{chat_log_content}"},
            {"role": "user", "content": f"{message}"},
        ],
        temperature=0,
    )
    answer = response['choices'][0]['message']['content']

    print(f"AI: {answer}")

    log = open(f"{name}.txt", "a")
    log.write(f"{name}: {message}\nAI: {answer}\n")
    log.close()


