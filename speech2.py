#from __future__ ﻿import print_function
import datetime
import pickle
import os.path
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
import os
import time
#import pyttsx3
from gtts import gTTS
import googletrans
import speech_recognition as sr
#import pytz
import subprocess
import playsound as playsound
import sys
import pyaudio
import json
import vlc
import weathercom
import PyPDF2
import pywhatkit
#import myspsolution as mysp
#from pdfminer.high_level import extract_text

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

gt = googletrans.Translator()

def speak(text):
    #engine = pyttsx3.init()
    #engine.say(text)
    #engine.runAndWait()
    filename = "test.mp3"
    #hindi_words = "hindi.mp3"
    #hindi = "hi"
    #english = "en-us"
    tts = gTTS(text=text, lang="en")
    #
    #tts2 = gTTS(text=text, lang=hindi)
    #
    tts.save(filename)
    #tts2.save(hindi_words)
    playsound.playsound(filename)
    #playsound.playsound(hindi_words)
    os.remove(filename)
    #os.remove(hindi_words)

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def get_audio(ask=False):
    #hindi="hi-In"
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        #r.adjust_for_ambient_noise(source)#listen(phrase_time_limit=4)
        audio = r.listen(source,phrase_time_limit=2)
        said = ""

        try:
            #said = r.recognize_google(audio, language="en-us")
            said = r.recognize_google(audio, language="en")

            #language = 'hi-In'
            #print(said)
        
        except Exception as e:
            print("Exception:" + str(e))

    return said.lower()
    #return said2.lower()



def groovemusic():
    #playsound.playsound("D:\\music\\moveon.mp3")
    p = vlc.MediaPlayer("D:\\music\\moveon.mp3")
    p.play()

def groovestop():
    p = vlc.MediaPlayer()
    p.stop()



"""def authenticate_google():
    #Shows basic usage of the Google Calendar API.
    #Prints the start and name of the next 10 events on the user's calendar.
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service"""


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    # THE NEW PART STARTS HERE
    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def computa():
    os.system("start explorer.exe")

#def sendmsg():
    #pywhatkit.sendwhatmsg('+256750499458', 'hello there, this msg has been sent from pratiks a.i. speech2', 14, 2)

def weather(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase

pratik = "उठो"
mrrobot = "jarvis"
waketone = "D:\\study\\python\\cortana_wake.mp3"
endtone = "D:\\study\\python\\end.mp3"
WAKE = "hello {}".format(mrrobot)
wake2 = "नमस्कार"
#SERVICE = authenticate_google()
print("Start")

while True:
    print("Listening")
    text = get_audio()
    print(text)
    #wake2

    #if text.count(WAKE) > 0:
    #    playsound.playsound(waketone)
    #    speak("hello sir, i m ready")
    #    #speak("साहब मैं तैयार हूं")
    #    print("hello sir, i m ready")
    #    #print("साहब मैं तैयार हूं")
    #    
    #    text = get_audio()
    #    playsound.playsound(endtone)

    #    """query = get_audio()
    #    text = gt.translate(query)
    #    query = text.text
    #    query = query.lower()
    #    print(query)"""

    CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                get_events(date, SERVICE)
            else:
                speak("I don't understand")

    NOTE_STRS = ["make a note", "write this down", "remember this"]
    for phrase in NOTE_STRS:
        if phrase in text:
            speak("What would you like me to write down?")
            note_text = get_audio()
            note(note_text)
            speak("I've made a note of that.")

    if "how are you" in text:
        print("i m fine")
        speak("i m fine")

    if "open computer" in text:
        print("opening files")
        speak("opening files")
        computa()

    if "goodbye" in text:
        print("see you later")
        speak("see you later")
        sys.exit()

    if "you are very good" in text:
        print("my master i m very please that you are happy")
        speak("my master i m very please that you are happy")

    if "my computer" in text:
        print("opening computer")
        speak("opening computer")
        os.system("start explorer.exe")

    if "play song" in text:
        print("opening player")
        speak("opening player")
        groovemusic()

    if "top" in text:
        print("stoping song")
        speak("stopping song")
        groovestop()

    if "what is the today's weather" in text:
        speak("which city")
        city = get_audio()
        humidity, temp, phrase = weather(city)
        print("currently in " + city + "  temperature is " + str(temp)
            + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
        speak("currently in " + city + "  temperature is " + str(temp)
                    + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)

    if "music" in text:
        os.system('C:\\Users\\Public\\Desktop\\vlc.lnk D:\\music\\moveon.mp3')

    if "call pikachu" in text:
        print("pikachu")
        speak("pikachu")
        playsound.playsound("D:\\audio\\pikachu_voice\\pikachu.mp3")

    if "translate" in text:
        print("tell me the word")
        speak("tell me the word")
        words = get_audio()
        said = gt.translate(words,dest="gu")
        words = said.text
        #words = said.lower()
        print(words)
        speak(words)

    if "आप कैसे हो" in text:
        speak("मै ठीक हू")
        print("मै ठीक हू")

    if "अनुवाद करना" in text:
        speak("मुझे शब्द बताओ")
        link = get_audio()
        result = gt.translate(link,dest='gu').text
        speak(result)
        print(result)

    if "read the book" in text:
        book = open('linux.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(book)
        pages = pdfReader.numPages
        print(pages)
        for num in range(26, pages):
            page = pdfReader.getPage(26)
            read = page.extractText()
            print(read)
            speak(read)

    if "send message" in text:
        print("sending message")
        speak("sending message")
        sendmsg()
        print("message delivered")
        speak("message delivered")