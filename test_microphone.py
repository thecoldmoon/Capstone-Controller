#!/usr/bin/env python3
# Tutorial : https://www.youtube.com/watch?v=Itic1lFc4Gg&ab_channel=yingshaoxo%27slab
# Change Input Accordingly

import argparse
import os
import json
import queue
import sounddevice as sd
import vosk
import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

start_time = timer()

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = int(device_info['default_samplerate'])
   
    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    blocksizes = [800, 2000, 3800, 5200, 8200, 11800]
    average = []
    zero_ratios = []
    for size in blocksizes:
        stream =  sd.RawInputStream(samplerate=args.samplerate, blocksize = size, device=args.device, dtype='int16',
                                channels=1, callback=callback)
        stream.start() 
        print('#' * 80)
        print('Press Ctrl+C to stop the recording')
        print('#' * 80)
        
        rec = vosk.KaldiRecognizer(model, args.samplerate)
        start_time = timer()
        time_elapsed = np.array([])
        queue_size = np.array([])
        avg_size = np.array([])
        timeout = timer()

        while True:
            time_elapsed=np.append(time_elapsed, timer()-start_time)
            queue_size=np.append(queue_size, q.qsize())
            data = q.get()
            
            if rec.AcceptWaveform(data) or timer()-timeout >3:
                final =  json.loads(rec.Result())
                timeout = timer()
                if final["text"] != "": print("Result: " + final["text"])
            
            if dump_fn is not None:
                dump_fn.write(data)
            if (timer() - start_time) > 60:
                plt.plot(time_elapsed, queue_size, label = str(size))
                average.append(np.mean(queue_size[queue_size != 0]))
                zero_ratios.append(np.count_nonzero(queue_size==0)/len(time_elapsed))
                stream.close()
                break
    plt.legend()
    # naming the x axis
    plt.xlabel('Time Elapsed')
    # naming the y axis
    plt.ylabel('Queue Size')
    
    # giving a title to my graph
    plt.title('Macbook - Vosk Lightweight Model')
    
    # function to show the plot
    plt.show()
    plt.scatter(blocksizes, average, label = "Raspberry Pi")
    # naming the x axis
    plt.xlabel('Block Size')
    # naming the y axis
    plt.ylabel('Average Queue Size for Queue > 0')
    
    # giving a title to my graph
    plt.title('Block Size vs Average Queue Size')
    
    # function to show the plot
    plt.show()

    plt.scatter(blocksizes, zero_ratios)
    # naming the x axis
    plt.xlabel('Block Size')
    # naming the y axis
    plt.ylabel('% Non-Empty Queue')
    
    # giving a title to my graph
    plt.title('Block Size vs % of Non-Empty Queue')
    
    # function to show the plot
    plt.show()
    parser.exit(0)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
