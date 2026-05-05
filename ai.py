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

# Calling ai
def call_ai(history: list[dict], mode="char"):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history,
        stream=True
    )
    if mode == "char":
        for chunk in response:
            text = chunk.choices[0].delta.content
            if text:
                yield text
    elif mode == "word":
        text = ""
        for chunk in response:
            t = chunk.choices[0].delta.content
            if not t:
                continue
            if t == ',':
                yield text
                text = ""
            elif "," in t:
                text = text + t[:t.find(",")]
                yield text
                text = t[t.find(",")+1:]
            else:
                text = text + t 
    

def call_finy(money: Decimal, user_currency: str, income: Decimal="N/A", goal: str="N/A", mode: str="basic") -> None:
    clear()
    print("----- FINY -----")
    print()

    asks: list[str] = ["Chat with Finy: ", "Ask anything: ", "Anything else you wanted to talk about: ", "Ready to help: ", "Enter: ", "Start typing: ", "Reply: "]

    settings: str = f""" You're Finy, an assistant, built-in app called Finance_Tracker
                        You should be polite, but not too formal. You have to give a structured answer to users questions.
                        Also, do your best at creating your responses suitable for terminal, in which you would be used.
                        Do not write too much words. Change the style of your speech only if the user asks for it directly.
                        Users money: {money} {user_currency}. Their monthly income: {income}. Their current goal: {goal}.
                        Never suggest to set anything since you can't change their settings (goals, income, money, currency).
                        Never make anything up.
                        In the end, always say: "To stop the conversation enter 'quit'"."""
    # Analysis first, then chatting
    if mode == "basic":
        first_message: str = """This is default message, provided by developer. Analyze user's finances and give structured description.
                            Hand them some advice. Make it look like you weren't asked to do this analysis.
                            Afterwards, you can communicate more freely.""" 
    # No analysis
    elif mode == "chat":
        print("~You:")
        first_message = input("Start chatting with Finy: ")

    history: list[dict] = [
        {"role": "system", "content": settings},
        {"role": "user", "content": first_message}
    ]
    print()
    print("~Finy:")

    full_response = ""
    for chunk in call_ai(history):
        print(f"\033[3m{chunk}\033[0m", end="", flush=True)
        full_response = full_response + chunk
        sleep(0.05)
    history.append({"role": "assistant", "content": full_response})
    print()
    
    while True:
        print()
        print("~You:")
        ask = choice(asks)
        user_message = input(ask)

        if user_message.lower().strip() == "quit":
            break

        history.append({"role": "user", "content": user_message})

        print()
        print("~Finy:")
        full_response = ""
        for chunk in call_ai(history):
            print(f"\033[3m{chunk}\033[0m", end="", flush=True)
            full_response = full_response + chunk
            sleep(0.05)

        history.append({"role": "assistant", "content": full_response})

    return