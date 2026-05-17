from utils import clear
from decimal import Decimal, InvalidOperation
from time import sleep
from storage import update_file
from ai import call_ai
from dotenv import load_dotenv
import os
from datetime import datetime, date
import plotly.express as px
from requests import get
import pandas as pd

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
def overview(currency: str, user_currency: str) -> tuple[str]:
    # Find the currency to convert to:
    convert_currency = ""
    if user_currency == currency and currency != "USD":
        convert_currency = "USD"
    elif user_currency == currency:
        convert_currency = "EUR"
    else:
        convert_currency = user_currency

    # Todays year rounded to 0 or 5
    today = date.today()
    rounded_today =  today.year // 5 * 5
    beginning = rounded_today - 30
    years: list[int] = [year for year in range(beginning, rounded_today+1, 5)]
    values: list[float] = []

    # Find values
    url = "https://api.frankfurter.dev/v2/rates"
    
    try:
        for year in years:
            params = {
            "base": currency,
            "quotes": convert_currency,
            "date": f"{year}-01-01"
            }
            response = get(url, params)
            values.append(response.json()[0]["rate"])
    except (KeyError, IndexError):
        return "Invalid",

    if today.year != rounded_today:
        params = {
            "base": currency,
            "quotes": convert_currency,
            "date": f"{today.year}-{today.month}-{today.day}"
        }
        response = get(url, params)
        years.append(today.year)
        todays_rate = response.json()[0]["rate"]
        values.append(todays_rate)
    df = pd.DataFrame({
        "X_data": years,
        "Y_data": values
    })

    fig = px.line(df, x="X_data", y="Y_data", title=f"{currency} Change Through {beginning}-01-01 To {today} In {convert_currency}", 
                     labels=
                     {
                         "X_data": "years",
                         "Y_data": convert_currency
                     })
    
    # Description
    settings = f"""
                You need to give summarization of this currency: {currency}. 
                Do not add any values (since you don't know relevant data).
                Don't ask user anything and act like you're a system.
                You should only sum up currency. If you know some funny facts about it - go for it.
                Try not to write too many words and try to use more enters;"""
    history = [
        {"role": "system", "content": settings}
    ]
    clear()
    print(f"{currency.upper()}: Description")
    print()
    print()
    print("-" * 30)
    for chunk in call_ai(history):
        print(chunk, end="", flush=True)
        sleep(0.02)
    print()
    print("-" * 30)
    print()
    print("Have a look at the graph we created for you in your browser!")

    fig.show()

    return today, beginning

def curr_overview(currency: str, user_currency: str) -> None:
    url = "https://api.frankfurter.dev/v2/rates"
    func_return = overview(currency, user_currency)
    if func_return[0] == "Invalid":
        print(f"Error: there's no such currency: {currency}...")
        sleep(1.5)
        return
    beginning = func_return[1]
    today = func_return[0]
    print("\nMENU:\n")
    print(f"To convert any currency to {currency} - '<value> <currency>'.")
    print(f"To convert any currency to {currency} (at any time between {beginning} and {today} - '<value> <currency> <date>'.)")
    print("To quit - 'quit'.\n")
    
            
    while True:
        user_input = input("INPUT: ").lower()

        if user_input == "quit":
            break

        user_input = user_input.split()
        
        if len(user_input) == 2:
            curr = user_input[1].upper()
            
            try:
                value = float(user_input[0])
            except TypeError:
                print("Error: please enter integer or decimal in the first field...")
                sleep(1.5)
                continue

            if curr == currency:
                print()
                print("-" * 40)
                print(f"{value} {user_input[1]} = {value} {user_input[1]}")
                print("-" * 40)
                print()
                continue

            params = {
                "base": curr,
                "quotes": currency,
                "date": f"{today.year}-{today.month}-{today.day}"
            }    
            curr_output = get(url, params)
            if curr_output == []:
                print("Error: please enter a valid currency...")
                sleep(1.5)
                continue
            try:
                curr_value = curr_output.json()[0]["rate"]
            except KeyError:
                print("Error: please enter a valid currency...")
                sleep(1.5)
                continue
            print()
            print("-" * 15)
            print(f"{value} {curr} = {curr_value * value} {currency}")
            print("-" * 15)
            print()
            
            

        elif len(user_input) == 3:
            pass

        else:
            print("Error: please enter valid input...")