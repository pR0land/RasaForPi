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
import librosa

WAVE_OUTPUT_FILENAME = "output.wav"
# Initialize PyAudio
audio = pyaudio.PyAudio()

# Set the sampling rate and the number of channels
RATE = 16000
CHANNELS = 2
CHUNK = 1024

recordedData = np.array(np.float32)

bot_message = ""
message = ""

my_mic = danspeech.audio.Microphone(device_index=1) #Siger hvad mic det er man skal bruge

model = TransferLearned()

#def addToAudio(data):
#    numpy.append(recordedData, data)
#def callback(in_data, frame_count, time_info, status):
    # Convert the audio input to a numpy array
    #data = np.frombuffer(in_data, dtype=np.int16)
    #dataAsFloat = data.astype(np.float32)
    #addToAudio(dataAsFloat)
    # Transcribe the audio using Danspeech
    #recognizer = Recognizer(model=model)
   # text = recognizer.recognize(dataAsFloat)
    # Print the transcription
    #print(f"Du sagde: {text}")

 #   return (in_data, pyaudio.paContinue)
def VArecord():

    # Open a stream to capture audio input from the ReSpeaker 4-Mic Array
    stream = audio.open(format=audio.get_format_from_width(2),
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=1,
                        frames_per_buffer=CHUNK)

    # Start the stream
    stream.start_stream()
    frames = []
    # Wait for the stream to finish
    #while stream.is_active():
     #   time.sleep(0.1)
    for i in range(0, int((RATE / CHUNK) * 7)):
        #pass
        data = stream.read(CHUNK)
        frames.append(data)
    # Stop the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    audio.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(audio.get_sample_size(audio.get_format_from_width(2)))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    lyd = load_audio(path=f"{WAVE_OUTPUT_FILENAME}")
    recognizer = Recognizer(model=model)
    message = recognizer.recognize(lyd)
    print(f"Du sagde: {message}")

    return message


