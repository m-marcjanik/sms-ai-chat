import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_KEY")

completion = openai.Completion()

initial_info = "Human: We are roleplaying."

incoming_number = input("Before starting chat, please state your username:\n")

while True:
    incoming_msg = input(f"{incoming_number}: ")

    if os.path.exists(f"{incoming_number}.txt"):
        with open(f"{incoming_number}.txt", "r") as f:
            chat_log_content = f.read()
    else:
        with open(f"{incoming_number}.txt", "w") as chat_log_content:
            chat_log_content.write(initial_info)

    prompt = f'{chat_log_content}Human: {incoming_msg}\nAI:'
    response = completion.create(prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0,
                                 max_tokens=150)
    answer = response.choices[0].text.strip()
    print(f"AI: {answer}")

    log = open(f"{incoming_number}.txt", "a")
    log.write(f"Human: {incoming_msg}\nAI: {answer}\n")
    log.close()

