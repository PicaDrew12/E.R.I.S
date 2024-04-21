from openai import OpenAI
client = OpenAI(api_key="sk-proj-t1OI0ZgZ5dWeAU14l5T9T3BlbkFJwQSbiFPqzkQqd8Knc2aa")
import json



def ai_text_gen(userMessage, character,chatHistory,useOpenAI):
    if useOpenAI:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        )
        print(5)
    else:
        if(character=="TD"):
            character = "TopicDetector"
        elif(character == "AS"):
            character = "Eris"
        elif(character == "ISQ"):
            character = "InternetSearchQuery"
        elif(character == "ISS"):
            character = "InternetSumarizer"
        elif(character == "MTE"):
            character = "MusicTopicExtractor"
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

        response = requests.post(url, headers=headers, json=data, verify=True)
        assistant_message = response.json()['choices'][0]['message']['content']
        #history.append({"role": "assistant", "content": assistant_message})
        print(assistant_message)
        return assistant_message
    



with open('conversations/2024-04-06.txt', 'r') as file:
    # Read the entire content of the file
    convo = file.read()
    
chatHistory = json.loads(convo)
print("j")
print(chatHistory)

