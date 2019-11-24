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
	recognizer = sr.Recognizer()
	microphone = sr.Microphone()
	while True:
		recognize_speech_from_mic(recognizer, microphone)

	

def recognize_speech_from_mic(recognizer, microphone):
	"""Transcribe speech from recorded from `microphone`.

	Returns a dictionary with three keys:
	"success": a boolean indicating whether or not the API request was
	       successful
	"error":   `None` if no error occured, otherwise a string containing
	       an error message if the API could not be reached or
	       speech was unrecognizable
	"transcription": `None` if speech could not be transcribed,
	       otherwise a string containing the transcribed text
	"""
	# check that recognizer and microphone arguments are appropriate type
	if not isinstance(recognizer, sr.Recognizer):
		raise TypeError("`recognizer` must be `Recognizer` instance")

	if not isinstance(microphone, sr.Microphone):
		raise TypeError("`microphone` must be `Microphone` instance")

	# adjust the recognizer sensitivity to ambient noise and record audio
	# from the microphone
	with microphone as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)

	# set up the response object
	response = {
		"success": True,
		"error": None,
		"transcription": None
	}

	# try recognizing the speech in the recording
	# if a RequestError or UnknownValueError exception is caught,
	#     update the response object accordingly
	try:
		response["transcription"] = recognizer.recognize_google(audio)
		sendServerMessage(response["transcription"])
	except sr.RequestError:
		# API was unreachable or unresponsive
		response["success"] = False
		response["error"] = "API unavailable"
		print("api")
	except sr.UnknownValueError:
		print("unknown")
		# speech was unintelligible
		response["error"] = "Unable to recognize speech"

	return response


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





	


