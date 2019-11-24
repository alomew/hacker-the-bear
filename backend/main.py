import datetime

from flask import Flask, render_template, jsonify, request
from google.cloud import datastore
from rpi.Mitsuku import MitsukuBot
import random
from enum import Enum

class DanceMove:
	

	NOTHING = 0
	DANCE = 1
	WAVE = 2
	CUDDLE = 3

	DANCE_MOVE = NOTHING
	def setDance(self, move):
		self.DANCE_MOVE = move

app = Flask(__name__)


bot = MitsukuBot()

danceMove = DanceMove()

datastore_client = datastore.Client()

def store_speech(speech_json):
	entity = datastore.Entity(key=datastore_client.key('speech'))
	dt = datetime.datetime.now()
	speech_json['timestamp'] = dt
	entity.update(speech_json)

	datastore_client.put(entity)

def fetch_speeches(limit):
	query = datastore_client.query(kind="speech")
	query.order = ['-timestamp']

	speeches = query.fetch(limit=limit)

	return speeches

# @app.route('/')
# def root():
#     # Store the current access time in Datastore.
#     store_time(datetime.datetime.now())
#
#     # Fetch the most recent 10 access times from Datastore.
#     times = fetch_times(10)
#
#     return jsonify(list(times))


@app.route('/')
def root():
	return render_template("index.html")

@app.route('/readspeeches')
def fetchspeeches():
	return jsonify(list(fetch_speeches(10)))

@app.route('/addspeech', methods=['POST'])
def addspeech():
	json = request.get_json()
	if json:
		store_speech(json)
		return jsonify(True)
	else:
		return jsonify(False)

@app.route('/textofperson', methods=['POST'])
def textofperson():
	json = request.get_json()
	print(json)
	#json = {'user_id': "1", 'person_text': 'Hi there', 'timestamp': datetime.datetime.now().isoformat()}
	badWords = {"sad","lonely","unhappy","kill","die", "leave", "depressed","death","hungry","tired","stiff","aching", "miss"}
	sosWords = {"fallen", "hurt", "injured", "broken", "pain", "ouch", "help", "stroke", "heart", "attack"}
	happyWords = {"happy", "excited", "nice", "sunny"}
	needWords = {"hungry", "thirsty", "tired", "exhausted", "sleepy"}
	songWords = {"play", "song"}
	familyWords = {"family", "sister", "daughter", "grandson", "grandaughter"} # include actual names
	memoryWords = {"remember", "remembered"}
	forgetWords = {"forget", "forgotten"}

	rand = random.randint(1,100)
	# If 5 or less, tell them to drink water
	if json:
		try:
			person_text = json["person_text"]
			status = 0
			bot = False
			for word in person_text:
				w = word.lower()
				if w in sosWords:
					status = 1
					break
				elif w in badWords:
					status = 2
					break
				elif w in needWords:
					status = 3
					break
				elif w in forgetWords:
					status = 4
					break
				elif w in memoryWords:
					status = 5
					break
				elif w in familyWords:
					status = 6
					break
				elif w in happyWords:
					status = 7
					break
				elif w in songWords:
					status = 8
					break
				elif w in {"bot", "human", "husky", "dog", "pet", "baby", "alien", "robot", "machine", "ai"}:
					bot = True
				
			if status ==1:
				sosResponse = {"Wait there, I am sending help!", "Lie in the recovery position", "Please call the police"}
				bear_text= random.sample(sosResponse,1)[0]

			elif status == 2:
				badResponse = {"You could try some exercise", "I'm sorry about that, I hope you have a better day tommorrow", "May I reccomend nightline?"}
				bear_text = random.sample(badResponse,1)[0]

			elif status == 3:
				needsResponse = {"Try and better your health", "Take some supplemants", "Drink water"}
				bear_text = random.sample(needsResponse,1)[0]

			elif status == 4:
				badResponse = {"Wait there, I am sending help!", "Lie in the recovery position", "Please call the police"}
				bear_text = random.sample(badResponse,1)[0]

			elif status == 5:
				memoryRes = {"I'm so glad you remember that","That sounds good, would you like to talk more about it?","Do you remember anything else about the situation"}
				bear_text = random.sample(memoryRes,1)[0]

			elif status == 6:
				familyRes = {"That's interesting, tell me more!", "That's great, it's great that you remember", "Oh really?"}
				bear_text = random.sample(familyRes,1)[0]

			elif status == 7:
				happyRes = {"That's awesome! I'm glad", "Yippeee!", "Yay!"}
				bear_text = random.sample(happyRes,1)[0]
				
			elif status == 8:
				songRes = "" # Songs will play
				bear_text = "Dance time!"

			else:
				done = False
				howAreYou = {"how are you", "how are you doing", "how are you feeling", "you okay"}
				whatAreYouDoing = {"what are you doing", "what are you up to", "what you doing", "up to much"}
				if bot:
					bots = {"I'm simply a husky, Hacker the husky!", "Look at me, I'm a dog!", "Last time I checked, I was indeed a dog!"}
					bear_text = random.sample(bots,1)[0]
					done = True
				for val in howAreYou:
					if val in bear_text:
						okThanks = {"I'm good thank you! How are you?", "I'm pretty great, what about you?", "I'm alright actually. Are you okay?", "Doing well, you?"}
						bear_text = random.sample(okThanks,1)[0]
						done = True
						break
				for val in whatAreYouDoing:
					if val in bear_text:
						stuff = {"Talking to you, of course!", "Just enjoying my time, talking to you, what about you?", "Just chilling, you?"}
						bear_text = random.sample(stuff,1)[0]
						done = True
						break
				if not done:	
					bear_text = bot.sendMessage(person_text)[1:-1]
		except:
			byeRes = {"I need some sleep", "I'm tired", "I ought to go, have a wonderful day!", "Goodnight", "Good day"}
			bear_text = random.sample(byeRes,1)[0]

		if rand < 5:
			drinkRes = {"Hey, make sure you've been drinking enough.", "Have you been drinking? It's been a while", "Make sure you have a glass of water!"}
			bear_text += ". " + random.sample(drinkRes,1)[0]

		json['bear_text'] = bear_text
		return jsonify(json)

	return jsonify({'user_id': '1',
					'person_text':'',
					'timestamp':datetime.datetime.now().isoformat(),
					'bear_text':'You have made a development error.'})



@app.route('/ping')
def ping():
	return jsonify('pong')

@app.route('/DanceMove')
def dance():
	response = "Nothing"
	if danceMove.DANCE_MOVE == DanceMove.DANCE:
		response = "Dance"
	elif danceMove.DANCE_MOVE == DanceMove.WAVE:
		response = "Wave"
	elif danceMove.DANCE_MOVE == DanceMove.CUDDLE:
		response = "Cuddle"
	
	danceMove.setDance(DanceMove.NOTHING)
	
	return jsonify(response)


if __name__ == '__main__':
	# This is used when running locally only. When deploying to Google App
	# Engine, a webserver process such as Gunicorn will serve the app. This
	# can be configured by adding an `entrypoint` to app.yaml.
	# Flask's development server will automatically serve static files in
	# the "static" directory. See:
	# http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
	# App Engine itself will serve those files as configured in app.yaml.
	global dancemove
	dancemove = DanceMove.NOTHING
	app.run(host='127.0.0.1', port=8080, debug=True)
	
