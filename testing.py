import json
import requests
def retrieve_url(endpoint):
    url = 'https://eris-api-v1.000webhostapp.com/update_api.php'
    data = {'endpoint': endpoint, 'action': 'retrieve'}
    
    try:
        # Attempt to make the API call
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an error for non-successful status codes
        retrieved_url = response.text

        # Save the retrieved URL locally in urls.json
        with open('urls.json', 'r+') as file:
            urls_data = json.load(file)
            urls_data['api_urls'][endpoint] = retrieved_url
            file.seek(0)
            json.dump(urls_data, file, indent=4)

    except requests.RequestException as e:
        print(f"Error retrieving URL for '{endpoint}' from API:", e)
        # If the API call fails, return the URL already saved in the JSON file
        with open('urls.json', 'r') as file:
            urls_data = json.load(file)
            retrieved_url = urls_data['api_urls'].get(endpoint)

            if retrieved_url is None:
                print(f"No URL found for '{endpoint}' in the JSON file.")
                return None

    return retrieved_url


def ai_text_gen(userMessage, character,chatHistory):
    if(character=="TD"):
        character = "TopicDetector"
    elif(character == "AS"):
        character = "Eris"
    else:
        character = "Example"
        
                      
    first_api_url = retrieve_url(endpoint="text_gen")
    url = first_api_url+ "/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    history = chatHistory


    user_message = userMessage
    history.append({"role": "user", "content": user_message})
    data = {
        "mode": "chat",
        "character": character,
        "messages": history,
        
    }

    response = requests.post(url, headers=headers, json=data, verify=True)
    assistant_message = response.json()['choices'][0]['message']['content']
    #history.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message


ai_text_gen("WHATS THE TIME", "TD",[])  # Testing the function with a sample