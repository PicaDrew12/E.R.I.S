import os
import fnmatch
print("TEST")
def search_text_in_files(directory, text):
    directory = os.path.normpath(directory)  # Convert Windows path to Python compatible path
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding="utf-8") as file:
                    for line_num, line in enumerate(file, start=1):
                        if text in line:
                            print(f"Found '{text}' in file: {filepath}, line {line_num}:")
                            print(line.strip())

# Example usage
directory_to_search = r'F:\Github\gradio'  # Replace this with the directory path you want to search
search_text = 'Colab notebook detected. This cell will run indefinitely so that you can see errors and logs.'  # Replace this with the text you want to search for
search_text_in_files(directory_to_search, search_text)
