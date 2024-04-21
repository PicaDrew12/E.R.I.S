import json
import datetime
import os
def read_history_from_file():
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join("conversations", current_date + ".txt")
        if os.path.getsize(filename) == 0:
            return []
        with open(filename, "r", encoding="utf-8") as file:
            
            history = json.load(file)
        return history
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []



print(json.dumps(read_history_from_file()))