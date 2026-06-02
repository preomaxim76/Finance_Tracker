# Finance_Tracker

Finance Tracker, fully written in Python, is a TUI application to help people manage their finances.

*** PROJECT ARCHITECTURE ***
1. main.py: 
   Main.py is the main file to launch other files. 
2. auth.py: 
   Auth.py is the file that has functions related to signing up / logging in. It also includes some functions that are later being used in files like settings.py (f.e. change_nickname, generate_nickname, change_currency, etc.). 
3. menu.py: 
   Menu.py is the most used file of them all. Even though it has just one function, it connects all the parts together (settings, finances, ai, etc.). It is literally a menu, to which user comes back over and over again to choose actions and view their changes, to access other functions/features.
4. settings.py: 
   Settings.py is used to change some default settings. Some examples of what user can do: change username, nickname, password, currency, view their password and so on.
5. finance.py: 
   Finance.py, being the largest file, has functions, that are used to manipulate finances: update total amount of money, change income, goal, salary, to have currency overview, and view last transactions. 
6. ai.py: 
   Ai.py, as the name suggests, has functions related to AI. It has 2 functions: call_ai and call_finy. Function call_ai is used not only to call the financial assistant, but also to generate usernames. So, call_ai is a more abstract function, that gives ai the prompt and gets output, whereas call_finy is a function that works more with the financial assiatant, called Finy, itself. By the way, the model I'm using is Groq, it's convenient and fast.
7. storage.py: 
   Storage.py is a very important file. This file is more about saving all data, provoded by the user. With such functions that we use a lot in other code like open_file to get data, save_file, update_file and more, this file helps me stick with the rule DRY (Don't Repeat Yourself). I save data using SQLITE3 for convenience.
8. utils.py: 
   Utils.py is a file with 2 functions: clear() -> clears terminal to make it look nicer and greeting() -> to provide user with an appropriate greeting, depending on the curreny time of day (good morning/afternoon/evening/night).


- Signing Up / Loging in
Finance Tracker has a working database, that is handled using sqlite3 (a light version of sql) in the code (storage.py).
This database (clients.db) has two working tables:
1. users - a table that has the most important info about humans:
    1. Username (TEXT)
    2. Password (BLOB)
    3. Total Money Amount (REAL)
    4. User Currency (TEXT)
    5. Other Currencies (TEXT) - a dict of other currencies for easier access
    6. Income (REAL) - their monthly income
    7. Goal (TEXT)
    8. userId (INTEGER PRIMARY KEY)
2. transactions - a table that keeps track of users transactions:
    1. transactionId (INTEGER) - to match userId
    2. Total Amount of Money (REAL)
    3. Currency (TEXT) - in which currency this transaction was made
    4. Way (TEXT) - +/- to track whether user added or deleted money from their bank account
    5. Datetime (TEXT) - datetime of the transaction
    6. Description (TEXT) - short description provided by the user / or automatically (when salary/income is added)

When registering or changing nicknames, if user enters nickname already in use, AI will suggest some alternatives. Also if user enters nickname with space like "username 10" system will suggest to change to "username_10" and if denied will give AI suggestions. If AI suggestions are deinies in any case user would be given an oppurtunity to again choose their beloved username. This will repeat until user finds the best nickname.
When registering or changing password, user will be provided with information on how secure their password is (calculated by formula): Very Weak, Moderate. If password is Strong or Highly Secure, user won't get any info, since there's no need in changing password to a more secure one and will ask user whether they want to change it.
