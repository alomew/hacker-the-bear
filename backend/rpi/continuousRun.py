import pyaudio,os
import speech_recognition as sr



def run():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            mainfunction(source)

def mainfunction(source, r):
	try:
		audio = r.listen(source)
		user = r.recognize_google(audio)
		print(user)
	except sr.UnknownValueError:
		print("Undetected voice")
	except sr.RequestError as e:
		print("There was an error {}".format(e))
	

