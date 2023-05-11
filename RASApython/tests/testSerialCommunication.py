import os
import requests
import serial
import RPi.GPIO as GPIO
import time
import rasaCommunication as rc
import pyttsx3

serialRead = True
Talking = False

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

engine = pyttsx3.init(driverName='sapi5') #Selve engine
engine.setProperty("rate", 190) #Hvor hurtigt den taler
voices = engine.getProperty("voices")
engine.setProperty('voice',voices[1].id) #standard windows voice (danish)

while True:
    while serialRead:
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
                if alarm == "Buzz":
                    ser.write(b"Start Prompting\n")

                if response == 'answer':
                    serialRead = False
            elif state == "Talk":
                Talking = True
                serialRead = False
    while Talking:
        message = rc.VArecord()

        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

        for i in r.json():
            bot_message = i['text']
            # print(f"{self.bot_message}")
            # Logging.reply_logger.append(self.bot_message)
            print(bot_message)

            engine.say(bot_message)  # Bot speak
            engine.runAndWait()
            engine.stop()
