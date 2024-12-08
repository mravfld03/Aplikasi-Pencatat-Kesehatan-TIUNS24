import os
import json
from datetime import date, datetime, timedelta

# Nama file database
DATABASE_FILE = "user_database.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def clean_old_data(user_data, username):
    if username not in user_data:
        return

    target = user_data[username].get("target", "Mingguan")
    days_limit = 7 if target == "Mingguan" else 30
    today = date.today()

    for category in ["data_harian_steps", "data_harian_sleep", "data_harian_water"]:
        if category in user_data[username]:
            keys_to_delete = [
                key for key in user_data[username][category]
                if (today - datetime.strptime(key, "%Y-%m-%d").date()).days > days_limit
            ]
            for key in keys_to_delete:
                del user_data[username][category][key]
    save_database(user_data)
