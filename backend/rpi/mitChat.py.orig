from TextToSpeech import tts
from recognition import SpeechRecognition
from Mitsuku import MitsukuBot
import json
import os

recog = SpeechRecognition(5, 48000)
recog.takeMicInput()
recog.convertAudioFile()
message = recog.recogniseVoice()
suku = MitsukuBot()
reply = suku.sendMessage(message)[0]
speak = tts()
speak.say(reply)

