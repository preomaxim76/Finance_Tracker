from time import sleep
from utils import clear
from auth import authorization, sign_up
from menu import menu
from storage import open_file
from utils import greeting


# Main - to start other functions
def main() -> None:
    clear()
    print("___Finance Tracker___")
    print("Keep Track of your finances!")
    print()
    nickname, password = authorization()
    if nickname == "": # The user does not have an account
        user_data, nickname, password = sign_up()
    else:
        user_data = open_file()[nickname]


    clear()
    print(greeting(nickname))
    sleep(2)
    menu(nickname, user_data, password)

if __name__ == "__main__":
    main()