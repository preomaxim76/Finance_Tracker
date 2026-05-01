from utils import clear
from decimal import Decimal
from time import sleep
from storage import save_file, open_file, delete_user
from finance import add, delete
from json import dump
from settings import settings
from ai import call_ai
import sys
import os
import bcrypt


# Menu
def menu(nickname: str, user_data: dict, password: str) -> None:
    clear()

    # Available functions
    available: list = ["add", "del", "finy", "curr", "settings", "quit"]

    # Users total money
    money: Decimal = Decimal(user_data["money"])

    user_currency = user_data["user_currency"]

    while True:
        clear()
        print("---HOME---")
        print(f"Total Money: {round(money, 3)} {user_currency}")
        print()
        print("Main Currencies:")
        print()
        
        for curr, value in user_data["other_currencies"].items():
            value = Decimal(value)

            print(f"{curr}: {round(value, 3)} {user_currency} - {round(money * value, 3)} {curr}")
        
        print()
        print("MENU: \n1. ADD - add/change money to/in your account\n2. DEL - delete money from your bank account\n3. FINY - integrated AI to help you with your finances\n4. CURR <currency> - returns detailed overview of the currency\n5. SETTINGS\n6. QUIT")

        while True:
            action: str = input("INPUT: ").split()
            func = action[0].lower()

            if func not in available:
                print(f"Error: function {func} is not found...")
                sleep(0.1)
            else:
                break

        match func:
            # Add money
            case "add":
                money = add(nickname=nickname, user_data=user_data, money=money)

            # Delete money
            case "del":
                money = delete(nickname=nickname, user_data=user_data, money=money)

            # Chatting with integrated AI Finy
            case "finy":
                call_ai(money, user_currency)

            # Detailed overview of the currency (including graphs)
            case "curr":
                pass

            case "settings":
                call = settings(user_data, nickname, password)
                if call == {}:
                    users = open_file()
                    del users[nickname]
                    with open("Python/TProjects/Finance_Tracker/users_finances.json", "w") as f:
                        dump(users, f)

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

                    
                    if "old_nickname" in call:
                        nickname = call["nickname"]
                        delete_user(call["old_nickname"])



                    save_file(user_data, nickname)



            # Quit
            case "quit":
                sys.exit()

