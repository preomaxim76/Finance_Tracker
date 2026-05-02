from storage import open_file, save_file
import bcrypt
from time import sleep
from utils import clear
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CURRENT_CURRENCY_VALUE_API")


# Authorizing and signing in

# nickname if the user has an account, "" otherwise
def authorization() -> tuple[str, str]: 
    print("Type in your nickname and password if you have an account and 'sign up' if you don't.")
    
    while True:
        inpt = input("INPUT: ")
        if inpt.lower().strip() == "sign up":
            return "", ""
        if len(inpt.split()) == 2:
            nn, password = inpt.split()
            dct = open_file()

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

        r = get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}")
        try:
            dct = r.json()["conversion_rates"]
        except KeyError:
            print(f"Error: We couldn't find {currency} currency. Please enter a valid currency.")
            continue
        st_code = r.status_code
        if str(st_code)[0] == "2": # OK
            other_curr = {}

            for curr in converting_currencies:
                curr =  curr.upper()
                if curr != currency and curr in dct:
                    other_curr[curr] = dct[curr]

            data.update({"user_currency": currency.upper(), "other_currencies": other_curr})
            break
        else:
            print("Error occurred, while sending request (for developer):",  st_code)
    return data

# Sign in -> data, nickname, password
def sign_up() -> tuple[dict, str, str]:
    # converting_currencies: list = ["USD", "RUB", "EUR", "GBP", "CHY", "CAD", "AUD", "JPY"] 

    users_data = open_file()

    # New user data
    data: dict = {}
    data["money"] = 0

    clear()
    print("Create an account.")
    while True:
        username = input("Please create your username: ")
        if username in users_data:
            print("Unfortunately, this nickname already exists. Try another one.")
            continue
        break

    password: str = input("Create your password: ").strip()

    # Converts password to bytes
    byte_password: bytes = password.encode()
    # Hashing passwords
    hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    
    data["password"] = str(hashed)
    
    # Adding currency
    data = change_currency(data)

    # Saving data of our user to file users_finances.json
    save_file(data=data, user_name=username)

    print("You have successfully registered!")
    sleep(2)
    return data, username, password
