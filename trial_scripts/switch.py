import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(4, GPIO.IN)    # set GPIO4 as input (button)
GPIO.setup(17, GPIO.OUT)    # set GPIO17 as output (TRIGGER)
GPIO.setup(27, GPIO.OUT)    # set GPIO27 as input (Call Bel)
GPIO.setup(22, GPIO.OUT)    # set GPIO22 as input (Microphone)


try:  
    while True:
        print(GPIO.input(4))
        if(GPIO.input(4)):
            GPIO.output(22,1)
            GPIO.output(17,0)
        else:
            GPIO.output(17,1)
            GPIO.output(22,0)
            
        sleep(0.2)         # wait 0.1 seconds
        
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself 