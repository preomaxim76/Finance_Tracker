from utils import clear
from decimal import Decimal, InvalidOperation
from time import sleep
from storage import save_file
import plotly.express as px
from ai import call_ai
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

# Updating users finances (total amount of money)
def update():
    pass

# Updating users monthly income
def income(currency: str, old_salary: Decimal) -> Decimal:
    clear()
    print("Set Monthly Salary")
    print()
    print(f"Enter your salary in {currency} ('quit' - to quit).")
    while True:
        user_input = input("INPUT: ")
        if user_input.lower().strip() == "quit":
            return old_salary
        try:
            salary = Decimal(user_input)
            if old_salary != "N/A":
                clear()
                print(f"Are you sure you want to change your salary?\n{old_salary} -> {salary}\n")
                while True:
                    ask = input("INPUT: ").strip().lower()
                    if ask in ["yes", "y"]:
                        break
                    elif ask in ["no", "n"]:
                        print("Your salary has not been changed...")
                        sleep(1.5)
                        return old_salary
                    else:
                        print("Error: please enter 'yes' or 'no'.")
            print(f"Your income has been successfully set as {salary} {currency}.")
            sleep(1.5)
            return salary
            

        except InvalidOperation:
            print(f"Error: {user_input} is not a number.")


# Setting a goal
def goal() -> str:
    settings: str = """
                    You need to make users goal shorter and more readable.
                    It should be like a short sentence. Example: "I want to save $1000 for mac".
                    You should not give any advices.
                    You should only write goal and thats it. No questions and anything".
                    If user asks you to change sth - you do.
                    Always write full sentences! Never add anything from yourself.
                    If user writes something strange, like 'hey' just print out 'N/A'.
                    If user doesn't complete his sentence, do not try to invent something, just print out the data you have:
                    example: i want -> you answer with: 'I want <something>."""

    clear()
    print("Create your goal. Try to be short and consistent. \nTo quit - 'QUIT'. 'SET GOAL' - to set current goal.\n")
    users_goal = input("INPUT: ")
    if users_goal.lower().strip() == "quit":
        return

    history: list[dict] = [
        {"role": "system", "content": settings},
        {"role": "user", "content": users_goal}
    ]

    
    while True:
        print()
        print("~Finy:")

        full_response = ""
        for chunk in call_ai(history):
            print(chunk, end="", flush=True)
            sleep(0.05)
            full_response = full_response + chunk
        print()

        history.append({"role": "assistant", "content": full_response})

        print()
        print()
        print("SET <goal> to set <goal> as your goal.")
        user_message = input("INPUT: ")
        um = user_message.lower().strip()

        if um == "quit":
            return
        if um == "set goal":
            clear()
            print("Your goal has been successfully changed!")
            sleep(1.5)
            return full_response
        elif um.startswith("set"):
            print("Your goal has been successfully changed!")
            sleep(1.5)
            return " ".join(um.split()[1:])
        
        history.append({"role": "user", "content": user_message})
        
        
        
    


# Detailed overview of the currency, including graphs
def overview() -> None:
    pass



