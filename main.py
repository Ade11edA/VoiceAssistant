import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk
import subprocess
from datetime import datetime

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 350)

        # GUI
        self.root = tk.Tk()
        self.label = tk.Label(text="Inactive", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.runAssistant, daemon=True).start()
        self.root.mainloop()



    def wakeUp(self):
        with sr.Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = self.recognizer.listen(mic)
            try:
                if 'start' in self.recognizer.recognize_google(audio).lower():
                    print("I'm up")
                    self.label.config(text="active")
                    return True
            except sr.UnknownValueError:
                self.label.config(text="inactive")
                print("Could not understand audio")
            except sr.RequestError:
                self.label.config(text="inactive")
                print("Could not request results from service")
        return False

    def runAssistant(self):
        while True:
            if self.wakeUp():
                self.speaker.say("Hello there")
                self.speaker.runAndWait() 
                with sr.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    try:
                        command = self.recognizer.recognize_google(audio)
                        print(f"You said: {command}")
                        if "what time is it" in command.lower():
                            self.speaker.say(datetime.now())
                        if "open calculator" in command.lower():
                            self.openApp("calc.exe")
                            
                    except sr.UnknownValueError:
                        print("Could not understand the command")
                    except sr.RequestError:
                        print("Could not request results from service")
                        
    def openApp(self, appName):
        try:
            subprocess.Popen(appName)
            self.speaker.say(f"Opening {appName.split('.')[0]}")
            self.speaker.runAndWait()
        except Exception as e:
            print(f"Failed to open {appName}: {e}")

if __name__ == "__main__":
    VoiceAssistant()
