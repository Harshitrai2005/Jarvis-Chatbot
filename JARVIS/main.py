
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import time
import os
import pyautogui
import sys
import pyaudio
import psutil
from elevenlabs import  generate,play
from elevenlabs import set_api_key
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
from api_key import api_key_data
set_api_key(api_key_data)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def engine_talk(query):
    audio=generate(
        text=query,
        voice="Grace",
        model="eleven_modellingual_v1"
    )    
    play(audio)


def initialize_engine():
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty("voices")
    engine.setProperty('voice',voices[1].id)
    rate=engine.getProperty('rate')
    engine.setProperty('rate',rate-50)
    volume=engine.getProperty('volume')
    engine.setProperty('volume',volume+0.25)
    return engine

def speak(text):
    engine=initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r=sr.Recognizer()
    with sr.Microphone()as source:
         r.adjust_for_ambient_noise(source,duration=0.5)
         print("Listening--------")
         r.pause_threshold=1.0
         r.phrase_threshold=0.3
         r.sample_rate=48000
         r.dynamic_energy_threshold=True
         r.operation_timeout=5
         r.non_speaking_duration=0.5
         r.dynamic_energy_adjustment=2
         r.energy_threshold=4000
         r.phrase_time_limit=10
         print(sr.Microphone.list_microphone_names())
         audio=r.listen(source)
    try:
         print("\r",ends="",flush=True)
         print('Recognizing-------')
         query=r.recognize_google(audio,language=['en-in'])
         print("\r",end="",flush=True)
         print(f"User said:  {query}\n")

    except Exception as e:
         print('Say that again plsease')
         return 'None'
    return query    


def cal_day():
    day=datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thurdsay",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
      
    }
    if day in day_dict.keys():
       day_of_week=day_dict[day]
       print(day_of_week)
    return day_of_week



def WishMe():
    hour=int(datetime.datetime.now().hour)
    t=time.strftime("%I:%M:%p")
    day=cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
       speak((f"Good Morning Harshit, it's {day} an the time is {t} "))
    elif(hour>=12) and(hour<=16) and ('PM' in t):
        speak(f"Good afternoon Harshit ,it's{day} and the time is {t} ")
    else:
        speak(f"Good evening Harshit,it's {day} and the time is {t} ")


def social_media_query(command):
    if 'GeeksForGeeks' in command:
        speak("opening facebook account ")
        webbrowser.open("https://www.geeksforgeeks.org/problem-of-the-day?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=practice_header")
    elif 'leetcode' in command:
        speak("opening leetcode account")
        webbrowser.open("https://leetcode.com/u/harshitrai/")
    elif 'whatsapp' in command:
        speak("opening whatsapp")
        webbrowser.open("")
    else:
        speak("No result found")    

def schedule():
    day=cal_day().lower()
    speak("Sir today's schedule is ")
    week={
        "monday":""
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile("C:\\Windows\\System32\\calc.exe")
    elif "notepad" in command:
        speak("opeaning notepad")
        os.startfile("C:\\windows\\System32\\notepad.exe")
    elif "paint" in command:
        speak("opening paint")
        os.startfile("C:\\Windows\\System32\\paint.exe")

def closeApp():
      if "calculator" in command:
          speak("closing calculator")
          os.startfile("taskkill /f /im calc.exe")
      elif "notepad" in command:
          speak("closing notepad ")
          os.startfile("taskkill /f /im notepad.exe")
      elif "paint" in command:
          speak("closing paint")
          os.startfile("taskkill /f /im paint.exe")   

def browsing(query):
    if "google" in query:
        speak("Sir, what do you wnat to search on google")
        s=command().lower()
        print(s)
        webbrowser.open(f"{s}")

def condition():
    usage=str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery=psutil.sensors_battery()
    percentage=battery.percent
    speak(f"Sir our system is having {percentage} percent battery now")

    if percentage>=75:
        speak("Sir we have enough battery percentage No need to connect now")
    elif percentage>=40 and percentage<75:
        speak("Sir we should connect our pc for charging")
    else:
        speak("sir we have low battery ,pls charge immediately")


if __name__=="__main__":
     engine_talk("allow me to introduce to you ,I am jarvis a virtual chatbot assistant for helping you 24 hours a day 7 days a week")

     while True:
         query=input("Enter your command")

         if ('GeeksForGeeks' in query) or('leetcode' in query) or('whatsapp' in query):
             social_media_query(query)
        
         elif ('college tt ' in query) or('college time table' in query) or ('time table' in query): 
             schedule()   

         elif ("volume up" in query):
             pyautogui.press("volumeup")
             speak("volume up")

         elif ("volume down" in query):
             pyautogui.press("volumedown")
             speak("volume down")

         elif ("volume mute" in query) or("mute the volume" in query):
             pyautogui("volume mute")
             speak('volume mute')

         elif("open calculator" in query ) or ("open paint" in query) or("open notepad" in query):
             openApp(query)


         elif("close calculator" in query ) or ("close paint" in query) or("close notepad" in query):
             closeApp(query)


         elif ("who" in query) or("what" in query) or("how" in query) or("where " in query) or("hi" in query) or("hello"in query):
             padded_sequences=pad_sequences(tokenizer.texts_to_sequences([query]),truncating="post",maxlen=20)
             result=model.predict(padded_sequences)
             tag=label_encoder.inverse_transform([np.argmax(result)])


             for i in data['intents']:
                 if i['tag']==tag:
                     speak(np.random.choice(i["responses"]))

         elif ("open google " in query) or ("google" in query):
              browsing(query)
              
         elif ("system condition" in query) or ("condition of system" in query) or ("condition" in query):
              speak("checking the system conditions")
              condition()


         elif "exit" in query:
             sys.exit()
 
             


             


     





