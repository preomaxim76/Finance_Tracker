from utils import clear
from decimal import Decimal
from random import choice
from time import sleep
from ollama import chat # Changing soon

# Change to Groq

# Chatting with Finy
def call_ai(money: Decimal, user_currency: str) -> None:
    system = f"""
                You are Finy, a finance assistant.
                Answer questions **directly and concisely** in 2-3 sentences. 
                Focus on user's finances and give clear monthly spending advice. 
                Their total money: {money} {user_currency}. 
                Remember previous conversation for context. 
                Never add greetings or filler. 
                Always end with: 'To stop the conversation enter "stop"'.
            """
    messages = [
        {
            "role": "system",
            "content": system
        },
    ]

    asks: list = ["Chat with Finy: ", "Ask anything: ", "Anything else you wanted to talk about: ", "Ready to help: ", "Enter: ", "Start typing: ", "Reply: "]


    clear()
    while True:
        print("AI-assistant Finy:\n")
        ask = choice(asks)
        user_message = input(ask)

        if user_message == "stop":
            print("Thank you for chatting with Finy!")
            sleep(1.5)
            break
        messages.append({"role": "user", "content": user_message})

        print("Finy is thinking. Please wait a moment...")
        response = chat(model = "phi3:mini", messages=messages, stream=True)

        print("Finy:")

        full_response: str = ""
        for chunk in response:
            ans = chunk["message"]["content"]
            print(ans, end='', flush=True)
            full_response = full_response + ans
        print()
        messages.append({"role": "assistant", "content": full_response})