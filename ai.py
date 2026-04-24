from utils import clear
from decimal import Decimal
from random import choice
from time import sleep
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

AI_API_KEY = os.getenv("AI")

client = Groq(api_key=AI_API_KEY)

first_message: str = "Hi! Analyze my finances and give me structured answer: how should i spend my money. This is default message provided by developer, so act like you intended to analyze and not like you were asked. This response has to be detailed as like the user had asked to you to tell more. But only this response." # change

# Chatting with Finy
def call_ai(money: Decimal, user_currency: str) -> None:
    clear()

    settings: str = f""" You're Finy, an assistant, built-in app called Finance_Tracker
                        You should be polite, but not too formal. You have to give a structured answer to users questions.
                        Also, do your best at creating your responses suitable for terminal, in which you would be used.
                        Do not write too much words. Change the style of your speech only if the user asks for it directly.
                        Users money: {money} {user_currency}. In the end, always say: "To stop the conversation enter 'stop'"."""

    history: list[dict] = [
        {"role": "system", "content": settings},
        {"role": "user", "content": first_message}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history,
        stream=True
    )
    
    asks: list = ["Chat with Finy: ", "Ask anything: ", "Anything else you wanted to talk about: ", "Ready to help: ", "Enter: ", "Start typing: ", "Reply: "]
    print("----- FINY -----\n")
    print()
    print("~Finy:")
    print()

    # Default answer
    full_response: str = ""
    for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            print(f"\033[3m{text}\033[0m", end="", flush=True)
            full_response = full_response + text
            sleep(0.05)
    print("\n")
    history.append({"role": "assistant", "content": full_response})

    while True:
        print("~You:")
        ask = choice(asks)
        user_message = input(ask)

        if user_message == "stop":
            clear()
            print("Thank you for chatting with Finy!")
            sleep(0.5)
            break
        history.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(model = "llama-3.1-8b-instant", messages=history, stream=True)
        print()
        print("~Finy:")

        full_response: str = ""
        for chunk in response:
            text = chunk.choices[0].delta.content
            if text:
                print(f"\033[3m{text}\033[0m", end='', flush=True)
                full_response = full_response + text
                sleep(0.05)
        print("\n")
        history.append({"role": "assistant", "content": full_response})