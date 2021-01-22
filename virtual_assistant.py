import pyttsx3
import psutil
import speech_recognition as sr 
from GoogleNews import GoogleNews
import asyncio

engine = pyttsx3.init('sapi5') # sapi5 is for Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # voice id can be male(0) or female(1) 
    
class Hazel:
    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()
        
    def greeting(self):
        self.speak("Hello, I am Hazel, how may I assist you today?")
        
    def take_command(self):
        speech = sr.Recognizer()
        speech.energy_threshold = 3000
        with sr.Microphone() as source:
            speech.adjust_for_ambient_noise(source)
            print("Listening...")
            speech.pause_threshold = 1.0
            audio = speech.listen(source)
            try: 
                print("Recognizing...")     
                Query = speech.recognize_google(audio, language='en-in') 
                print("Shubham : ", Query) 
            except Exception as e: 
                print(e) 
                self.speak("Could you say that again!") 
                return
            return Query 
        
    def system_details(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()._asdict()['percent']
        self.speak("The CPU is at " + str(cpu_usage) + " and the memory is at " + str(memory_usage) + " % of its capacity.")
        print("Hazel : The CPU is at " + str(cpu_usage) + " and the memory is at " + str(memory_usage) + " % of its capacity.")
        if cpu_usage >= 90:
            self.speak("CPU capacity reached, free up some RAM.")
        if memory_usage >= 90:
            self.speak("Memory capacity reached, its about to blast.")
            
    def name(self):
        self.speak("My name is Hazel, your favorite companion.")
        print("My name is Hazel, your favorite companion.")
    
    def getTopNews(self):
        googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
        self.speak("Can you tell me the topic name?")
        print("Hazel : Can you tell me the topic name?")
        while True:
            topic = self.take_command()
            if topic != None:
                topic = topic.lower()
                print("Shubham : ", topic)
                break
        googlenews.search(topic)
        result = googlenews.result()
        print(result)
        for i in range(len(result)):
            print(i+1, ". ", result[i]['title'])
            
    async def remind(self, text, delay):
        await asyncio.sleep(delay)
        self.speak(test)
        print("Hazel : " + text)
        
    async def run_reminder(self, task):
        await task
            
    def reminder(self):
        self.speak("What is the agenda for the reminder?")
        print("Hazel : What is the agenda for the reminder?")
        while True:
            agenda = self.take_command()
            if agenda != None:
                print("Shubham : ", agenda)
                agenda = agenda.lower()
                break
        self.speak("Your reminder agenda is " + agenda + ". Can you please say Okay to confirm!")
        print("Hazel : Your reminder agenda is ", agenda, ". Can you please say Okay to confirm!")
        while True:
            confirm = self.take_command()
            if confirm != None:
                print("Shubham : ", confirm)
                confirm = confirm.lower()
                break
        if "okay" in confirm or "ok" in confirm:
            self.speak("And after how many minutes should I set the reminder?")
            print("Hazel : And after how many minutes should I set the reminder?")
            while True:
                minutes = self.take_command()
                if minutes != None:
                    print("Shubham : ", minutes)
                    minutes = int(minutes.split()[0])
                    seconds = minutes * 60
                    task = asyncio.create_task(self.remind(agenda, seconds))
                    self.run_reminder(task)
                    break        

if __name__ == "__main__":
    hazel = Hazel()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hazel.run_reminder())
    hazel.greeting()
    while True:
        while True:
            query = hazel.take_command()
            if query != None:
                query = query.lower()
                break
        if "system" in query:
            hazel.system_details()
        elif "your name" in query:
            hazel.name()
        elif "news" in query:
            hazel.getTopNews()
        elif "remind" in query or "reminder" in query:
            hazel.reminder()