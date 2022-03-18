#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

SetLogLevel(0)

# if not os.path.exists("model"):
#     print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
#     exit (1)

wf = wave.open(sys.argv[1], "rb")

# if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#     print ("Audio file must be WAV format mono PCM.")
#     exit (1)

TRIGGER_WORDS = ['help', 'nurse', 'pain', 'hello']

def checkTriggerWords(text):
    count = 0
    for word in TRIGGER_WORDS:
        count += text.count(word)
    return count

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

print("YES",wf.getframerate())

signal_time = range(100)
signal_sent = np.array([(x+1)%5 == 0 for x in range(100)]).astype(int) 
# plt.scatter(signal_time, signal_sent, label = 'Ideal Signal Detection Time')

files = ["a1.wav", "a2.wav", 'a5.wav', 'a6.wav',"a3.wav",'a4.wav']
files2 = ["a12.wav", "a22.wav", 'a52.wav', 'a62.wav',"a32.wav",'a42.wav']
files1 =["a11.wav", "a21.wav", 'a51.wav', 'a61.wav',"a31.wav",'a41.wav']

for infile in files2:
    ratio = []
    for x in range(1, 10,1):
        run_time = 0
        triggerWordHistory = []
        wf = wave.open(infile, "rb")
        timeout  = 0
        start_time = timer()
        vosk_time = []
        vosk_received = 0
        while True:
            data = wf.readframes(8000)
            run_time += 0.5
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data) or (run_time + 0.5 - timeout) > x:
                print("TRUE", run_time + 0.5 - timeout)
                timeout = run_time
                text =  json.loads(rec.Result())
                if text["text"] != "": print("Result: " + text["text"])
                vosk_received += checkTriggerWords(text["text"])
            else:
                final =  json.loads(rec.PartialResult())
                if final["partial"] != "": print("Partial: " + final["partial"])
        # plt.scatter(vosk_time, vosk_received, label = "Vosk Timeout (s): "+ str(x))
        ratio.append(vosk_received/80)
    plt.plot(range(1, 10,1), ratio)

for infile in files1:
    ratio = []
    for x in range(1, 10,1):
        run_time = 0
        triggerWordHistory = []
        wf = wave.open(infile, "rb")
        timeout  = 0
        start_time = timer()
        vosk_time = []
        vosk_received = 0
        while True:
            data = wf.readframes(8000)
            run_time += 0.5
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data) or (run_time + 0.5 - timeout) > x:
                print("TRUE", run_time + 0.5 - timeout)
                timeout = run_time
                text =  json.loads(rec.Result())
                if text["text"] != "": print("Result: " + text["text"])
                vosk_received += checkTriggerWords(text["text"])
            else:
                final =  json.loads(rec.PartialResult())
                if final["partial"] != "": print("Partial: " + final["partial"])
        # plt.scatter(vosk_time, vosk_received, label = "Vosk Timeout (s): "+ str(x))
        ratio.append(vosk_received/100)
    plt.plot(range(1, 10,1), ratio)
for infile in files:
    ratio = []
    for x in range(1, 10,1):
        run_time = 0
        triggerWordHistory = []
        wf = wave.open(infile, "rb")
        timeout  = 0
        start_time = timer()
        vosk_time = []
        vosk_received = 0
        while True:
            data = wf.readframes(8000)
            run_time += 0.5
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data) or (run_time + 0.5 - timeout) > x:
                print("TRUE", run_time + 0.5 - timeout)
                timeout = run_time
                text =  json.loads(rec.Result())
                if text["text"] != "": print("Result: " + text["text"])
                vosk_received += checkTriggerWords(text["text"])
            else:
                final =  json.loads(rec.PartialResult())
                if final["partial"] != "": print("Partial: " + final["partial"])
        # plt.scatter(vosk_time, vosk_received, label = "Vosk Timeout (s): "+ str(x))
        ratio.append(vosk_received/60)
    plt.plot(range(1, 10,1), ratio)
plt.legend()
# naming the x axis
plt.xlabel('Timeout Period')
# naming the y axis
plt.ylabel('Ratio of Trigger Words Detected')

# giving a title to my graph
plt.title('Ratio of Trigger Words Detected for Various Data over Timeout Period')

# function to show the plot
plt.show()

