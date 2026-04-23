from utils import clear
from decimal import Decimal
from time import sleep
from storage import save_file
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("HISTORIC_CURRENCY_VALUE_API")

# Menu functions:

# ADD function
def add(nickname: str, user_data: dict, money: Decimal) -> Decimal:
    clear()
    print(f"Total money: {money}")
    while True:
        print("Enter number to add and *number to change the value to the number. (QUIT to quit)")

        total = input("Enter: ")
        if total.strip() == "":
            print("Error: please enter a number...")
            sleep(1.5)
            continue
        if total.upper() == "QUIT":
            break
        if total[0] == "*":
            money = 0
            total = total[1:]
        try:
            total = Decimal(total)
            money += total
        except:
            print("Error: please enter a number...")
            sleep(1.5)
            continue
        print("Money added successfully!")
        sleep(1.5)
        break
    # TODO add money to users bank account
    user_data["money"] = float(money)

    
    save_file(data=user_data, user_name=nickname)

    return money

# DEL function
def delete(nickname: str, user_data: dict, money: Decimal = Decimal("0")) -> Decimal:
    clear()
    print(f"Total money: {money}")
    print("Enter number to delete that amount of money from you bank account. Enter 'quit' to quit.\n")
    
    while True:
        number = input("Enter: ")
        if number.lower() == "quit":
            break
        elif number.isnumeric():
            number = Decimal(number)
            money -= number
            user_data["money"] = float(money)

            save_file(data=user_data, user_name=nickname)
            print("Success!")
            sleep(1)
            break
        else:
            print("Please enter a number...")
            continue
    
    return money

# Detailed overview of the currency, including graphs
def overview() -> None:
    pass