import requests
from bs4 import BeautifulSoup
import json

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
        "messages": history
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    #history.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message






def web_search(transcript):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''You are a search AI, you will recive a command and you will make a search item from it, for example: USER: "Search  for the best cat food"YOU: "Best cat food"'''},
                {"role": "user", "content": transcript}
            ]
        )
    text = response['choices'][0]['message']['content']
    text = ai_text_gen(userMessage=transcript,character="",chatHistory=[])
    api_key = "AIzaSyDng0fQh-6N6hNXmdgSRmnhhVVA1fk2RNk"
    search_engine_id = "128169a03d6034a8b"
    print(text)

    def search(query):
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
        return requests.get(url).json()

    def scrape(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text()
        return None

    query = text
    data = search(query)

    if data.get("items"):
        limit = 1  # Set the desired limit here
        count = 0
        for item in data["items"]:
            
            contents = scrape(item["link"])
            if contents:
                print(".")
                print(".")
            count += 1
            if count >= limit:
                break
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "YOu are a website scraper AI, you will recive web results from a page and you will sumaraize, you will find what the user wants on the webpage, this is what the user wants: "  + transcript +  ", find what the user wants on the webpage"},
                {"role": "user", "content": str(contents)[:15000]}
            ]
        )
        text = response['choices'][0]['message']['content']
        print(".")
        return text
    else:
        print("No results found")


print(web_search(input("HEY: ")))