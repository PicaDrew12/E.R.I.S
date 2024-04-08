import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_and_save(query, file_name):
    try:
        # Perform Google search
        search_results = search(query, num=5, stop=5)

        # Iterate through search results
        for url in search_results:
            try:
                # Fetch webpage content
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    body_content = soup.find('body').text.replace("\n"," ")

                    # Check if content is not too short
                    if len(body_content) > 1000:
                        # Save content to a text file
                        with open(file_name, 'w', encoding='utf-8') as file:
                            file.write(body_content)
                        print(f"Content saved from {url}")
                        return
                    else:
                        print(f"Content from {url} is too short, trying next URL...")
            except Exception as e:
                print(f"Error accessing {url}: {e}")
        print("No valid URL found or all content too short.")
    except Exception as e:
        print(f"Error searching: {e}")

# Example usage
query = "apple pie recipie"
file_name = "tests/web.txt"
search_and_save(query, file_name)
