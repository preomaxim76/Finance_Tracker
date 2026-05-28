from storage import open_file, save_file
import bcrypt
from time import sleep
from utils import clear
from requests import get
import os
import sys
from math import log2
from ai import call_ai

URL = "https://api.frankfurter.dev/v2/rates"


# Authorizing and signing in

# Check if password is secure:
# S = log2(N) * L
# Where L is length and N is the range, the variety of different symbols
def password_is_secure(password: str) -> str:
    l = len(password)
    n = 75 # A-Z, a-z, 0-9, !@ ...

    s = log2(n) * l
    
    # Values of s:
    # 0 - 32 bits: Very weak
    # 32 - 59 bits: Moderate
    # 60 - 80 bits: Strong
    # 80+ bits: Highly secure

    if s < 32:
        return "Very Weak"
    
    if s < 59:
        return "Moderate"
    
    if s < 80:
        return "Strong"
    
    if s > 80:
        return "Highly Secure"


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
        # Sign up
        if inpt.lower().strip() == "sign up":
            return "", ""
        
        # If length == 2 -> it should be valid/invalid email & password
        if len(inpt.split()) == 2:
            nn, password = inpt.split()
            data = open_file(table_name="users")

            # Checking password with bcrypt (because passwords are hidden)
            if nn in data and bcrypt.checkpw(password.encode(), data[nn]["password"][2:-1].encode()):
                return nn, password
            else:
                print("Error: Incorrect email or password")
        else:
            print("Invalid Input")

# Change Currency: is used in settings (when changing currency) and in sign_up (when setting one)
def change_currency(data: dict, first: bool=True) -> dict:
    converting_currencies: list = ["USD", "RUB", "EUR", "GBP", "CHY", "CAD", "AUD", "JPY"] # The main ones

    # Checking if we want settings() or sign_up()
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

        # Updating data with new currency and currency values
        data.update({"user_currency": currency.upper(), "other_currencies": other_curr})
        
        return data

# This function generates 4 usernames (it uses AI from call_ai() function)
# TODO: Consider changing in the future, since AI gives unstable returns
def generate_usernames(example: str) -> dict:
    bad_usernames = open_file(table_name="users").keys() # The ones that are already being used
    
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

# This function is used both in sign_up (to set nickname) and in settings (to change it)
def change_nickname(users_data: dict, user_nicknames: list = []) -> str:
    flag = True 
    while True:
        username = input("Please create your username: ")
        # User nicknames are nicknames that the user changed while he was in settings (since program only saves data in menu() after user quits)
        if username in users_data and username not in user_nicknames:
            print("Unfortunately, this nickname already exists. \nSuggestions:\n")

            usernames = generate_usernames(example=username) # Generating 

            for key, username in usernames.items():
                print(f"{key}. {username}")
            print()

            length = len(usernames)

            # Quit to enter their own or number to choose suggestion
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

def change_password() -> str:
    flag = False
    output: str = "Create your password: "
    while True:
        clear()
        password: str = input(output).strip()
        
        secure = password_is_secure(password)
        
        if secure not in ("Highly Secure", "Strong"):
            print()
            print(f"Your password is {secure}.")
            print("Are you sure you want to choose this password?")
            while True:
                answer = input("Enter: ").lower().strip()
                if answer in ("yes", "y"):
                    flag = True
                    break
                elif answer in ("no", "n"):
                    output = "Create a stronger password: "
                    break
        # Do not require verification
        else:
            flag = True
        if flag:
            break   
    return password          

# Sign up -> data, nickname, password
def sign_up() -> tuple[dict, str, str]:
    users_data = open_file(table_name="users")

    # New user data
    data: dict = {}
    data["money"] = 0

    clear()
    print("Create an account.")
    
    username = change_nickname(users_data)

    password = change_password()

    # Converts password to bytes
    byte_password: bytes = password.encode()

    # Hashing passwords
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    
    data["password"] = str(hashed)
    data["goal"] = "N/A" # Not set by default
    data["income"] = 0.0 # Not set by default
    
    # Adding currency
    data = change_currency(data)


    # Saving data of our user to file users_finances.json
    save_file(data=data, user_name=username, table_name="users")

    print("You have successfully registered!")
    sleep(2)
    
    return data, username, password
