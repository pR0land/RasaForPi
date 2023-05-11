import os
import serial
import RPi.GPIO as GPIO
import time
serialRead = True
ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
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
                if alarm == "Buzz" or "Light":
                    ser.write(b"Start Prompting\n")

                if response == 'answer':
                    serialRead = False
