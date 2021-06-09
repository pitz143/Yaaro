import speech_recognition as sr
from gtts import gTTS
import playsound as playsound
import os
import weathercom
import json
import pyaudio


#from gTTS 
sr_name = "jarvis"
r = sr.Recognizer()
wake = "hey {}".format(sr_name)
waketune = "D:\\study\\python\\cortana_wake.mp3"

def voice_command_processor(ask=False):
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source,phrase_time_limit=4)
        text = ''
        try:
            text=r.recognize_google(audio)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print("service is down")

        return text.lower()



def audio_playback(text):
    filename = "test.mp3"
    tts = gTTS(text=text, lang='en', slow='false')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def execute_voice_command(text):
    if "what are you" in text:
        audio_playback("i am jarvis your voice assistance system")
        print("i am jarvis your voice assistance system")

    """if "how are you" in text:
    	audio_playback("i am fine")"""

    if "what is the today's weather" in text:
        city = voice_command_processor("which city")
        humidity, temp, phrase = weatherReport(city)
        audio_playback("currently in " + city + "  temperature is " + str(temp)
                       + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
        print("currently in " + city + "  temperature is " + str(temp)
              + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)

    if "how can you help me" in text:
    	print("with everything")
    	audio_playback("with everything")
    	

    if "how are you jarvis" in text:
    	print("i am never tried sir, always at your service.")
    	audio_playback("i am never tried sir, always at your service.")
    	

    if "my name is pratik" in text:
    	print("that nice of a name, how are you pratik!")
    	audio_playback("that nice of a name, how are you pratik!")

    #audio_playback(waketune
    #playsound("cortana_wake.mp3")
    #"hey {}".format(sr_name)

    if "hey jarvis" in text:
        #os.system("mpg123 " + waketune)
        playsound.playsound("D:\\study\\python\\cortana_wake.mp3")
        print("listening")
        audio_playback("listening")

    if "do you know me" in text:
    	ask_name = voice_command_processor("tell me your name")
    	print("nice to meet you " + ask_name)
    	audio_playback("nice to meet you " + ask_name)

    if "who are you" in text:
    	print("i m jarvis, your voice assistance program")
    	audio_playback("i m jarvis, your voice assistance program")




def weatherReport(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase


while True:
    command = voice_command_processor()
    print(command)
    execute_voice_command(command)


