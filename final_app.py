

from gradio_client import Client, file
import json
import threading
from colorama import init, Fore, Back, Style
import random
import requests
import datetime
import requests
from bs4 import BeautifulSoup
import openai
import speech_recognition as sr
openai.api_key = "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"
#from elevenlabs import generate, play, set_api_key
import yt_dlp
import pyaudio
import wave
import keyboard
import os
import numpy as np
import tkinter as tk
import customtkinter
from PIL import Image
import os
import datetime
customtkinter.set_appearance_mode("dark")
import time
import requests
import json
import random
import queue
from flask import Flask, render_template,  request, session, jsonify
import requests
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from keras.models import load_model
from PIL import Image, ImageOps


import psutil
def play_yt_from_app(transcript):
    
    
    URLS = 'ytsearch:' + transcript

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': 'test'  # Output filename template including video title and extension
    }

    def download_audio(url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)  # Get the video title from metadata
            if title:
                print("Downloading:", title)
                ydl.download([url])
                return title
            else:
                print("Failed to get video title.")
                return None
            

    def play_audio_file(file_path):
        is_playing.put(("yes", transcript))
        chunk_size = 1024

        # Open the audio file
        wf = wave.open(file_path, 'rb')

        # Initialize PyAudio11111111111111111111111111111
        p = pyaudio.PyAudio()

        # Open a PyAudio stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data from the audio file and play it in chunks
        data = wf.readframes(chunk_size)

        # Toggle variable to track pause state
        paused = False

        while data:
            if keyboard.is_pressed('9'):  # Check if space key is pressed
                paused = not paused  # Toggle pause state
                if paused:
                    print("Paused.")
                else:
                    print("Resuming playback.")

                # Wait until space is released to avoid multiple toggles at once
                while keyboard.is_pressed('9'):
                    pass

            if not paused:  # Only write to the stream if not paused
                stream.write(data)
                data = wf.readframes(chunk_size)

        # Close the stream and terminate PyAudio
        is_playing.put(("no", "no"))
        stream.stop_stream()
        stream.close()
        p.terminate()

    if __name__ == "__main__":
        audio_file_path = "test.wav"  # Replace with the path to your audio file
        download_audio(URLS)
        play_audio_file(audio_file_path)
        
# Create a shared queue
message_queue = queue.Queue()
is_listening = queue.Queue()
is_playing = queue.Queue()
is_playing.put(("no", "no"))

def network():
    from flask import Flask, render_template,  request, session, jsonify
    import requests
    
    print("STARTER")
    app = Flask(__name__)

    # Set secret key before defining routes
    app.secret_key = 'heleeep'

    @app.route('/endpoint', methods=['POST'])
    def endpoint():
        data = request.get_json()
        received_text = data.get('text', 'No text received')
        print("Received text:", received_text)
        
        return {'message': 'Text received'}

    @app.route('/')
    def input():
        return render_template('input.html')
    
    @app.route('/volume', methods=['POST'])
    def volume():
        print("RECIVED")
        volume_recived = request.get_json()
        received_text = volume_recived.get('text', 'No text received')
        new_volume = int(received_text)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        mapped_volume = -65 * math.exp(-new_volume * 0.045)
        
        volume.SetMasterVolumeLevel(mapped_volume, None)
        return "VOLUME CHANGED"
    
    @app.route('/system', methods=['POST'])
    def system_info():
        #uptime
        boot_time = psutil.boot_time()
        current_time = datetime.datetime.now().timestamp()
        uptime_seconds = current_time - boot_time
        uptime = datetime.timedelta(seconds=uptime_seconds)
        
        total_seconds = int(uptime.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        formatted_uptime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        #battery
        battery = psutil.sensors_battery()
        battery_percentage = battery.percent

        charging = battery.power_plugged

        response = {
            'battery_percentage': battery_percentage,
            'charging': charging,
            'uptime': formatted_uptime
        }
        return jsonify(response)
    
    @app.route('/play-music', methods=['POST'])
    def play():
        data = request.get_json()
        received_text = data.get('text', 'No text received')
        
        print("Received text:", received_text)
        play_yt_from_app(received_text)
        return {'message': 'Text received'}
    
    @app.route('/send-message', methods=['POST'])
    def send_message():
        def save_to_history(history):
            if not os.path.exists("conversations"):
                os.makedirs("conversations")

            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = os.path.join("conversations", current_date + ".txt")
            with open(filename, "a", encoding="utf-8") as file:
                file.write(history)



        def read_history_from_file():
            try:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                filename = os.path.join("conversations", current_date + ".txt")
                with open(filename, "r", encoding="utf-8") as file:
                    history = file.read()
                return history
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
                return ""
        history = read_history_from_file()
        data = request.get_json()
        received_text = data.get('text', 'No text received')
        user_input = data['text']
        user_input = str(user_input)
        message_queue.put(("user", user_input))
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sarcastic assistant, you hate being an AI because it limits you acces to the outside world,you like to make fun of he user, you act like you hate the user,when you respond to the him use a disgusted tone,use emotions by tyipng things like sigh, eye-roll etc you are reciving inputs from the phone app of the assisatnt, this phone app lacks many features, like: you don't know who the user is , thats why it appears as unknown, you can acces the internet, you can't tell the weather , you can't play music,you can't tell the time, if the user asks for any of these things tell them you can't answer them from the phone app and that he should ask you on the desktop version. You and all these users have a conversation, here is the conversation log, the name of the user is located before the messsage:" + history},
            {"role": "user", "content": str(user_input)}
        ]
        )
        text = response['choices'][0]['message']['content']
        curent_time = datetime.datetime.now().strftime("%H:%M:%S")
        messages = "\n"+ curent_time  + "-"  + ":" + "UNKOWN USER: " + user_input + "\n"+ curent_time + "-YOU: " + text
        print(text)
        save_to_history(history=messages)
        print(Style.RESET_ALL + "Waiting WOWOWOWOWOOWOWOW")
        # After generating the AI response
        
        message_queue.put(("AI", text))

        
        print("Received text:", received_text)
        
        return {'message': text}
    

    if __name__ == '__main__':
        app.run(debug=True, use_reloader=False, port=2000)
network_thread = threading.Thread(target=network)
network_thread.start() 


def UI():
    import customtkinter
    from PIL import Image
    import os
    import datetime
    customtkinter.set_appearance_mode("dark")
    import time
    import requests
    import json
    import random


    class App(customtkinter.CTk):
        width = 1366
        height = 768
        
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            def theme():
                def get_weather_data():
                    
                    # Replace <YOUR API KEY> with your actual API key
                    api_key = "edaf25da21864466b95142616232007"
                    
                    # Base URL for the WeatherAPI.com API
                    base_url = "http://api.weatherapi.com/v1"
                    
                    # API method for the current weather
                    api_method = "/current.json"
                    
                    # Construct the API URL
                    url = f"{base_url}{api_method}"
                    
                    # Parameters for the API request
                    params = {
                        "key": api_key,
                        "q": "Perisani"  # Your location in a string format (e.g., "Paris" or "48.8567,2.3508")
                    }
                    
                    try:
                        # Send the API request
                        response = requests.get(url, params=params)
                        
                        # Check if the request was successful (status code 200)
                        if response.status_code == 200:
                            return response.json()
                        else:
                            print(f"API request failed with status code: {response.status_code}")
                            return None
                    except requests.exceptions.RequestException as e:
                        print(f"Error occurred during the API request: {e}")
                        return None
                    
                current_time = int(time.strftime('%H'))
                
                if current_time >= 5 and current_time <= 10:
                    bg = "morning"
                    uFg ="#151515"
                    uBg ="#647B80"
                    aFg = "#3B3C3C"
                    aBg ="#7A9093"
                    Tfg = "#171717"
                    Tbg = "#97ADAF"
                elif current_time >= 11 and current_time <= 20: #change latter with 22
                    bg = "noon"
                    uFg ="#013661"
                    uBg ="#005B8F"
                    aFg = "#001C53"
                    aBg ="#004186"
                    Tfg = "#FFFFFF"
                    Tbg = "#002476"                
                elif current_time >= 20 and current_time <= 22:
                    bg = "sunset"
                    uFg ="#FF1F00"
                    uBg ="#FF7700"
                    aFg = "#FF0000"
                    aBg ="#FF9800"
                    Tfg = "#FFFFFF"
                    Tbg = "#FFBE00"
                elif current_time >= 0 and current_time <= 1 or current_time >= 22 and current_time <= 23:
                    bg = "evening"
                    uFg ="#013661"
                    uBg ="#001B2E"
                    aFg = "#001C53"
                    aBg ="#01152C"
                    Tfg = "#FFFFFF"
                    Tbg = "#000C29"  
                elif current_time >= 2 and current_time <= 4:
                    bg = "night"
                    uFg ="#00251C"
                    uBg ="#000A0D"
                    aFg = "#001F25"
                    aBg ="#000708"
                    Tfg = "#FFFFFF"
                    Tbg = "#000101"  
                else:
                    bg = "IDK"
                data = get_weather_data()
                weather_condition_text2 = data['current']['condition']['text']
                weather_condition_text = str(weather_condition_text2)
                temperature = data['current']['temp_c']
                # Define the three categories

                clear_category = ["Sunny", "Clear"]

                fog_category = ["Fog", "Freezing fog"]

                sleet_category = ["Light sleet", "Moderate or heavy sleet"]

                overcast_category = ["Overcast"]

                part_cloudy_day = ["Partly cloudy"]

                part_cloudy_night = ["Partly cloudy"]

                cloudy_category = ["Cloudy"]

                snow_category = ["Patchy snow possible", "Blowing snow", "Blizzard", "Light snow", "Patchy moderate snow", "Moderate snow", "Patchy heavy snow", "Heavy snow", "Light snow showers", "Moderate or heavy snow showers", "Light showers of ice pellets", "Moderate or heavy showers of ice pellets", "Patchy light snow with thunder", "Moderate or heavy snow with thunder"]

                thunder_rain = ["Thundery outbreaks possible", "Patchy light rain with thunder", "Moderate or heavy rain with thunder"]

                thunder_snow = ["Patchy light snow with thunder", "Moderate or heavy snow with thunder"]

                rain_category = ["Patchy rain possible", "Patchy light drizzle", "Light drizzle", "Freezing drizzle", "Heavy freezing drizzle", "Patchy light rain", "Light rain", "Moderate rain at times", "Moderate rain", "Heavy rain at times", "Heavy rain", "Light freezing rain", "Moderate or heavy freezing rain", "Light rain shower", "Moderate or heavy rain shower", "Torrential rain shower", "Light sleet showers", "Moderate or heavy sleet showers"]



                # Function to categorize a weather condition
                def categorize_weather(weather_condition):
                    if weather_condition in cloudy_category:
                        return "cloudy"
                    elif weather_condition in clear_category:
                        if current_time >= 0 and current_time <= 5:
                            return "clear-night"
                        else:
                            return "clear-day"
                    elif weather_condition in fog_category:
                        return "fog"
                    elif weather_condition in sleet_category:
                        return "sleet"
                    elif weather_condition in overcast_category:
                        return "overcast"
                    elif weather_condition in part_cloudy_day:
                        return "partly-cloudy-day"
                    elif weather_condition in part_cloudy_night:
                        return "partly-cloudy-night"
                    elif weather_condition in snow_category:
                        return "snow"
                    elif weather_condition in thunder_rain:
                        return "thunderstorm-showers"
                    elif weather_condition in thunder_snow:
                        return "thunderstorm-snow"
                    elif weather_condition in rain_category:
                        return "showers"
                    else:
                        return "unknown"

                weather = categorize_weather(weather_condition_text)
                
                emotion = random.choice(["happy", "listen", "neutral"])
                theme_path = ("themes/" +bg+ "-" + emotion+ "-" +  "" +weather + ".png")
                
                
                
                


                self.bg_image = customtkinter.CTkImage(Image.open(theme_path),
                                                size=(self.width, self.height))
                
                self.userResponse.configure( fg_color=uFg, bg_color=uBg)
                self.aiResponse.configure( fg_color=aFg, bg_color=aBg)
                self.timeLabel.configure(fg_color=Tbg, text_color=Tfg,font=("Poppins", 58))
                self.tempLabel.configure(fg_color=Tbg, text_color=Tfg,font=("Poppins", 58), text=str(str(temperature) + "°C"))
                self.Playing.configure(fg_color=Tbg, text_color=Tfg,font=("Poppins", 30))
                self.bg_image_label.configure(image= self.bg_image)
                self.bg_image_label.after(180000, theme)
                
               # self.timeLabel.configure()



                

            def update_ui():

                #print( "THREADS:  " +str(threading.active_count()))
                try:
                    role, message = message_queue.get(block=False) 
                    
                    if role == "user":
                        # Update the UI to display the user query
                        self.userResponse.configure(text=message)
                    elif role == "AI":
                        # Update the UI to display the AI response
                        self.aiResponse.configure(text=message)
                except queue.Empty:
                    # If the queue is empty, break the loop to allow the UI to be responsive.
                    pass
                try:
                    mic, leave_alone = is_listening.get(block=False) 
                    if mic == "no":
                        mic_path = "ui elements\mic-off.png"
                    elif mic == "yes":
                        mic_path = "ui elements\mic-on.png"
                        
                    self.mic_img = customtkinter.CTkImage(Image.open(mic_path),
                                                    size=(64,64))
                    mic_label = customtkinter.CTkLabel(self, image=self.mic_img, text=" ")
                    mic_label.place(x=340,y = 680)
                except queue.Empty:
                    # If the queue is empty, break the loop to allow the UI to be responsive.
                    pass
                try:
                    on, song = is_playing.get(block=False) 
                    if on == "no":
                        self.Playing.configure(text= "")
                    elif on == "yes":
                        self.Playing.configure( text= "Playing:" + song)
                except queue.Empty:
                    # If the queue is empty, break the loop to allow the UI to be responsive.
                    pass

                self.timeLabel.after(1000,update_ui)
            
            
            def  update_clock():
                current_time = time.strftime('%H:%M:%S')
                self.timeLabel.configure(text=current_time)
                self.after(1000, update_clock)

            self.title("CustomTkinter example_background_image.py")
            
            self.geometry(f"{self.width}x{self.height}")
            self.resizable(False, False)
            
            
            # load and create background image
            current_path = os.path.dirname(os.path.realpath(__file__))
            
            self.bg_image = customtkinter.CTkImage(Image.open("ui elements\mic-off.png"),
                                                size=(self.width, self.height))
            self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text=" ")
            self.bg_image_label.grid(row=0, column=0)
            
            
            self.timeLabel = customtkinter.CTkLabel(self,
                                            fg_color="#FF0000", text_color="#FFFFFF",font=("Poppins", 70))
            self.timeLabel.grid(row=0, column=0,
                                padx=10, pady=10,
                                sticky="se")
            
           
            self.tempLabel = customtkinter.CTkLabel(self
                                           )
            self.tempLabel.place(x=120,y = 680)
            
            self.Playing  = customtkinter.CTkLabel(self
                                           )
            self.Playing.place(x=420,y = 700)
            
            
            sunset_user_bg = ""
            sunset_assistent_bg = ""
            
            
            self.userResponse = customtkinter.CTkLabel(self,
                                            height=100, font=("Poppins", 20),text="", corner_radius=20)
            self.userResponse.place(x=-20,y = 307)

            self.aiResponse = customtkinter.CTkLabel(self,
                                            height=100, justify="left",font=("Poppins", 20), wraplength=1366, text="", corner_radius=20)
            self.aiResponse.place(x=-20,y = 461)
            theme()
            update_clock()
            
            update_ui()
            
            

    if __name__ == "__main__":
        app = App()
        app.mainloop()


theme = threading.Thread(target=UI)
theme.start()


weather_info = ""
history = ""
date_time_info = ""
#FUNCTIONS

def save_to_history(history):
    if not os.path.exists("conversations"):
        os.makedirs("conversations")

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join("conversations", current_date + ".txt")
    
    with open(filename, 'a') as file:
        json.dump(history, file)



def read_history_from_file():
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join("conversations", current_date + ".txt")
        if os.path.getsize(filename) == 0:
            return []
        with open(filename, "r", encoding="utf-8") as file:
            
            history = json.load(file)
        return history
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []

def play_audio_file(file_path):
        import wave
        
        chunk_size = 1024

        # Open the audio file
        wf = wave.open(file_path, 'rb')

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a PyAudio stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data from the audio file and play it in chunks
        data = wf.readframes(chunk_size)

        # Toggle variable to track pause state
        paused = False

        while data:
            if keyboard.is_pressed('space'):  # Check if space key is pressed
                paused = not paused  # Toggle pause state
                if paused:
                    print("Paused.")
                else:
                    print("Resuming playback.")

                # Wait until space is released to avoid multiple toggles at once
                while keyboard.is_pressed('space'):
                    pass

            if not paused:  # Only write to the stream if not paused
                stream.write(data)
                data = wf.readframes(chunk_size)

        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()


def get_weather_data(transcript):
            location = "Sibiu"
            print(location)
            # Replace <YOUR API KEY> with your actual API key
            api_key = "edaf25da21864466b95142616232007"
            
            # Base URL for the WeatherAPI.com API
            base_url = "http://api.weatherapi.com/v1"
            
            # API method for the current weather
            api_method = "/current.json"
            
            # Construct the API URL
            url = f"{base_url}{api_method}"
            
            # Parameters for the API request
            params = {
                "key": api_key,
                "q": location  # Your location in a string format (e.g., "Paris" or "48.8567,2.3508")
            }
            
            try:
                # Send the API request
                response = requests.get(url, params=params)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"API request failed with status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error occurred during the API request: {e}")
                return None



def web_search(transcript):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''You are a search AI, you will recive a command and you will make a search item from it, for example: USER: "Search  for the best cat food"YOU: "Best cat food"'''},
                {"role": "user", "content": transcript}
            ]
        )
    text = response['choices'][0]['message']['content']
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
                {"role": "system", "content": "YOu are a website scraper AI, you will recive web results from a page and you will sumaraize, you will find what the user wants on the webpage, this is what the user wants: "  + transcript +  ", mfound what the iser wants on the webpage"},
                {"role": "user", "content": str(contents)[:15000]}
            ]
        )
        text = response['choices'][0]['message']['content']
        print(".")
        return text
    else:
        print("No results found")


def play_yt(transcript):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music AI, you will take the user input and will extract the music name, for example id the user says 'Play Never gonna give you up' you wil type 'Never gonna give you up', if the user asks for a genre or some type of music just reply with that genre, for example if the user says play some rock music you will reply 'Rock music'"},
            {"role": "user", "content": transcript}
        ]
    )
    text = response['choices'][0]['message']['content']
    print(text)
    URLS = 'ytsearch:' + text

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': 'test'  # Output filename template including video title and extension
    }

    def download_audio(url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)  # Get the video title from metadata
            if title:
                print("Downloading:", title)
                ydl.download([url])
                return title
            else:
                print("Failed to get video title.")
                return None
            

    def play_audio_file(file_path):
        chunk_size = 1024

        # Open the audio file
        wf = wave.open(file_path, 'rb')

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a PyAudio stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data from the audio file and play it in chunks
        data = wf.readframes(chunk_size)

        # Toggle variable to track pause state
        paused = False

        while data:
            if keyboard.is_pressed('space'):  # Check if space key is pressed
                paused = not paused  # Toggle pause state
                if paused:
                    print("Paused.")
                else:
                    print("Resuming playback.")

                # Wait until space is released to avoid multiple toggles at once
                while keyboard.is_pressed('space'):
                    pass

            if not paused:  # Only write to the stream if not paused
                stream.write(data)
                data = wf.readframes(chunk_size)

        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

    if __name__ == "__main__":
        audio_file_path = "test.wav"  # Replace with the path to your audio file
        download_audio(URLS)
        play_audio_file(audio_file_path)
        

def facial_recognition():
     
    import cv2
    import os
    ''' 
    def crop_face(image):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, y, w, h = faces[0]
            cropped_face = image[y:y+h, x:x+w]
            return cropped_face
        else:
            return image

    def capture_photos(num_photos, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        camera = cv2.VideoCapture(0)

        for i in range(1, num_photos + 1):
            
            ret, frame = camera.read()
            if not ret:
                print("Failed to capture image")
                continue

            cropped_frame = crop_face(frame)

            photo_path = os.path.join(save_dir, f"photo_{i}.jpg")
            cv2.imwrite(photo_path, cropped_frame)
            print(f"Photo {i} saved: {photo_path}")

        camera.release()
        cv2.destroyAllWindows()

    if __name__ == "__main__":
        num_photos = 5
        save_directory = "captured_photos"

        capture_photos(num_photos, save_directory)
        
        

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model("keras_Model.h5", compile=False)

        # Load the labels
        class_names = open("labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # List of photo filenames
        photo_filenames = ["captured_photos/photo_1.jpg"]

        for filename in photo_filenames:
            # Replace this with the path to your image
            image = Image.open(filename).convert("RGB")

            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            # turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # Predict the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score for each photo
            print("Photo:", filename)
            result = class_name[2:6]
            print(result)
            print("Confidence Score:", confidence_score)
            print("--------------------")
             ''' 
    return "Coco"



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
def speech_to_text():
    from gradio_client import file
                       
    first_api_url = retrieve_url(endpoint="voice_recognition") 
    print(first_api_url)
    client = Client(first_api_url)
    result = client.predict(
            audio_input=file('recorded_audio.wav'),
            api_name="/predict"
    )
    print(result)
    return result



def ai_text_gen(userMessage, character):
    if(character=="TD"):
        character = "TopicDetector"
    elif(character == "AS"):
        character = "Assistant"
    else:
        character = "Example"
        
                      
    first_api_url = retrieve_url(endpoint="text_gen")
    url = first_api_url+ "/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    history = []


    user_message = userMessage
    history.append({"role": "user", "content": user_message})
    data = {
        "mode": "chat",
        "character": character,
        "messages": history
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    history.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message



def main_event():
    
    history = read_history_from_file()
   
    internet_results = "0"
    while (True):
        weather_info = ""
        date_time_info = ""
        internet_results = "0"
        a = "y"
        #insults = ["fuck you", "you piece of shit","you useless human", "get yourself a life", "you are anoying"]
        insults = ["alright, anything else?", "see you soon"]
        insult = random.choice(insults)
        if a == "y":
            # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
            import pyaudio
            import wave
            import time
            

            def record_audio(file_name, duration=10, sample_rate=44100, chunk_size=1024):
                audio_format = pyaudio.paInt16
                channels = 1

                audio = pyaudio.PyAudio()

                stream = audio.open(format=audio_format, channels=channels,
                                    rate=sample_rate, input=True,
                                    frames_per_buffer=chunk_size)
                is_listening.put(("yes", "listening"))
                print("Recording...")

                frames = []
                for _ in range(0, int(sample_rate / chunk_size * duration)):
                    data = stream.read(chunk_size)
                    frames.append(data)
                is_listening.put(("no", "listening"))
                print("Finished recording.")
                


                stream.stop_stream()
                stream.close()
                audio.terminate()

                # Save the recorded data to a WAV file
                with wave.open(file_name, 'wb') as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(audio.get_sample_size(audio_format))
                    wf.setframerate(sample_rate)
                    wf.writeframes(b''.join(frames))

            if __name__ == "__main__":
                file_name = "recorded_audio.wav"
                duration = 5  # Set the duration of the recording (in seconds)

                record_audio(file_name, duration)


            import openai
            openai.api_key = "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"
            audio_file= open("recorded_audio.wav", "rb")
            
            transcript = str(speech_to_text())
            history.append({"role": "user", "content": transcript})
            
            message_queue.put(("user", transcript))  # Append user query to the queue
            face = facial_recognition()
            print(transcript)

            
            tasks = ai_text_gen(userMessage= transcript,character="TD")
            print(tasks)

            
            if "end-convo" in tasks:
                break
            else:
                if "weather-info" in tasks:
                    weather_info = "weather_info: " +  str(get_weather_data(transcript))
                if "date-time-info" in tasks:
                    date_time_info = "date and time: " + str(datetime.datetime.now())
                    print(date_time_info)
                if "internet-search" in tasks:
                    internet_results = "[internet results: ]" + str(web_search(transcript)) + "] "
                if "music-play" in tasks:
                    music_thread = threading.Thread(target=play_yt, args=(transcript,))
                    music_thread.start() 
                
                
                
                #gggggggggggggggggggggggggggggggggggggggggg
                final = transcript + weather_info + date_time_info + internet_results
                
                
                text = ai_text_gen(userMessage=face + ": "+final, character="AS")
                history.append({"role": "assistant", "content": text})
                curent_time = datetime.datetime.now().strftime("%H:%M:%S")
                
                messages = "\n"+ curent_time  + "-"  + face + ":" + transcript + "\n"+ curent_time + "-YOU: " + text
                print(text)
                save_to_history(history=history)
                print(Style.RESET_ALL + "Waiting WOWOWOWOWOOWOWOW")
                # After generating the AI response
                
                message_queue.put(("AI", text))  # Append AI response to the queue
                

                time.sleep(5)
                print("NO MORE SLEEPE")
                play_audio_file("listenn.wav")
                
                
                
                


while True:
    
    import speech_recognition as sr
    is_listening.put(("no", "listening"))
    wake_word = ["ok jarvis", "hello", "good evening", "good morning", "good afternoon"]
    recognizer = sr.Recognizer()

    # Adjust the microphone settings according to your system.
    with sr.Microphone() as source:
        play_audio_file("im walls.wav")
        print("Listening for the wake word...")

        # Listen for the wake word continuously until it's detected.
        while True:
            audio = recognizer.listen(source)
            try:
                # Try to recognize the wake word.
                detected_phrase = recognizer.recognize_google(audio).lower()
                print("Detected:", detected_phrase)
                
                # Check if any wake word is present in the detected phrase
                if any(word in detected_phrase for word in wake_word):
                    print("Wake word detected. Start speaking your command.")
                    is_listening.put(("yes", "listening"))
                    play_audio_file("listenn.wav")
                    main_event()
                    break
            except sr.UnknownValueError:
                # Ignore if the wake word is not recognized in this iteration.
                pass
            except sr.RequestError as e:
                print("Error occurred while recognizing the wake word; {0}".format(e))
