import json

# Define the file path
file_path = 'history.json'

# Load existing JSON data from the file
try:
    with open(file_path, 'r') as file:
        history = json.load(file)
except FileNotFoundError:
    # If the file doesn't exist, start with an empty list
    history = []

# Append new data to the `history` list
new_data = {"role": "assistant", "content": "New text"}
history.append(new_data)

# Write the updated `history` list back to the JSON file
with open(file_path, 'w') as file:
    json.dump(history, file)

print("New data appended to", file_path)
