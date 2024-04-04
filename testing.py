import requests
import json

# Function to retrieve the API URL
def retrieve_url(endpoint):
    url = 'https://eris-api-v1.000webhostapp.com/update_api.php'  # Replace 'your-server-address' with the actual server address
    data = {'endpoint': endpoint, 'action': 'retrieve'}
    response = requests.post(url, data=data)
    return response.text

# Load API URLs from JSON file
with open('urls.json', 'r') as file2:
    data = json.load(file2)
    first_api_url = data['api_urls']['text_gen']

# Load history from text file
try:
    with open('history.txt', 'r') as file:
        history = json.load(file)
except FileNotFoundError:
    history = []

# Construct URL for API call
endpoint = 'text_gen'
url = retrieve_url(endpoint) + "/v1/chat/completions"
print(url)

headers = {"Content-Type": "application/json"}

while True:
    # If history exists, print previous conversation
    if history:
        for entry in history:
            print(entry['role'] + ': ' + entry['content'])

    # Get user input
    user_message = input("> ")
    
    # Append user message to history
    history.append({"role": "user", "content": user_message})
    
    # Prepare data for API call
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": history
    }
    
    # Make API call
    response = requests.post(url, headers=headers, json=data, verify=True)
    
    # Get response from API
    assistant_message = response.json()['choices'][0]['message']['content']
    
    # Append assistant message to history
    history.append({"role": "assistant", "content": assistant_message})
    
    # Print assistant message
    print(assistant_message)
    
    # Write history to text file
    with open('history.txt', 'w') as file:
        json.dump(history, file)
