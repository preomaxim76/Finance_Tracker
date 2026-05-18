from storage import open_file, save_file
import bcrypt
from time import sleep
from utils import clear
from requests import get
import os
import sys
from json import decoder
from ai import call_ai

URL = "https://api.frankfurter.dev/v2/rates"


# Authorizing and signing in

# nickname if the user has an account, "" otherwise
def authorization() -> tuple[str, str]: 
    print("Type in your nickname and password if you have an account and 'sign up' if you don't.\nTo quit - 'quit'")
    
    while True:
        inpt = input("INPUT: ")
        if inpt.lower().strip() == "quit":

            clear()
            print("Are you sure you want to exit the program?")
            while True:
                ask = input("INPUT: ").lower().strip()
                if ask in ["y", "yes"]:
                    sys.exit()
                elif ask in ["n", "no"]:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)


                print("Error: please enter 'yes' or 'no'...")
        if inpt.lower().strip() == "sign up":
            return "", ""
        
        if len(inpt.split()) == 2:
            nn, password = inpt.split()
            dct = open_file(table_name="users")

            if nn in dct and bcrypt.checkpw(password.encode(), dct[nn]["password"][2:-1].encode()):
                return nn, password
            else:
                print("Error: Incorrect email or password")
        else:
            print("Invalid Input")

# Fix it
def change_currency(data: dict, first: bool=True) -> dict:
    converting_currencies: list = ["USD", "RUB", "EUR", "GBP", "CHY", "CAD", "AUD", "JPY"]
    if first:
        output: str = "Enter your currency: "
    else:
        output: str = "Enter your new currency: "

    while True:
        currency: str = input(output)
        print("Sending request...")

        params = {
            "base": currency,
        }
        
        lst = get(URL, params).json()
        if lst == [] or type(lst) == dict:
            print(f"Error: We couldn't find {currency} currency. Please enter a valid currency.")
            continue

        other_curr = {}
        for curr in lst:
            if curr["quote"] in converting_currencies:
                other_curr[curr["quote"]] = curr["rate"]


        data.update({"user_currency": currency.upper(), "other_currencies": other_curr})
        
        return data

def generate_usernames(example: str) -> dict:
    bad_usernames = open_file(table_name="users").keys()
    
    settings = f"""
                Generate exactly 4 usernames similar in style to: {example}.

                Rules:
                - Output ONLY 4 usernames (no explanations, no extra text)
                - Format: username1,username2,username3,username4,username5
                - No spaces anywhere
                - Use only lowercase letters and numbers
                - Keep them visually clean and modern
                - You may slightly modify the base name or add short suffixes/prefixes (numbers or short words)
                - Avoid special characters
                - Each username must be unique
                - Do NOT include any of these: {bad_usernames}

                Make the usernames look natural and realistic (like real users would pick them).
"""
    
    history: list[dict] = [
        {"role": "system", "content": settings}
    ]
    usernames = {count: un.strip().lower() for count in range(1, 5) for un in list(call_ai(history, mode="word")) if un.lower().strip() not in bad_usernames}
    return usernames

    
def change_nickname(users_data: dict) -> str:
    flag = True
    while True:
        username = input("Please create your username: ")
        if username in users_data:
            print("Unfortunately, this nickname already exists. \nSuggestions:\n")
            usernames = generate_usernames(example=username)
            for key, username in usernames.items():
                print(f"{key}. {username}")
            print()
            length = len(usernames)
            while True:
                inpt = input("Please enter a number or 'quit' to choose your own: ").lower().strip()
                if inpt == "quit":
                    break
                
                try:
                    inpt = int(inpt)
                except ValueError:
                    print("Error: please enter 'quit' or a valid number...")
                    continue

                if 1 <= inpt <= length:
                    break
                username = usernames[int(inpt)]
                clear()
                print(f"Your username {username} has been successfully set!")
                sleep(1.5)
                return username
            if inpt == "quit":
                clear()
                continue
            username = usernames[int(inpt)]
            clear()
            print(f"Your username {username} has been successfully set!")
            sleep(1.5)
            return username

        if " " in username:
            clear()
            ready_username = username.replace(" ", "_")
            print(f"Your username: '{username}' has spaces, which is invalid for a nickname.")
            print(f"Is it okay that your username would be changed: {username} -> {ready_username}?")
            while True:
                answer = input("INPUT: ").lower().strip()
                if answer in ["y", "yes"]:
                    clear()
                    print(f"Your username: {ready_username}.")
                    sleep(1.5)
                    username = ready_username
                    clear()
                    return username 
                elif answer in ["n", "no"]:
                    flag = False
                    break
        
            if flag == False:
                clear()
                print("Then we would like to suggest these usernames: ")
                usernames = generate_usernames(username)

                for key, username in usernames.items():
                    print(f"{key}. {username}")
                print()
                length = len(usernames)
                
                while True:
                    inpt = input(f"Please enter a number (1:{length}) or 'quit' to choose your own: ").lower().strip()


                    if inpt.isdigit() and 1 <= int(inpt) <= length:
                        break

                    if inpt == "quit":
                        break

                    else:
                        print(f"Error: please enter 'quit' or digit 1 - {length} (inc.)")

                if inpt == "quit":
                    clear()
                    continue

                username = usernames[int(inpt)]
                clear()
                print(f"Your username {username} has been successfully set!")
                sleep(1.5)
                return username
        return username
             

# Sign up -> data, nickname, password
def sign_up() -> tuple[dict, str, str]:
    users_data = open_file(table_name="users")

    # New user data
    data: dict = {}
    data["money"] = 0

    clear()
    print("Create an account.")
    
    username = change_nickname(users_data)

    password: str = input("Create your password: ").strip()

    # Converts password to bytes
    byte_password: bytes = password.encode()
    # Hashing passwords
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    
    data["password"] = str(hashed)
    data["goal"] = "N/A"
    data["income"] = 0.0
    
    # Adding currency
    data = change_currency(data)


    # Saving data of our user to file users_finances.json
    save_file(data=data, user_name=username, table_name="users")

    print("You have successfully registered!")
    sleep(2)
    return data, username, password
