import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
import subprocess
from datetime import datetime
import pyautogui
import time
import webbrowser
import subprocess

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 250)
        
        # GUI
        self.root = tk.Tk()
        self.label = tk.Label(text="No Commands", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.listen_for_commands, daemon=True).start()
        self.root.mainloop()
    
    def listen_for_commands(self):
        with sr.Microphone() as source:
            print("Listening for commands")
            while True:
                try:
                    # Listen for a command
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    self.label.config(text="You said: "+ command, font=("Arial", 60, "bold"))
                    
                    self.process_command(command)
                except sr.UnknownValueError:
                    print("Sorry, I did not understand that.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
    def process_command(self, command):
        if "click" in command:
            # Click the button based on a keyword (simple example)
            button_name = command.split("click")[-1].strip()
            # click_button(button_name)
        elif "search" in command:
            search_term = command.split("search")[-1].strip()
            self.searchWebsite(search_term)
        elif "open" in command:
            app_name = command.split("open")[-1].strip()
            self.openApp(app_name)
        elif "hello" in command:
            self.speaker.say("Hello there")
            self.speaker.runAndWait()
        elif "look up" in command:
            term = command.split("look up")[-1].strip()
            self.lookUp(term)
            
    
    def openApp(self, app):
        print("opening " + app)
        appList = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "firefox": "firefox",
        }

        appCommand = appList.get(app.lower())
        if appCommand:
            subprocess.Popen(appCommand)
        else:
            try:
                print("Cannot find app")
            except Exception as e:
                print(f"Failed to open {app}: {e}")
    
    def searchWebsite(self, site):
        print(f"Searching for: {site}")
        webbrowser.open_new_tab(site)
        
    def lookUp(self, term):
        print(f"Searching for: {term}")
        url = f'https://www.google.com/search?q={term}'
        webbrowser.open(url)
        
if __name__ == "__main__":
    VoiceAssistant()
