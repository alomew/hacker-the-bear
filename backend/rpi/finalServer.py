import pyaudio,os
import speech_recognition as sr
from datetime import datetime
import time
import requests
import json
import threading
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
	r = sr.Recognizer()
	with sr.Microphone() as source:

		while True:
			mainfunction(source, r)

def mainfunction(source, r):
	try:
		r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
		audio = r.listen(source)
		text = r.recognize_google(audio)
		sendServerMessage(text)
		print(text)
	except sr.UnknownValueError:
		print("Undetected voice")
	except sr.RequestError as e:
		print("There was an error {}".format(e))


def sendServerMessage(text):
	now = str(datetime.now())
	print(now)
	dataVal = {"user_id":"1",
	"timestamp": now,
	"person_text": str(text)}
	headers = {"Content-type":"application/json"}
	r = requests.post(server+serverSlug, json = dataVal, headers=headers) # requests.post to make a post call to dummy server.
	data = json.loads(r.content.decode('utf-8'))
	sendPiMessage(data)


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





	


