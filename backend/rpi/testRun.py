import pyaudio,os
import speech_recognition as sr
from datetime import datetime
import time
import requests
import json
import threading
from speech import SpeechRecognition
from BotChoice import randBot
from TextToSpeech import tts


server = "https://hacker-the-bear.appspot.com/"
serverSlug = "textofperson"
serverHealth = "ping"

pi = "http://192.168.43.87:5000/"
piSlug = "getText"
piHealth = "ping"

""" JSON Format:
toServer
{ user-id, timestamp, person-text}
fromServer/toRPI
{ user-id, timestamp, person-text, bear-text}
"""


def run():
	suki = randBot()
	sr = SpeechRecognition(5, 48000)
	while True:
		sr.takeMicInput()
		sr.convertAudioFile()
		sendServerMessage(sr.recogniseVoice(),suki)


def sendServerMessage(text,suki):
	tts().say(suki.sendMessage(text))
	


def sendPiMessage(jdata):
	speech = tts()
	speech.say(jdata["bear_text"])	




"""while True:
	r = requests.get(url = server+serverHealth)
	data = r.json() 
	if data:
		r = requests.get(url = pi+piHealth)
		data1 = r.json()
		if data1:
			break
	time.sleep(0.5)"""
run()
"""x = threading.Thread(target=run)
x.start()"""
# Main program





	


