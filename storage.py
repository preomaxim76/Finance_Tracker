import sqlite3
import json
from time import sleep

def open_file() -> dict:
    conn = sqlite3.connect("Python/TProjects/Finance_Tracker/database.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS users (
              username TEXT UNIQUE,
              password BLOB, 
              money REAL,
              user_currency TEXT,
              other_currencies TEXT)""")
    
    c.execute("SELECT * FROM users")
    data = {row["username"]: {key: value for key, value in dict(row).items() if key != row["username"]} for row in c.fetchall()}
    for key in data:
        data[key]["other_currencies"] = json.loads(data[key]["other_currencies"])
    
    conn.commit()
    conn.close()

    return data


def save_file(data: dict, user_name: str) -> None:
    conn = sqlite3.connect("Python/TProjects/Finance_Tracker/database.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS users (
              username TEXT UNIQUE,
              password BLOB, 
              money REAL,
              user_currency TEXT,
              other_currencies TEXT)""")
    stored_data: dict = open_file()

    if user_name in stored_data:
        c.execute("DELETE FROM users WHERE username = ?", (user_name,))
    
    password = data["password"]
    money = data["money"]
    user_currency = data["user_currency"]
    other_currencies = json.dumps(data["other_currencies"])
    c.execute("INSERT INTO users (username, password, money, user_currency, other_currencies) VALUES (?, ?, ?, ?, ?)", (user_name, password, money, user_currency, other_currencies))
    
    conn.commit()
    conn.close()

    return
def delete_user(user_name: str) -> None:
    conn = sqlite3.connect("Python/TProjects/Finance_Tracker/database.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (user_name,))

    conn.commit()
    conn.close()

    return
