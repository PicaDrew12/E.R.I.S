import json

with open("user.json", "r") as user_prefs_file:
    user_prefs =json.loads(user_prefs_file.read()) 

print(user_prefs['name'])