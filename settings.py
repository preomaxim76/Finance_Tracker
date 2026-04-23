from utils import clear
from time import sleep
import bcrypt
from copy import deepcopy
from auth import change_currency
from storage import open_file


# Settings functions:

def change_nickname(to_return: dict, users_data: dict, nickname: str) -> dict:
    old_nickname = nickname
    while True:
        username = input("Please enter your new username: ")
        if username == nickname:
            print("This is your last saved nickname.")
            print("Do you want to keep it?")
            answer = input("Enter: ")
            if answer.strip().lower() in ["yes", "y"]:
                print("Your nickname has not been changed.")
                sleep(2)
                return to_return
        elif username in users_data:
            print("Unfortunately, this nickname already exists. Try another one.")
            continue
        else:
            nickname = username
            to_return["nickname"] = nickname
            to_return["old_nickname"] = old_nickname
            print(f"You have successfully changed your nickname from {old_nickname} to {nickname}.")

            sleep(2)
            return to_return


def change_password(password: str) -> tuple[str, bool]:
    clear()
    confirm = input("Please enter your old password: ")
    if confirm.strip() == password:
        clear()
        return input("Enter your new password: ").strip(), True
    else:
        print("Invalid password")
        sleep(2)
        return password, False

# Rating: rate, feedback -> txt file
def rate_app(nickname: str):
    rate: int = 0
    print("How was your experience?")
    while True:
        number = input("Enter number/10: ")
        if number.isdigit() and 0 < int(number) < 11:
            rate = number
            break
        else:
            print("Please enter an integer from 1 to 10")
            sleep(0.1)
    feedback = input("Please leave your feedback and tell us what we can do better: ")
    with open("Python/TProjects/Finance_Tracker/user_ratings.txt", "a") as f:
        f.write(f"Nickname: {nickname}\n")
        f.write(f"Feedback: {feedback}\n")
        f.write(f"\nRate: {rate}/10\n\n")



# Settings: currency, password, nickname, delete account
def settings(user_data: dict, nickname: str, password: str) -> dict:
    users_data: dict = open_file()
    to_return = deepcopy(user_data)
    view = False
    var = "view"
    to_return["password_is_changed"] = False
    to_return["nickname"] = nickname
    while True:
        currency = to_return["user_currency"]


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
        print("To rate our app: 'rate'.")
        print("To delete account, enter 'del account'.")
        print("To save changes - quit.\n")

        possible: list = ["nickname", "currency", "pass", "password", "del account", "rate", "quit"]

        while True:
            func = input("Enter ('QUIT' - to quit): ").strip().lower()

            if not func in possible:
                print(f"Error: {func} is not a function")
                sleep(0.1)
                continue
            break

        match(func):
            case "nickname":
                clear()
                print("Are you sure you want to change your nickname?")
                answer = input("Enter: ").strip().lower()

                if answer in ("y", "yes"):
                    to_return = change_nickname(to_return, users_data, nickname)
                    nickname = to_return["nickname"]
                else:
                    continue
                    
            
            case "currency":
                old_currency = currency
                to_return = change_currency(to_return, first=False)
                print(f"Currency has been successfully changed from {old_currency} to {to_return['user_currency']}.")
                sleep(2)
                
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
                

            case "password":
                password: tuple[str, bool] = change_password(password)
                
                if password[1]: # Password was changed
                    to_return["password"] = password[0]
                    to_return["password_is_changed"] = True
                password = password[0]
                print("Your password has been successfully changed.")
                sleep(2)
                continue

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

            case "rate":
                clear()
                print("Rating")
                print()
                rate_app(nickname)
                print("Your feedback has been saved! Thank you!\nIt really helps us get better!")
                sleep(3.5)

            case "quit":
                return to_return
        

