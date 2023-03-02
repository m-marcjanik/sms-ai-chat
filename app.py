import openai
import os
from twilio.rest import Client
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_KEY")
twilio_account_sid = os.environ.get("TWILIO_SID")
twilio_auth_token = os.environ.get("TWILIO_TOKEN")

completion = openai.Completion()

initial_info = "Human: We are roleplaying. "


def send_sms(to, body):
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(to=to, from_="732106215", body=body)
    return message


app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():

    incoming_number = request.values["From"]
    incoming_msg = request.values["Body"]

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

    log = open(f"{incoming_number}.txt", "a")
    log.write(f"Human: {incoming_msg}\nAI: {answer}\n")
    log.close()

    send_sms(incoming_number, answer)

    return answer