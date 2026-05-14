import sqlite3
import json

def get_user_id(username: str) -> str:
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()

    c.execute("SELECT userId FROM users WHERE username = ?", (username, ))
    
    userid = c.fetchone()[0]
    return userid

def create_table_if_not_exists(file_name: str, table_name: str) -> None:
    conn = sqlite3.connect(file_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if table_name == "users":
        c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                userId INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL, 
                money REAL,
                user_currency TEXT NOT NULL,
                other_currencies TEXT NOT NULL,
                income REAL,
                goal TEXT)
            """)
    elif table_name == "transactions":
        conn = sqlite3.connect("transactions.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER,
                money_transaction REAL NOT NULL,
                way TEXT NOT NULL,
                datetime TEXT NOT NULL, 
                description TEXT)""")
        
    conn.commit()
    conn.close()


    return


def open_file(file_name: str, table_name: str) -> dict:
    create_table_if_not_exists(file_name, table_name)

    conn = sqlite3.connect(file_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    
    c.execute(f"SELECT * FROM {table_name}")
    data = {row["username"]: {key: value for key, value in dict(row).items() if key != row["username"]} for row in c.fetchall()}
    for key in data:
        data[key]["other_currencies"] = json.loads(data[key]["other_currencies"])
    
    conn.commit()
    conn.close()

    
    return data

def save_file(data: dict, user_name: str, file_name: str, table_name: str) -> None:
    conn = sqlite3.connect(file_name)
    c = conn.cursor()
    if table_name == "users":
        create_table_if_not_exists("clients.db", "users")
        
        password = data["password"]
        money = data["money"]
        user_currency = data["user_currency"]
        other_currencies = json.dumps(data["other_currencies"])
        goal = data["goal"]
        income = 0.0 if not data["income"] else data["income"]
        c.execute("INSERT INTO users (username, password, money, user_currency, other_currencies, goal, income) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_name, password, money, user_currency, other_currencies, goal, income))
        
    conn.commit()
    conn.close()

    return

def update_file(data: dict, user_name: str, file_name: str, table_name: str, old_username: str=None) -> None:
    create_table_if_not_exists(file_name, table_name)

    conn = sqlite3.connect(file_name)
    c = conn.cursor()
    if not old_username:
        user_id = get_user_id(user_name)
    else:
        user_id = get_user_id(old_username)

    if table_name == "users":
        password = data["password"]
        money = data["money"]
        user_currency = data["user_currency"]
        other_currencies = json.dumps(data["other_currencies"])
        goal = data["goal"]
        income = data["income"]

        c.execute("UPDATE users SET username = ?, password = ?, money = ?, user_currency = ?, other_currencies = ?, goal = ?, income = ? WHERE userId = ?",
                  (user_name, password, money, user_currency, other_currencies, goal, income, user_id))
    
    # Updating transactions
    elif table_name == "transactions":
        total_money = float(data["money_transaction"])
        way = data["way"]
        transaction_datetime = str(data["datetime"])
        description = data["description"]
        c.execute("INSERT INTO transactions (transaction_id, money_transaction, way, datetime, description) VALUES (?, ?, ?, ?, ?);", 
                  (user_id, total_money, way, transaction_datetime, description))


    conn.commit()
    conn.close()

    return


def delete_user(user_name: str) -> None:
    create_table_if_not_exists("transactions.db", "transactions")
    conn = sqlite3.connect("transactions.db")
    c = conn.cursor()

    c.execute("DELETE FROM transactions WHERE transaction_id = ?", (get_user_id(user_name), ))

    conn.commit()
    conn.close()

    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (user_name,))

    conn.commit()
    conn.close()

    

    return
