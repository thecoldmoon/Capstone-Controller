import os
import queue
import pyaudio
import sys
import vosk
import json
from timeit import default_timer as timer
import sounddevice as sd
from gpiozero import LED
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from pprint import pprint
from time import sleep     # this lets us have a time delay (see line 15)  

TRIGGER_WORDS = ['help', 'nurse', 'pain']

# SET UP
q = queue.Queue()
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  

callBellLight = 27
voiceLight = 22
triggerLight = 17
micSwitch = 4
callBell = 2

GPIO.setup(callBell, GPIO.IN)    # set GPIO2 as input (Button)
GPIO.setup(micSwitch, GPIO.IN)    # set GPIO4 as input (Switch)
GPIO.setup(triggerLight, GPIO.OUT)    # set GPIO17 as output (TRIGGER)
GPIO.setup(voiceLight, GPIO.OUT)    # set GPIO27 as input (Call Bel)
GPIO.setup(callBellLight, GPIO.OUT, initial=GPIO.HIGH)    # set GPIO22 as input (Microphone)

# HELPER FUNCTIONS
def checkMicrophone(nameString):
    p = pyaudio.PyAudio()
    for ii in range(p.get_device_count()):
        if nameString in p.get_device_info_by_index(ii).get('name'):
            return True
    return False

def flashTrigger(reason):
    print("CALL BELL triggered by:",reason)
    GPIO.output(triggerLight,1)
    sleep(1)
    GPIO.output(triggerLight,0)

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def initiateVoice():
    model = "model"
    if not os.path.exists(model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        sys.exit()
    device_info = sd.query_devices('USB PnP Audio Device: Audio (hw:1,0)', 'input')
    samplerate = int(device_info['default_samplerate'])
   
    model = vosk.Model(model)
    return model, samplerate

def checkTriggerWords(text):
    count = 0
    for word in TRIGGER_WORDS:
        count += text.count(word)
    return [timer() for i in range(count)]

# INIT
model, samplerate = initiateVoice() if checkMicrophone('USB PnP Audio Device') else print('Microphone not detected') and sys.exit()

# RUN
def main():
    triggerWordHistory = []
    repeats = []
    
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype='int16',
                            channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)

        while True:
            ## Voice Modality, Check switch is on and mic is plugged in
            if GPIO.input(micSwitch):
                
                # Make sure light is on
                GPIO.output(voiceLight,1)

                # Check for voice and trigger
                data = q.get()
                if rec.AcceptWaveform(data):
                    text = json.loads(rec.Result())
                    triggerWordHistory += checkTriggerWords(text["text"])
                    print("RESULT", rec.Result())
                    print("Trigger word history",triggerWordHistory)
                    print('repeats', repeats)
                    
                    # Check if Threshold is met, 
                    # Repetive, triggers if word is a single trigger word is heard consecutively
                    if len(text["text"].split()) > 0:
                        for word in text["text"].split():
                            if word in TRIGGER_WORDS:
                                if len(repeats) == 0 or repeats[-1] == word:
                                    repeats.append(word)
                                else:
                                    repeats = []
                            if len(repeats) >= 3: 
                                flashTrigger("Voice Repeat")
                                repeats = []
                    # Temporal, triggers if 4 trigger words are heard consecutively within 4 seconds
                    if len(triggerWordHistory) >= 3:
                        if (triggerWordHistory[-1] - triggerWordHistory[0]) >= 4:
                            flashTrigger("Voice Temporal")
                        triggerWordHistory= []
                
            else:
                GPIO.output(voiceLight,0)
                print("Mic Switch is Off, not listening")

            ## Call Bell Press Modality
            if GPIO.input(callBell) == GPIO.LOW:
                flashTrigger("Call Bell")


if __name__ == '__main__':
    pprint(main())