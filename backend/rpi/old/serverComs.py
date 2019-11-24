import pyaudio,os
import speech_recognition as sr
from datetime import datetime
import time
import requests
import json
import threading


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
#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time

import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
	# received audio data, now we'll recognize it using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		text = recognizer.recognize_google(audio)
		sendServerMessage(text)
		print("Google Speech Recognition thinks you said " + text)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))


def run():
	while True:
		r = sr.Recognizer()
		m = sr.Microphone()
		with m as source:
		    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

		# start listening in the background (note that we don't have to do this inside a `with` statement)
		stop_listening = r.listen_in_background(m, callback)
		# `stop_listening` is now a function that, when called, stops background listening

		# do some unrelated computations for 5 seconds
		for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

		# calling this function requests that the background listener stop listening
		stop_listening(wait_for_stop=False)




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
	"""r = requests.get(url = pi+piHealth)
	data1 = r.content.decode('utf-8')
	if data1:
		print("ok")"""
	headers = {"Content-type":"application/json"}
	r = requests.post(pi+piSlug, json = jdata, headers=headers) # requests.post to make a post call to dummy server.
	my_json = r.content.decode('utf-8')




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





	


