import json
import requests

def retrieve_url(endpoint):
    url = 'https://eris-api-v1.000webhostapp.com/update_api.php'  # Replace 'your-server-address' with the actual server address
    data = {'endpoint': endpoint, 'action': 'retrieve'}
    response = requests.post(url, data=data)
    retrieved_url = response.text

    # Save the retrieved URL locally in urls.json
    with open('urls.json', 'r+') as file:
        urls_data = json.load(file)
        urls_data['api_urls'][endpoint] = retrieved_url
        file.seek(0)  # Move the cursor to the beginning of the file
        json.dump(urls_data, file, indent=4)  # Write the updated data back to the file

    return retrieved_url

# Example usage:
# Assuming you want to retrieve the URL for the 'text_gen' endpoint
retrieved_text_gen_url = retrieve_url('text_gen')
print("Retrieved URL for 'text_gen':", retrieved_text_gen_url)
