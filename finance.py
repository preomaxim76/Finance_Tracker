from utils import clear
from decimal import Decimal, InvalidOperation
from time import sleep
from storage import update_file
import plotly.express as px
from ai import call_ai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("HISTORIC_CURRENCY_VALUE_API")

# Menu functions:

# Updating users finances (total amount of money)
def update(total: Decimal, username: str, total_income: Decimal) -> Decimal:
    clear()
    print("----MONEY UPDATING----\n")
    print("Please enter +'number' or -'number' to add or delete money from your total amount.\nTo add your salary enter 'salary'.\nTo exit - 'quit'.\n")
    while True:
        command = input("INPUT: ").lower().strip()
        if command == "quit":
            return total
        elif command == "" or command.isspace():
            print("Error: please enter +/- and a valid number...")
            continue
        elif command == "salary":
            total += total_income
            print(f"Successfully added {total_income}!")
            description = "My Salary"
            money = total_income
            start = "+"
            sleep(1)

            
        else:
            start = command[0]

            try:
                money = Decimal(command[1:].strip())
            except InvalidOperation:
                print("Error: please enter +/- and a valid number...")
                continue

            if start == "+":
                total += money

            elif start == "-":
                total -= money
            
            else:
                print("Error: please enter +/- as a first character...")
                continue
            description = input("Note: ")

        t = datetime.now()
            

        update_file(
            data={"username": username, "money_transaction": money, "way": start, "datetime": t, "description": description},
            user_name=username, 
            file_name="transactions.db",
            table_name="transactions"
        )



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
            if old_salary != 0.0:
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
            clear()
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
    print("Create Your Goal\n\nSET <goal> to set <goal> as your goal.\n<goal> - to see AI's suggestion\nTo quit - 'QUIT'. \n")
    users_goal = input("INPUT: ").strip()
    if users_goal.lower() == "quit":
        return
    
    # User wants to set their goal manually
    if users_goal.lower().startswith("set"):
        clear()
        print("Your goal has been successfully changed!")
        sleep(1.5)
        return users_goal[3:].strip()

    history: list[dict] = [
        {"role": "system", "content": settings},
        {"role": "user", "content": users_goal}
    ]

    
    while True:
        clear()
        print("Create Your Goal\n\nSET <goal> to set <goal> as your goal.\n<goal> - to see AI's suggestion\nTo quit - 'QUIT'. \n")
        print("~Finy:")

        full_response = ""
        for chunk in call_ai(history):
            print(chunk, end="", flush=True)
            sleep(0.05)
            full_response = full_response + chunk

        history.append({"role": "assistant", "content": full_response})

        print()
        print()
        print("'SET GOAL' - to set current goal.")
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



