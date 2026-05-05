from utils import clear
from decimal import Decimal
from time import sleep
from storage import save_file, open_file, delete_user
from finance import add, delete, goal, income
from json import dump
from settings import settings
from ai import call_finy
import sys
import os
import bcrypt


# Menu
def menu(nickname: str, user_data: dict, password: str) -> None:
    clear()

    # Available functions
    available: list = ["finance", "add", "del", "finy", "curr", "settings", "quit", "finy chat"]

    # Users total money
    money: Decimal = Decimal(user_data["money"])
    user_currency = user_data["user_currency"]
    salary = user_data["income"]
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

            print(f"{curr}: {round(value, 3)} {user_currency} - {round(money * value, 3)} {curr}")
        
        print()
        print("MENU: \n1. FINANCE\n2. FINY - integrated AI to help you with your finances (FINY CHAT to start chatting now)\n3. CURR <currency> - returns detailed overview of the currency\n4. SETTINGS\n5. QUIT")

        while True:
            action: str = input("INPUT: ").split()
            func = action[0].lower().strip()

            if func not in available:
                print(f"Error: function {func} is not found...")
                sleep(0.1)
            else:
                break

        match func:
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
                            pass

                        case "income":
                            old = salary
                            salary = income(currency=user_currency, old_salary=old)
                            if salary:
                                user_data["income"] = float(salary) if salary != "N/A" else old
                                save_file(user_data, nickname)

                        # Financial Goal
                        case "goal":
                            user_g = goal()
                            # Not return
                            if user_g:
                                user_goal = user_g
                                user_data["goal"] = user_goal
                                save_file(user_data, nickname)


                        case "quit":
                            break



            # Add money
            case "add":
                money = add(nickname=nickname, user_data=user_data, money=money)

            # Delete money
            case "del":
                money = delete(nickname=nickname, user_data=user_data, money=money)

            # Chatting with integrated AI Finy
            case "finy":
                if len(action) == 1:
                    call_finy(money, user_currency)
                else:
                    call_finy(money, user_currency, mode="chat")

            # Detailed overview of the currency (including graphs)
            case "curr":
                pass

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
                        nickname = call["nickname"]
                        delete_user(call["old_nickname"])



                    save_file(user_data, nickname)



            # Quit
            case "quit":
                sys.exit()

