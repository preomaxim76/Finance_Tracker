from utils import clear
from decimal import Decimal
from time import sleep
from storage import update_file, delete_user
from finance import goal, income, update, curr_overview
from json import dump
from settings import settings
from ai import call_finy
import sys
import os
import bcrypt


# Menu: printing out menu that user can interact with
# Access to all other functions (including quitting)
def menu(nickname: str, user_data: dict, password: str) -> None:
    clear()

    # Available functions
    available: list = ["finance", "finy", "curr", "settings", "quit", "finy chat"]

    # Users total money
    money: Decimal = Decimal(user_data["money"])
    user_currency = user_data["user_currency"]
    salary = Decimal(user_data["income"])
    user_goal = user_data["goal"]

    while True:
        clear()
        print("---HOME---")
        print(f"Total Money: {round(money, 3)} {user_currency}")
        print(f"Current Goal: {'N/A' if not user_goal else user_goal}")
        print(f"Total Income: {'N/A' if not salary else salary} {user_currency}")
        print()
        print("Main Currencies:")
        print()
        
        for curr, value in user_data["other_currencies"].items():
            value = Decimal(value)
            # Rounded to 3 after point to look better
            print(f"{curr}: {round(value, 3)} {user_currency} - {round(money * value, 3)} {curr}")
        
        print()
        print("MENU: \n1. FINANCE - manipulating finances\n2. FINY - integrated AI to help you with your finances (FINY CHAT to start chatting now)\n3. CURR <currency> - returns detailed overview of the currency\n4. SETTINGS\n5. QUIT")

        while True:
            action: str = input("INPUT: ").split()
            func = action[0].lower().strip()

            if func not in available:
                print(f"Error: function {func} is not found...")
                sleep(0.1)
            else:
                break

        match func:
            # finance.py functions
            case "finance":
                av = ["update", "income", "goal", "quit"]
                while True:
                    clear()
                    print("Finance Managing")
                    print()
                    print("Menu:")
                    print("\n1. UPDATE - to update your total amount of money\n2. INCOME - to update your income\n3. GOAL - to update your financial goal\n4. QUIT")
                    while True:
                        act: str = input("INPUT: ").lower().strip()
                        if act in av:
                            break
                        else:
                            print(f"Error: function {act} is not found...")
                            sleep(0.1)

                    match act:
                        case "update":
                            money = update(money, nickname, total_income=salary)
                            
                            user_data["money"] = float(money)
                            update_file(user_data, nickname, table_name="users")

                        case "income":
                            old = salary
                            salary = income(currency=user_currency, old_salary=old)
                            if salary:
                                user_data["income"] = float(salary) if salary != "N/A" else old
                                update_file(user_data, nickname, table_name="users")

                        # Financial Goal
                        case "goal":
                            user_g = goal()
                            # Not return
                            if user_g:
                                user_goal = user_g
                                user_data["goal"] = user_goal
                                update_file(user_data, nickname, table_name="users")


                        case "quit":
                            break


            # Chatting with integrated AI Finy
            case "finy":
                # If one -> "FINY" => Analysis first, conversation secondly
                if len(action) == 1:
                    call_finy(money, user_currency, salary, user_goal)
                
                # If two -> "FINY CHAT" => Chatting from the beginning
                elif len(action) == 2 and action[1].lower() == "chat":
                    call_finy(money, user_currency, salary, user_goal, mode="chat")

                # Invalid
                else:
                    print("Error: function call invalid...\nCorrect: 'FINY CHAT'.")
                    sleep(1.5)

            # Detailed overview of the currency (including graphs)
            case "curr":
                # Should be of length 2 (CURR <currency>)
                if len(action) == 2 and action[1].isalpha():
                    curr = action[1].upper()
                    clear()
                    curr_overview(curr, user_currency)
                else:
                    print("Error: function call invalid...\nCorrect: 'CURR <currency>'.")
                    sleep(1.5)

            case "settings":
                call = settings(user_data, nickname, password)
                # Delete
                if call == {}:
                    delete_user(nickname)
                    python = sys.executable
                    os.execl(python, python, *sys.argv)

                else:
                    if user_currency != call["user_currency"]:
                        user_currency = call["user_currency"]
                        user_data["user_currency"] = user_currency
                        user_data["other_currencies"] = call["other_currencies"]
                        user_data["money"] = call["money"]
                        money = Decimal(user_data["money"])
                    # Password is changed
                    if call["password_is_changed"]:
                        password = call["password"]
                        byte_password = password.encode()
                        hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
                        user_data["password"] = str(hashed)

                    if nickname != call["nickname"]:
                        old_nickname = nickname
                        nickname = call["nickname"]
                    else:
                        old_nickname = None
                        
                    update_file(user_data, nickname, table_name="users", old_username=old_nickname)

            # Quit
            case "quit":
                sys.exit()

