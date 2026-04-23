import os
from datetime import datetime, time



# System functions

# Clear the terminal - style
def clear() -> None:
    if os.name == "nt": # Windows
        os.system("cls")
    else: # macOS or Linux
        os.system("clear")

# Returns daytime: morning, afternoon, evening, night
def greeting(nickname: str) -> str:
    t = datetime.now().time()
    daytime: str = ""
    if time(5) <= t < time(12):
        daytime = "morning"
    elif time(12) <= t < time(18):
        daytime = "afternoon"
    elif time(18) <= t < time(23):
        daytime = "evening"
    else:
        daytime = "night"
    return f"Good {daytime}, {nickname}!"

