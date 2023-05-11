## Run this command in terminal  before executing this program
##rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
#import os
import pyttsx3

bot_message = ""
message = ""

my_mic = sr.Microphone(device_index=1) #Siger hvad mic det er man skal bruge



for i in voices:
    print(i.name)

def VArecord():
    r = sr.Recognizer()  # initialize recognizer
    with my_mic as source:  # mention source it will be either Microphone or audio files.
        print("Sig noget:")
        #r.energy_threshold = 4000 #threshold for sound picked up - incase of problems
        r.adjust_for_ambient_noise(my_mic, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)  # listen to the source
        except audio:
            print("Unable to listen here, try again")

        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.key=self.WIT_AI_KEY
            #Logging.reply_logger.append(self.message)  # storing message string
            print("Du sagde : {}".format(message))
            return message #Hent den message der lige er blevet speaket

        except sr.UnknownValueError:
            print("Kan du gentage, jeg hørte det ikke")
            r = sr.Recognizer()



