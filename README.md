# Controller

This controller is the basis for the functionality of the multi-use call bell system. The function of the system describes as follows:
* Provides on/off control and ON status for voice module (Switch, LED)
* Provides the ON status for the call bell (LED)
* Provides feedback for any signal trigger (LED)
* Receives, processes and sends call signal to the modalities

Hardware includes:
- Raspberry Pi 3B+
- 1/4 female mono audio jack (open circuit)
- Buttons
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

Voice Modality V2 (Stress Detection Approach)- Vosk + Deep Learning 
- 1. Receives speech from microphone
- 2. Processes trigger word is identified in Vosk
- 3. Vosk passes speech snippet to deep learning model.
- 4. Deep learning model triggers call bell if sound was identified as stressful
