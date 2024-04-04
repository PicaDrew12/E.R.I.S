import requests

def update_url(endpoint, new_url):
    url = 'https://eris-api-v1.000webhostapp.com/update_api.php'  # Replace 'your-server-address' with the actual server address
    data = {'endpoint': endpoint, 'new_url': new_url, 'action': 'update'}
    response = requests.post(url, data=data)
    print(response.text)

# Example usage:
endpoint = 'voice_recognition'
new_url = 'baia mare'
update_url(endpoint, new_url)
