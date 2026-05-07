from utils import clear
from time import sleep
from copy import deepcopy
from auth import change_currency, change_nickname
from storage import open_file


# Settings functions:

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
    users_data: dict = open_file(file_name="clients.db", table_name="users")
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
                    old_nickname = nickname
                    nickname = change_nickname(users_data)

                    to_return["nickname"] = nickname
                    to_return["old_nickname"] = old_nickname
                    clear()
                    print("Your username has been successfully changed!")
                    sleep(1.5)
                else:
                    continue
                    
            
            case "currency":
                old_currency = currency
                to_return = change_currency(to_return, first=False)
                
                clear()
                print("Would you like to change your money amount to match your new currency?")
                while True:
                    change_money_value = input("Enter: ")
                    if change_money_value.lower() in ("yes", "y"):
                        clear()
                        to_return["money"] = to_return["money"] / to_return["other_currencies"][old_currency]
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
                    print("Your password has been successfully changed.")
                else:
                    print("Your password has not been changed.")
                password = password[0]
                
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
        

