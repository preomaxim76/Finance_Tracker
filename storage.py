from json import load, dump

# Opens users_finances.json
def open_file() -> dict:
    with open("Python/TProjects/Finance_Tracker/users_finances.json", "r", encoding="utf-8") as json_file:
        dct: dict = load(json_file)
    return dct

# Saves user data -> users_finances.json
def save_file(data: dict, user_name: str) -> None:
    stored_data: dict = open_file()
    if user_name in stored_data:
        del stored_data[user_name]
    
    with open("Python/TProjects/Finance_Tracker/users_finances.json", mode="w", encoding="utf-8") as f:
        data = {user_name: data}
        data.update(stored_data)
        dump(data, f)

def delete_user(user_name: str) -> None:
    stored_data: dict = open_file()
    del stored_data[user_name]
    with open("Python/TProjects/Finance_Tracker/users_finances.json", mode="w", encoding="utf-8") as f:
        dump(stored_data, f)