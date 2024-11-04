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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class VoiceAssistant:
    def __init__(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 250)
        self.listening = True
        
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
        if "wake up" in command:
            self.listening = True
            self.speaker.say("I am listening.")
            self.speaker.runAndWait()
        elif "stop" in command:
            self.listening = False
            self.speaker.say("I have stopped listening.")
            self.speaker.runAndWait()
        
        if self.listening:
            if "click" in command:
                elementName = command.split("click")[-1].strip()
                self.clickElement(elementName)
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
            elif "type" in command:
                term = command.split("type")[-1].strip()
                self.Dictate(term)
    
    def Dictate(self, term):
        pyautogui.typewrite(term)
            
    def clickElement(self, elementName):
        elements = self.driver.find_elements(By.XPATH, "//*")
        
        for element in elements:
            if element.text.lower() == elementName.lower():
                element.click()
        
    def openApp(self, app):
        print("opening " + app)
        appList = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "firefox": "firefox.exe",
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
        webbrowser.get('mozilla').open_new_tab(site) #doesn't seem to be opening default browser, will look into it later
        
    def lookUp(self, term):
        print(f"Searching for: {term}")
        url = f'https://www.google.com/search?q={term}'
        webbrowser.get('firefox').open(url) #https://stackoverflow.com/questions/47118598/python-how-to-open-default-browser-using-webbrowser-module
        
if __name__ == "__main__":
    VoiceAssistant()
