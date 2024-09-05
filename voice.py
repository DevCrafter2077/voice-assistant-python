import pyttsx3 as p
import datetime
import wikipediaapi
import webbrowser
import os
import speech_recognition as sr
import subprocess
import pyjokes
import requests
import time
import cv2
import keyboard

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
myname = "monika"
cap = cv2.VideoCapture(0)

r = sr.Recognizer()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    current_time = datetime.datetime.now().time()
    morning_start = datetime.time(6, 0, 0)
    morning_end = datetime.time(11, 59, 59)
    noon_start = datetime.time(12, 0, 0)
    noon_end = datetime.time(14, 59, 59)
    afternoon_start = datetime.time(15, 0, 0)
    afternoon_end = datetime.time(17, 59, 59)
    night_start = datetime.time(18, 0, 0)
    night_end = datetime.time(23, 59, 59)

    if morning_start <= current_time < morning_end:
        speak("Good Morning!")
    elif noon_start <= current_time < noon_end:
        speak("Good Noon!")
    elif afternoon_start <= current_time < afternoon_end:
        speak("Good Afternoon!")
    elif night_start <= current_time <= night_end:
        speak("Good Evening!")
    else:
        speak("Good Night!")


if _name_ == "_main_":
    wish_me()
    speak("My name is Monika. I am your voice assistant.")
    speak("How can I help you?")

def takeCommand():  
    
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 25000
        r.adjust_for_ambient_noise(source, 1.2)
        audio = r.listen(source)
        
    print("Recognizing...")
    
    try:
        query = r.recognize_google(audio)
        print(f"User said: {query}")
    except Exception as e:
        speak("Sorry, I didn't get that. Say that again, please.")
        print("Say that again, please...")
        return "None"

    return query.lower()

def get_weather(city_name):
    api_key = "d6c37932ae5ccb4e09294755c14d1396"  
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city_name, 'appid': api_key}
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] != "404":
        if 'main' in data:
            main_data = data["main"]
            current_temperature_kelvin = main_data.get("temp")
            current_pressure = main_data.get("pressure")
            current_humidity = main_data.get("humidity")

            current_temperature_celsius = current_temperature_kelvin - 273.15

            weather_data = data["weather"]
            weather_description = weather_data[0].get("description")

            speak(f"Temperature: {current_temperature_celsius:.2f} degree Celsius, Pressure: {current_pressure} hPa, Humidity: {current_humidity}%, Description: {weather_description}")
            print(f"Temperature: {current_temperature_celsius:.2f} °C, Pressure: {current_pressure} hPa, Humidity: {current_humidity}%, Description: {weather_description}")
        else:
            speak("Weather information not available.")
    else:
        speak("City Not Found")


def close_browser():
    keyboard.press_and_release('Ctrl+w')

listening_enabled = True

while True:
    if listening_enabled:
        query = takeCommand().lower()
    else:
        query = ""

    if 'weather' in query:
        speak("Please tell me the city name.")
        print("City name:")
        city_name = takeCommand()
        get_weather(city_name)

    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")

        wiki_pedia = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='MyCustomAgent/1.0'
        )
        page = wiki_pedia.page(query)
        
        if page.exists():
            speak(f"Opening Wikipedia page for {query}.")
            webbrowser.open(page.fullurl)

            summary = page.summary[:500] 
            speak("According to Wikipedia")
            speak(summary)
            print(summary)
        else:
            speak("Sorry, I couldn't find any relevant information on Wikipedia.")

    elif 'open youtube' in query:
            speak("It's time for some entertainment! opening youtube...")
            speak("Press 'q' to quit from the youtube page")
            print("Press 'q' to quit from the youtube page")
            webbrowser.open("youtube.com")
            listening_enabled = False  
            keyboard.wait('q')
            close_browser()
            listening_enabled = True

    elif 'open google' in query:
            speak("Here you go with google")
            speak("Press 'q' to quit from the google page")
            print("Press 'q' to quit from the google page")
            webbrowser.open("google.com")
            listening_enabled = False
            keyboard.wait('q')
            close_browser()
            listening_enabled = True

    elif "open whatsapp" in query:
            speak("Opening whatsapp")
            speak("Press 'q' to quit from the whatsapp page")
            print("Press 'q' to quit from the whatsapp page")
            webbrowser.open("whatsapp.com")
            listening_enabled = False
            keyboard.wait('q')
            close_browser()
            listening_enabled = True

    elif "open camera" in query or "take a photo" in query:
            speak("Capture your memorable moment here..! Press q to stop the camera.")
            print("Press 'q' to stop the camera.")
            while True:
                ret, frame = cap.read()
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            
            
    elif "open stack overflow" in query:
            speak("Opening stack overflow")
            speak("Press 'q' to quit from the stack overflow page")
            print("Press 'q' to quit from the stack overflow page")
            webbrowser.open("www.stackoverflow.com")
            listening_enabled = False
            keyboard.wait('q')
            close_browser()
            listening_enabled = True
            
    elif "play music" in query or "play songs" in query or "open spotify" in query:
            speak("Here you go with spotify to listen songs.")
            speak("Press 'q' to quit from the spotify page")
            print("Press 'q' to quit from the spotify page")
            webbrowser.open("spotify.com")
            listening_enabled = False
            keyboard.wait('q')
            close_browser()
            listening_enabled = True
        
    elif 'tata' in query or "bye" in query:
            speak("bye bye... see you soon!")
            break
            
    elif 'exit' in query or 'stop' in query or 'leave' in query:
        speak("Thanks for using me.")       
        break

    elif "your name" in query:
            speak("My name is")
            speak(myname)
            print("My name is",myname)

    elif "your day" in query:
          speak("It's a great day. Thanks for asking me.")

    elif "how are you" in query:
          speak("I am fine.. thank you for asking.")

    elif "the" and "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

    elif "who are you" in query:
            speak("I am your virtual assistant ")

      elif "open gmail" in query or "send a mail" in query:
            speak("Here you go with gmail")
            speak("Press 'q' to quit from the gmail page")
            print("Press 'q' to quit from the gmail page")
            gmail = "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"
            os.startfile(gmail)
            listening_enabled = False
            keyboard.wait('q')
            close_browser()
            listening_enabled = True

    elif 'joke'in query or 'jokes' in query:
            speak(pyjokes.get_joke())

    elif query.startswith("where is"):
        location = query.replace("where is", "").strip()
        speak("User asked to Locate " + location) 
        speak("Press 'q' to quit from the location page")
        print("Press 'q' to quit from the location page")
        webbrowser.open("https://www.google.com/maps/place/" + location)
        listening_enabled = False
        keyboard.wait('q')
        close_browser()
        listening_enabled = True

    elif "restart the system" in query:
            speak("Your system is going to restart")
            subprocess.call(["shutdown", "/r"])

    elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

                  
    else:
                speak("Please try again!")
                print("Please try again")