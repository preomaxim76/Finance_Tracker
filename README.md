# Finance_Tracker

Finance Tracker, fully written in Python, is a TUI application to help people manage their finances.
<SOME MORE DESCRIPTION>

*** PROJECT ARCHITECTURE ***
1. main.py
   <sth>
2. auth.py
   <sth>
3. menu.py
   <sth>
4. settings.py
   <sth>
5. 

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
