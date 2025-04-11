import os
import sys
import webbrowser
import datetime
import wikipedia
import pyttsx3
import speech_recognition as sr
import pywhatkit
import threading

class VoiceAssistant:
    def __init__(self):
        # Initialize voice engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        self.listening = True
        self.current_action = None

    def speak(self, audio):
        """Convert text to speech"""
        print(f"HandiMate: {audio}")
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        """Take microphone input and return as text"""
        with sr.Microphone() as source:
            try:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
                print("Recognizing...")
                query = self.recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {query}")
                return query.lower()
                
            except sr.WaitTimeoutError:
                print("Listening timeout")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                self.speak("I didn't catch that. Please repeat.")
                return None
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                self.speak("Speech service unavailable.")
                return None

    def play_music(self):
        """Play music from default directory"""
        music_dir = os.path.join(os.path.expanduser('~'), 'Music')
        if os.path.exists(music_dir):
            songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                self.speak("Playing music")
            else:
                self.speak("No music files found")
        else:
            self.speak("Music directory not found")

    def search_google(self):
        """Handle Google search without blocking"""
        self.speak("Your Google search?")
        query = self.take_command()
        if query:
            self.speak(f"Searching for {query}")
            threading.Thread(target=pywhatkit.search, args=(query,)).start()

    def search_youtube(self):
        """Handle YouTube search without blocking"""
        self.speak("What should I play?")
        query = self.take_command()
        if query:
            self.speak(f"Playing {query}")
            threading.Thread(target=pywhatkit.playonyt, args=(query,)).start()

    def search_wikipedia(self, query):
        """Search Wikipedia"""
        query = query.replace("who is", "").replace("who was", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("Multiple results found. Be more specific.")
        except wikipedia.exceptions.PageError:
            self.speak("No information found.")
        except Exception as e:
            print(f"Wikipedia error: {e}")
            self.speak("Search failed.")

    def open_program(self, path, name):
        """Open a program"""
        try:
            os.startfile(path)
            self.speak(f"Opening {name}")
        except Exception as e:
            print(f"Error opening program: {e}")
            self.speak(f"Can't open {name}")

    def close_program(self, process_name, name):
        """Close a program"""
        try:
            os.system(f"taskkill /IM {process_name} /F")
            self.speak(f"Closed {name}")
        except Exception as e:
            print(f"Error closing program: {e}")
            self.speak(f"Can't close {name}")

    def process_command(self, query):
        """Process and execute user commands"""
        if not query:
            return

        # Website commands
        website_commands = {
            'open youtube': 'https://youtube.com',
            'open google': 'https://google.com',
            'open kaggle': 'https://www.kaggle.com',
            'open chat': 'https://chat.openai.com',
            'open wikipedia': 'https://wikipedia.org',
            'open facebook': 'https://facebook.com',
            'open twitter': 'https://twitter.com',
            'open instagram': 'https://instagram.com',
            'open github': 'https://github.com',
            'open stackoverflow': 'https://stackoverflow.com',
        }

        for cmd, url in website_commands.items():
            if cmd in query:
                self.speak(f"Opening {cmd.replace('open ', '')}")
                webbrowser.open(url)
                return

        # Special commands
        if 'play music' in query:
            self.play_music()
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"Time is {str_time}")
        elif 'open code' in query:
            self.open_program("C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "VS Code")
        elif 'close code' in query:
            self.close_program("Code.exe", "VS Code")
        elif 'open notepad' in query:
            self.open_program("C:\\Windows\\System32\\notepad.exe", "Notepad")
        elif 'close notepad' in query:
            self.close_program("notepad.exe", "Notepad")
        elif 'open calculator' in query:
            self.open_program("C:\\Windows\\System32\\calc.exe", "Calculator")
        elif 'close calculator' in query:
            self.close_program("Calculator.exe", "Calculator")
        elif 'open paint' in query:
            self.open_program("C:\\Windows\\System32\\mspaint.exe", "Paint")
        elif 'close paint' in query:
            self.close_program("mspaint.exe", "Paint")
        elif 'search on google' in query:
            self.search_google()
        elif 'search on youtube' in query:
            self.search_youtube()
        elif 'who is' in query or 'what is' in query:
            self.search_wikipedia(query)
        elif 'quit' in query or 'exit' in query:
            self.speak("Shutting down")
            self.listening = False
        else:
            self.speak("Command not recognized")

    def startup(self):
        """Initialization sequence"""
        startup_messages = [
            "Booting systems",
            "Loading modules",
            "Checking resources",
            "Establishing connections",
            "Ready"
        ]

        for message in startup_messages:
            self.speak(message)

        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.speak(f"{greeting}, I am HandiMate. How can I assist?")

    def run(self):
        """Main execution loop"""
        self.startup()
        while self.listening:
            query = self.take_command()
            if query:
                self.process_command(query)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
