import sqlite3
import json

def open_file() -> dict:
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS users (
              username TEXT UNIQUE NOT NULL,
              password BLOB NOT NULL, 
              money REAL,
              user_currency TEXT NOT NULL,
              other_currencies TEXT NOT NULL,
              income REAL,
              goal TEXT)""")
    
    c.execute("SELECT * FROM users")
    data = {row["username"]: {key: value for key, value in dict(row).items() if key != row["username"]} for row in c.fetchall()}
    for key in data:
        data[key]["other_currencies"] = json.loads(data[key]["other_currencies"])
    
    conn.commit()
    conn.close()

    return data


def save_file(data: dict, user_name: str) -> None:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS users (
              username TEXT UNIQUE NOT NULL,
              password BLOB NOT NULL, 
              money REAL,
              user_currency TEXT NOT NULL,
              other_currencies TEXT NOT NULL,
              income REAL,
              goal TEXT)""")
    stored_data: dict = open_file()

    if user_name in stored_data:
        c.execute("DELETE FROM users WHERE username = ?", (user_name,))
    
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
def delete_user(user_name: str) -> None:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (user_name,))

    conn.commit()
    conn.close()

    return
