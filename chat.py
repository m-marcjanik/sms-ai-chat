import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_KEY")

completion = openai.Completion()

initial_info = "System: We are two friends sending text messages to each other."

incoming_number = input("Before starting chat, please state your username:\n")

while True:
    incoming_msg = input(f"{incoming_number}: ")
    model = "gpt-3.5-turbo"

    if os.path.exists(f"{incoming_number}.txt"):
        with open(f"{incoming_number}.txt", "r") as f:
            chat_log_content = f.read()
    else:
        with open(f"{incoming_number}.txt", "w") as chat_log_content:
            chat_log_content.write(initial_info)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "We are roleplaying."},
            {"role": "user", "content": f"{incoming_msg}"},
        ],
        temperature=0,
    )
    answer = response['choices'][0]['message']['content']

    print(f"AI: {answer}")

    log = open(f"{incoming_number}.txt", "a")
    log.write(f"Human: {incoming_msg}\nAI: {answer}\n")
    log.close()


