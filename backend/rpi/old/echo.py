from TextToSpeech import tts
from recognition import SpeechRecognition
import json
import os

recog = SpeechRecognition(5, 48000)
recog.takeMicInput()
recog.convertAudioFile()
response = recog.recogniseVoice()
speak = tts()
speak.say(response)

