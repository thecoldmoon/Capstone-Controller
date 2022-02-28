import os
import sys
from callbellModality import checkCallBell
from gpiozero import LED
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from pprint import pprint

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

callBellLight = LED(17)
voiceLight = LED(18)
triggerLight = LED(19)

def main(data_dir):
    while True:

        ## Voice Modality
        if switch is on and pluggedin:
            if voiceLight.value == 0: # Initiation
                voiceLight.on()
                ## Start voice ignitiation
            else:
                ## Check voice trigger
        else:
            voiceLight.off()
            # Terminate voice

        ## Call Bell Press Modality
        if pluggedin:
            callBellLight.on()
            ## Check voice rec results
        else:
            callBellLight.off()


if __name__ == '__main__':
    pprint(main(sys.argv[1]))