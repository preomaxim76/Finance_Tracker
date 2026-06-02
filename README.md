# Finance_Tracker

Finance Tracker, fully written in Python, is a TUI application to help people manage their finances.
<SOME MORE DESCRIPTION>

*** PROJECT ARCHITECTURE ***
1. main.py
   Main.py is the main file to launch other files. 
2. auth.py
   Auth.py is the file that has functions related to signing up / logging in. It also includes some functions that are later being used in files like settings.py (f.e. change_nickname, generate_nickname, change_currency, etc.). 
3. menu.py
   Menu.py is the most used file of them all. It connects all the parts together (settings, finances, ai, etc.). It is literally a menu, to which user comes back over and over again to choose actions and view their changes, to access other functions/features.
4. settings.py
   <sth>
5. finance.py
   <sth>
6. ai.py
   <sth>
7. storage.py
   <sth>
8. utils.py
   <sth>


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
