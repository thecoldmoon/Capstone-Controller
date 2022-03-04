#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
from gpiozero import Button
from signal import pause
import sys
import os
import wave
import json

SetLogLevel(0)
button = Button(2)

def call_bell_initiated():
    print("CALL BELL Press")

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
lastText = ""

while True:
    data = wf.readframes(1000)
    
    button.when_pressed = call_bell_initiated
        
    if len(data) != 0:
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result())
            print(text["text"])
            if ("nurse" or "help" or "help me") in text["text"]:
                print("CALL BELL Voice")
        else:
            text = json.loads(rec.PartialResult())
            currentText = text['partial'].replace(lastText,'')
            print("Heard: " + currentText)
            if ("nurse" or "help" or "help me") in currentText:
                print("CALL BELL Voice")
            lastText = text['partial']
        

# text = json.loads(rec.FinalResult())
# if ("nurse" or "help" or "help me") in text["text"]:
#     print("CALL BELL Voice")

