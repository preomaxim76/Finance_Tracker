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
from dateutil.parser import parse, _parser
from storage import open_file

load_dotenv()
API_KEY = os.getenv("HISTORIC_CURRENCY_VALUE_API")

# Menu functions:

# Updating users finances (total amount of money) with +/- or salary 
def update(total: Decimal, username: str, total_income: Decimal, currency: str) -> Decimal:
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

        # Now
        t = datetime.now()
            

        update_file(
            data={"username": username, "money_transaction": money, "way": start, "datetime": t, "description": description},
            user_name=username, 
            currency=currency,
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

        # Saving history and printing out
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

    today = date.today()
    beginning = today.year - 30

    # Find valuespass
    url = f"https://api.frankfurter.app/{beginning}-01-01..{today}"

    params = {
        "from": currency,
        "to": convert_currency
    }
    
    try:
        days = []
        values = []
        request = get(url, params).json()["rates"]

        for key, value in request.items():
            days.append(key)
            values.append(value[convert_currency])

    except KeyError:
        return "Invalid",

    # Special, used in stocks
    df = px.data.stocks()

    fig = px.line(df, x=days, y=values, title=f"{currency} -> {convert_currency} Change Through {beginning}-01-01 To {today}", 
                     labels=
                     {
                         "X_data": "days",
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

    params = {
        "base": currency,
        "quotes": convert_currency
    }

    r = get("https://api.frankfurter.dev/v2/rates", params).json()[0]

    clear()
    print(f"{currency.upper()}: Description\n")
    print(f"{currency}: {r['rate']} {convert_currency}")
    print()
    print("-" * 30)
    for chunk in call_ai(history):
        print(chunk, end="", flush=True)
        sleep(0.02)
    print()
    print("-" * 30)
    print()
    print("Have a look at the graph we created for you in your browser!")

    fig.show() # Printing out graph

    return today, beginning

# Currency overview
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
        length = len(user_input)

        if length not in (2, 3):
            print("Error: please enter valid input...")
            continue
        curr = user_input[1].upper()
        try:
            value = float(user_input[0])
        except ValueError:
            print()
            print("Error: please enter integer or decimal in the first field...")
            sleep(1.5)
            print()
            continue

        if len(user_input) == 2:
            if curr == currency:
                print()
                print("-" * 30)
                print(f"{value} {user_input[1]} = {value} {user_input[1]}")
                print("-" * 30)
                print()
                continue

            params = {
                "base": curr,
                "quotes": currency,
                "date": f"{today.year}-{today.month}-{today.day}"
            }    
            
        else:
            try:
                user_datetime = parse(user_input[2])
            except _parser.ParserError:
                print("Error: please enter a valid datetime...")
                continue

            if not datetime(beginning, 1, 1) < user_datetime <= datetime(today.year, today.month, today.day):
                print(f"Error: please enter date between {beginning} and {today}.")
                continue
            user_date = user_datetime.date()

            if curr == currency:
                params = {
                    "base": curr,
                    "quotes": currency
                }
                todays_rate = get(url, params)

                params = {
                    "base": curr,
                    "quotes": currency,
                    "date": user_date
                }
                previous_rate = get(url, params)

                print("-" * 30)
                print(f"{value} {curr} = {round(value * todays_rate / previous_rate, 3)} {curr}")
                print("-" * 30)
                continue
            
            params = {
                "base": curr,
                "quotes": currency, 
                "date": f"{user_date.year}-{user_date.month}-{user_date.day}"
            }
        
        curr_output = get(url, params)
        if curr_output == []:
            print("Error: please enter a valid currency...")
            sleep(1.5)
            continue

        try:
            curr_value = curr_output.json()[0]["rate"]
        except (KeyError, IndexError):
            print("Error: please enter a valid currency...")
            print()
            sleep(1.5)
            continue

        print()
        print("-" * 30)
        print(f"{value} {curr} = {round(curr_value * value, 3)} {currency}")
        print("-" * 30)
        print()

# Sorting for last_transactions function
def _sort(data: list, mode:str = "basic") -> None:
    while True:
        clear()
        print("--- Keep Track of Your Transactions ---\n")
        if mode == "basic":
            for transaction in data:
                print(f"{transaction['way']}{transaction['money_transaction']} {transaction['currency']} at {transaction['datetime']}")
        else:
            for count, transaction in enumerate(data, start=1):
                print(f"{count}. {transaction['way']}{transaction['money_transaction']} {transaction['currency']} at {transaction['datetime']}")
                print(f"   Description: {transaction['description']}")
        print()
        print("Sort By:\n1. DATE - sort by date\n2. COST - sort by money transaction\n3. QUIT\nASC - ascending DESC - descending\n")
        way = input("INPUT: ").lower().strip()

        if way == "quit":
            break
        
        if not " " in way:
            print("Error: Please enter <sortby> and <ASC/DESC>...")
            sleep(1.5)
            continue

        way = way.split()

        sortby = way[0]
        level = way[1]

        if level not in ("asc", "desc"):
            print("Error: please enter ASC or DESC as a second argument...")
            sleep(1.5)
            continue
        
        match sortby:
            case "date":
                data = sorted(data, key=lambda elem: parse(elem["datetime"]))

            case "cost":
                data = sorted(data, key=lambda elem: elem["money_transaction"])

            case _:
                print("Error: INVALID <sortby>")
                sleep(1.5)
        if level == "desc":
            data.reverse()
    return

# Last transactions manipulating
def last_transactions(nickname: str) -> None:
    clear()
    slogan: str = "--- Keep Track of Your Transactions ---\n"
    print(slogan)
    print("Enter how many transactions you would like to view.")
    while True:
        try:
            number = int(input("INPUT: "))
            break

        except ValueError:
            print("Error: please enter a number...")
            sleep(0.5)
            continue

    data: list = open_file("transactions", number, nickname=nickname)
    
    while True:
        clear()
        print(slogan)
        for transaction in data:
            transaction["datetime"] = transaction["datetime"]
            print(f"{transaction['way']}{transaction['money_transaction']} {transaction['currency']} at {transaction['datetime']}")
        print()
        print("MENU:")
        print("1. SORT - sort this list\n2. FIND <date> - find all transactions\n3. QUIT\n")

        menu_choice = input("INPUT: ").lower().strip()
        
        # Quit
        if menu_choice == "quit":
            break

        if " " in menu_choice:
            func = menu_choice.split()[0]
            arg = menu_choice.split()[1]
        else:
            func = menu_choice
            arg = None
        
        match func:
            # SORT
            case "sort":
                if number > 1:
                    _sort(data)
                else:
                    print("You can't use this function with only one transaction selected...")
                    sleep(1.8)

            # FIND
            case "find":
                # Only function was given
                if not arg:
                    print("Error: FIND function takes argument <date>")
                    sleep(1.5)
                    continue
                
                # Check whether <date> is correct
                try:
                    transaction_datetime = parse(arg).date()

                except (_parser.ParserError, TypeError):
                    print("Error: given date/time is invalid... Please enter at least year...")
                    sleep(1.5)
                    continue
                
                transactions: list = open_file("transactions", 0, nickname, transaction_datetime)
                if not transactions:
                    print("Nothing was found for this date...")
                    sleep(2)
                else:
                    print("Transactions found...")
                    sleep(1)
                    _sort(transactions, mode="find")
                    
            # Invalid Function
            case _:
                print(f"Error: {func.upper()} is not a valid function...")
                sleep(1.5)
