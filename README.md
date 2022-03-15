# Running Main Program
 - 1. Connect to Raspberry Pi vis Ethernet cable
 - 2. SSH in using ``ssh pi@raspberrypi.local`` in terminal
 - 3. Run ``python3 main.py``

# File Structure
 - `` main.py `` - Script for prototype controller
 - `` test_ffmpeg.py `` - Script for testing audio files
 - `` test_microphone.py`` - Script for testing microphone
 
 Folders:
 - `` Audiofiles `` - Test audio files
 - `` model``  - Vosk model DONT REMOVE
 - `` trial-scripts``  - Some drafts
 - `` other-python-examples``  - Other examples provided by Vosk

# Controller

This controller is the basis for the functionality of the multi-use call bell system. The function of the system describes as follows:
* Provides on/off control and ON status for voice module (Switch, LED)
* Provides the ON status for the call bell (LED)
* Provides feedback for any signal trigger (LED)
* Receives, processes and sends call signal to the modalities

Hardware includes:
- Raspberry Pi 3B+
- 1/4 female mono audio jack (open circuit)
- Switch
- lights
- Microphone
- Wires + Breadboard

# Modalities

Call bell
- Receives direct signal from GPIO pin connected to female 1/4 jack

Voice Modality V1 (Temporal Approach)- Vosk
- 1. Receives speech from microphone
- 2. Processes speech in Vosk
- 3. If temporal threshold is met (e.g. "help" is said 3 times in 2 seconds, trigger call bell)

~~Voice Modality V2 (Stress Detection Approach)- Vosk + Deep Learning 
- 1. Receives speech from microphone
- 2. Processes trigger word is identified in Vosk
- 3. Vosk passes speech snippet to deep learning model.
- 4. Deep learning model triggers call bell if sound was identified as stressful

# Vosk Speech Recognition Toolkit

`` python3 test-simply.py nurse_help.wav ``

Vosk models are small (50 Mb) but provide continuous large vocabulary
transcription, zero-latency response with streaming API, reconfigurable
vocabulary and speaker identification.

Speech recognition bindings implemented for various programming languages
like Python, Java, Node.JS, C#, C++ and others.

Vosk supplies speech recognition for chatbots, smart home appliances,
virtual assistants. It can also create subtitles for movies,
transcription for lectures and interviews.

Vosk scales from small devices like Raspberry Pi or Android smartphone to
big clusters.

# Documentation

For installation instructions, examples and documentation visit [Vosk
Website](https://alphacephei.com/vosk).
