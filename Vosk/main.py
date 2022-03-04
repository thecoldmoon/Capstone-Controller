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

def flashTrigger():
    print("CALL BELL")
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
    device_info = sd.query_devices('default', 'input')
    samplerate = int(device_info['default_samplerate'])
   
    model = vosk.Model(model)

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device='default', dtype='int16',
                            channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
    return rec

def checkTriggerWords(text):
    count = 0
    for word in TRIGGER_WORDS:
        count += text.count(word)
    return [timer() for i in range(count)]

# INIT
rec = initiateVoice() if checkMicrophone('USB Condenser Microphone') else print('Microphone not detected') and sys.exit()

# RUN
def main(data_dir):
    triggerWordHistory = []
    repeats = []

    while True:
        ## Voice Modality, Check switch is on and mic is plugged in
        if GPIO.input(micSwitch):
            
            # Make sure light is on
            GPIO.output(voiceLight,1)

            # Check for voice and trigger
            data = q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())
                triggerWordHistory.append(checkTriggerWords(text["text"]))
                print("RESULT", rec.Result())
            
            else:
                print("PARTIAL", rec.PartialResult())
            
            # Check if Threshold is met, 
            # Repetive, triggers if word is a single trigger word is heard consecutively
            for word in text["text"].split():
                if word in TRIGGER_WORDS:
                    if len(repeats) is 0 or repeats[-1] is word: repeats.append(word) 
                if repeats >= 3: 
                    flashTrigger()
                    repeats = []
            # Temporal, triggers if 4 trigger words are heard consecutively within 4 seconds
            if len(triggerWordHistory) >= 3 and triggerWordHistory[-1] - triggerWordHistory[0] >= 4:
                flashTrigger()
                triggerWordHistory= []
        else:
            GPIO.output(voiceLight,0)
            print("Mic Switch is Off, not listening")

        ## Call Bell Press Modality
        if GPIO.input(callBell):
            flashTrigger()


if __name__ == '__main__':
    pprint(main(sys.argv[1]))