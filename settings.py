from utils import clear
from time import sleep
from copy import deepcopy
from auth import change_currency, change_nickname, change_password
from storage import open_file
from requests import get
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CURRENT_CURRENCY_VALUE_API")


# Settings functions:

# Settings: currency, password, nickname, delete account
def settings(user_data: dict, nickname: str, password: str) -> dict:
    users_data: dict = open_file(table_name="users")
    to_return = deepcopy(user_data)
    view = False
    var = "view"
    to_return["password_is_changed"] = False
    to_return["nickname"] = nickname
    user_nicknames = [] # To track nickname changes
    while True:
        currency = to_return["user_currency"]

        # View password?
        if not view:
            output = len(password) * "*"
            var = "view"
        else:
            output = password
            var = "hide"

        clear()
        print("---SETTINGS---\n")

        print(f"Current nickname: {nickname}. To change: 'nickname'")
        print(f"Current currency: {currency}. To change: 'currency'")
        print(f"Current password: '{output}'. To {var}: pass; To change: 'password'")
        print("To delete account, enter 'del account'.\n")
        print("To save changes - quit.\n")

        possible: list = ["nickname", "currency", "pass", "password", "del account", "quit"]

        while True:
            func = input("Enter ('QUIT' - to quit): ").strip().lower()

            if not func in possible:
                print(f"Error: {func} is not a function")
                sleep(0.1)
                continue
            break

        match(func):
            # Nickname changing
            case "nickname":
                clear()
                print("Are you sure you want to change your nickname?")
                answer = input("Enter: ").strip().lower()

                if answer in ("y", "yes"):
                    old_nickname = nickname
                    # Saving old nickname
                    user_nicknames.append(old_nickname)
                    nickname = change_nickname(users_data, user_nicknames)

                    to_return["nickname"] = nickname
                    to_return["old_nickname"] = old_nickname
                    clear()
                    print("Your username has been successfully changed!")
                    sleep(1.5)
                else:
                    continue
                    
            # Currency changing
            case "currency":
                old_currency = currency
                to_return = change_currency(to_return, first=False)
                new_currency = to_return["user_currency"]
                
                clear()
                print("Would you like to change your money amount to match your new currency?")
                while True:
                    change_money_value = input("Enter: ")
                    if change_money_value.lower() in ("yes", "y"):
                        clear()
                        other_currencies = to_return["other_currencies"]

                        if old_currency in other_currencies:
                            to_return["money"] = to_return["money"] / to_return["other_currencies"][old_currency]

                        else:
                            r = get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{new_currency}")
                            currency_value = r.json()["conversion_rates"][old_currency]
                            to_return["money"] = to_return["money"] / currency_value
                            
                        print(f"Currency has been successfully changed from {old_currency} to {to_return['user_currency']}")
                        print(f"Your total money has changed: {round(to_return['money'], 3)} to match your new currency.")
                        sleep(2.5)
                        break
                    elif change_money_value.lower() in ("no", "n"):
                        clear()
                        print(f"Currency has been successfully changed from {old_currency} to {to_return['user_currency']}.")
                        sleep(2)
                        break
                    else:
                        print("Please enter 'yes' or 'no'.")
                        sleep(.5)

                
                
            # Password viewing
            case "pass":
                clear()
                if view:
                    view = False
                    continue

                print(f"Are you sure you want to {var} your password?")
                answer = input("Enter: ").strip().lower()
                
                if answer in ("y", "yes"):
                    view = True
                else:
                    continue
                
            # Password changing
            case "password":
                clear()
                confirm = input("Please enter your old password: ")
                if confirm.strip() == password:
                    clear()
                    to_return["password"] = change_password()
                    to_return["password_is_changed"] = True
                    print("Your password has been successfully changed.")
                else:
                    print("Invalid password")
                    sleep(2)
                
                password = to_return["password"]
                
                sleep(2)
                continue
            # Account deletion
            case "del account":
                clear()
                print("Are you sure you want to delete your account? Your data will be lost forever.")
                answer = input("Enter: ").strip().lower()
                if answer not in ("y", "yes"):
                    continue
                clear()
                ps = input("Please enter your password to delete your account: ")
                if ps.strip() != password:
                    print("Invalid Password")
                    sleep(1.5)
                    continue

                
                clear()
                print("Deletion has been successful.")
                sleep(2)

                return {}

            # Quit (back to menu)
            case "quit":
                return to_return
        

