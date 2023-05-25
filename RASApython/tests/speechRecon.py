## Run this command in terminal  before executing this program
##rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions
import time

import danspeech.audio
import numpy
import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
#import os
import pyttsx3
from danspeech import Recognizer
from danspeech.pretrained_models import TransferLearned
from danspeech.language_models import DSL3gram
from danspeech.audio import load_audio
import numpy as np
import pyaudio
import wave
import queue
import threading


class SpeechRecon(object):

    def __init__(self, rate=16000, channels=4, chunk=1024):
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.queue = queue.Queue()

        # Set the sampling rate and the number of channels
        self.RATE = rate
        self.CHANNELS = channels
        self.CHUNK = chunk

        self.quitEvent = threading.Event()

        # Open a stream to capture audio input from the ReSpeaker 4-Mic Array
        self.stream = self.audio.open(format=pyaudio.paInt16,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            input_device_index=1,
                            frames_per_buffer=self.CHUNK,
                            stream_callback=self.callback)
    recordedData = np.array(np.float32)

    bot_message = ""
    message = ""

    my_mic = danspeech.audio.Microphone(device_index=1) #Siger hvad mic det er man skal bruge

    model = TransferLearned()


    #def addToAudio(data):
    #    numpy.append(recordedData, data)
    def callback(self,in_data, frame_count, time_info, status):
        # quing the inputdata
        self.queue.put(in_data)
        # Convert the audio input to a numpy array
        #data = np.frombuffer(in_data, dtype=np.int16)
        #dataAsFloat = data.astype(np.float32)
        #addToAudio(dataAsFloat)
        # Transcribe the audio using Danspeech
        #recognizer = Recognizer(model=model)
       # text = recognizer.recognize(dataAsFloat)
        # Print the transcription
        #print(f"Du sagde: {text}")

        return None, pyaudio.paContinue

    def readChunk(self):
        self.quitEvent.clear()
        while not self.quitEvent.is_set():
            frames = self.queue.get()
            if not frames:
                break
            frames = np.fromstring(frames, dtype='int16')
            yield frames

    def start(self):
        #clear the queue
        self.queue.queue.clear()
        # Start the stream
        self.stream.start_stream()

    def stop(self):
        self.quitEvent.set()
        self.stream.stop_stream()
        self.queue.put('')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            return False
        self.stop()

#This is the part which had a chance to understand danish, but was slow. Its no longer working,
# since i rewrote the file after this was commented out
        # frames = []
        # # Wait for the stream to finish
        # #while stream.is_active():
        #  #   time.sleep(0.1)
        # for i in range(0, int((RATE / CHUNK) * 10)):
        #     #pass
        #     data = stream.read(CHUNK)
        #     frames.append(data)
        # # Stop the stream
        # stream.stop_stream()
        # stream.close()
        #
        # # Terminate PyAudio
        # audio.terminate()
        #
        #
        # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        # wf.setnchannels(2)
        # wf.setsampwidth(audio.get_sample_size(audio.get_format_from_width(2)))
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()
        #
        # lyd = load_audio(path=f"{WAVE_OUTPUT_FILENAME}")
        # recognizer = Recognizer(model=model)
        # message = recognizer.recognize(lyd)
        # print(f"Du sagde: {message}")
        #
        # return message


