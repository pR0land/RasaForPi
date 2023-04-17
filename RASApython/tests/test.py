import requests
import speech_recognition as sr
from gtts import gTTS
#from playsound import playsound
#import os
import pyttsx3

bot_message = ""
message = ""

my_mic = sr.Microphone(device_index=1) #Siger hvad mic det er man skal bruge


engine = pyttsx3.init(driverName='sapi5') #Selve engine
engine.setProperty("rate", 190) #Hvor hurtigt den taler
voices = engine.getProperty("voices")
engine.setProperty('voice',"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0") #standard windows voice

def VArecord():
    r = sr.Recognizer()  # initialize recognizer
    with my_mic as source:  # mention source it will be either Microphone or audio files.
        print("Sig noget:")
        r.adjust_for_ambient_noise(my_mic, duration=0.2)
        audio = r.listen(source)  # listen to the source

        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.key=self.WIT_AI_KEY
            # Logging.reply_logger.append(self.message)  # storing message string
            # print("You said : {}".format(self.message))
            return message #Hent den message der lige er blevet speaket

        except sr.UnknownValueError:
            print("Kan du gentage, jeg hørte det ikke")
            r = sr.Recognizer()


message = VArecord()

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

for i in r.json():
        bot_message = i['text']
        #print(f"{self.bot_message}")
        #Logging.reply_logger.append(self.bot_message)
        print(bot_message)

        engine.say(bot_message) #Bot speak
        engine.runAndWait()
        engine.stop()