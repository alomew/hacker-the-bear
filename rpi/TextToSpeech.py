from gtts import gTTS
import os
from datetime import date

class tts():
	def __init__(self):
		pass
	
	def say(self, message):
		tts = gTTS(text=message, lang='en')
		now = date.today()
		tts.save("{}.mp3".format(now))
		os.system("mpg321 {}.mp3".format(now))
