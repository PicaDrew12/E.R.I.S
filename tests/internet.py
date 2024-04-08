

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
from PIL import Image, ImageOps


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



def ai_text_gen(userMessage, character,chatHistory):
    if(character=="TD"):
        character = "TopicDetector"
    elif(character == "AS"):
        character = "Eris"
    elif(character == "ISQ"):
        character = "InternetSearchQuery"
    elif(character == "MTE"):
        character = "MusicTopicExtractor"
    elif(character == "ISS"):
        character = "InternetSumarizer"
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



def play_yt(transcript):
    
    text = ai_text_gen(userMessage=transcript,character="MTE",chatHistory=[])
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
        







play_yt("Play Albert NBN Ter")