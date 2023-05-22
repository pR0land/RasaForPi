import os
import requests
import serial
import RPi.GPIO as GPIO
import time
import speechRecon as sr
import pyttsx3
import directionOfArrival as DOA

from pixels import Pixels

serialRead = False
Talking = True




ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

engine = pyttsx3.init(driverName='espeak') #Selve engine
engine.setProperty("rate", 140) #Hvor hurtigt den taler
voices = engine.getProperty("voices")
for i,voice in enumerate(voices):
    if voice.name == "danish":
        engine.setProperty('voice',voices[i].id) #standard windows voice (danish)
pixels = Pixels()


def giveFeedback(type):
    if type == "None":
        pass
    elif type == "Buzz":
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        ser.write(b"Start Feedback\n")
        GPIO.cleanup()
    elif type == "Light":
        pixels.listen()


def stopFeedback(type):
    if type == "None":
        pass
    elif type == "Buzz":
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        ser.write(b"Stop Feedback\n")
        GPIO.cleanup()
    elif type == "Light":
        pixels.off()



while True:
    while serialRead:
        print("reading serial")
        read_ser=ser.readline()
        if read_ser is not None:
            cleaned = read_ser.decode().split('\r')
            print(f'this is cleaned ({cleaned})')
            state = cleaned[0].split(',')[0]
            print(state)
            if state == 'Start':
                time.sleep(10)
                alarm = cleaned[0].split(',')[1]
                print(alarm)
                response = cleaned[0].split(',')[2]
                print(response)
                feedback = cleaned[0].split(',')[3]
                print(feedback)
                if alarm == "Buzz":
                    ser.write(b"Start Prompting\n")
                elif alarm == "Light":
                    ser.write(b"Start Prompting\n")
                    pixels.wakeup()
                elif alarm == "Talk":
                    ser.write(b"Start Prompting\n")
                    bot_message = "Hej har du tid til at svare på et kort spørgeskema?"

                    engine.say(bot_message)  # Bot speak
                    engine.runAndWait()
                    engine.stop()


                if response == 'answer':
                    message = input("Skriv hvad du vil sige:")
                    print("stop prompt")
                    GPIO.setmode(GPIO.BOARD)
                    GPIO.setup(11, GPIO.OUT)
                    ser.write(b"Stop Prompting\n")

                    if alarm == "Light":
                        pixels.off()
                    GPIO.cleanup()
                    Talking = True
                    serialRead = False

            elif state == "Talk":
                giveFeedback(feedback)
                print("start talking")
                message = "Hej"
                if alarm == "Light":
                    pixels.off()
                Talking = True
                serialRead = False
    while Talking:

        print("Nu skriver vi til botten")

        r = requests.post('http://192.168.0.10:5002/webhooks/rest/webhook', json={"message": message})
        stopFeedback(feedback)
        for i in r.json():
            bot_message = i['text']
            # print(f"{self.bot_message}")
            # Logging.reply_logger.append(self.bot_message)
            print(bot_message)

            engine.say(bot_message)  # Bot speak
            engine.runAndWait()
            engine.stop()
        giveFeedback(feedback)
        print(message)
        message = input("Skriv hvad du vil sige:")