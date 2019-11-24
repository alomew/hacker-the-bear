from datetime import datetime, timedelta, date

from twilio.rest import Client

import os

from flask import Flask, render_template, jsonify, request
from google.cloud import datastore
from rpi.Mitsuku import MitsukuBot
import random
from analysis.dbclass import Database
from enum import Enum

class DanceMove:
	

	NOTHING = 0
	DANCE = 1
	WAVE = 2
	CUDDLE = 3

	DANCE_MOVE = WAVE
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

def fetch_speeches_for_date(d):
	query = datastore_client.query(kind="speech")
	query.order = ['-timestamp']
	query.add_filter('timestamp', '>=', datetime.combine(d, datetime.time.min))
	query.add_filter('timestamp', '<=', datetime.combine(d, datetime.time.max))
	return(list(query.fetch(100)))

def store_message(message_json):
	message_json['been_said'] = False
	entity = datastore.Entity(key=datastore_client.key('message'))
	entity.update(message_json)

	datastore_client.put(entity)

def fetch_messages(user_id):
	query = datastore_client.query(kind='message')
	query.add_filter('been_said', '=', False)
	query.add_filter('user_id', '=', user_id)
	return list(map(lambda e: e['message'], query.fetch(10)))

def room_for_messages(user_id):
	if len(fetch_messages(user_id)) == 10:
		return False
	return True

def message_available(user_id, name):
	query = datastore_client.query(kind='message')
	query.add_filter('user_id', '=', user_id)
	query.add_filter('user_id', '=', name)
	query.add_filter('been_said', '=', False)

	entitylist = list(query.fetch(1))
	if entitylist:
		entity = entitylist[0]
		entity['been_said'] = True
		datastore_client.put(entity)
		return entity['message_text']
	return None

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
		if room_for_messages(json['user_id']):
			store_speech(json)
			return jsonify(True)
		return jsonify(False)
	else:
		return jsonify(False)

@app.route('/textofperson', methods=['POST'])
def textofperson():
	json = request.get_json()
	print(json)
	#json = {'user_id': "1", 'person_text': 'Hi there', 'timestamp': datetime.datetime.now().isoformat()}
	badWords = {"sad","lonely","unhappy","kill","die", "leave", "depressed","death","stiff","aching", "miss"}
	sosWords = {"fallen", "hurt", "injured", "broken", "pain", "ouch", "help", "stroke", "heart", "attack"}
	happyWords = {"happy", "excited", "nice", "sunny"}
	needWords = {"hungry", "thirsty", "tired", "exhausted", "sleepy"}
	songWords = {"play", "song", "sing"}
	familyWords = {"family", "sister", "daughter", "grandson", "grandaughter"} # include actual names
	memoryWords = {"remember", "remembered"}
	forgetWords = {"forget", "forgotten"}

	rand = random.randint(1,100)
	# If 5 or less, tell them to drink water
	if json:
		try:
			bear_text = ""
			person_text = json["person_text"]
		except Exception as e:
			# byeRes = {"I need some sleep", "I'm tired", "I ought to go, have a wonderful day!", "Goodnight", "Good day"}
			# bear_text = random.sample(byeRes,1)[0]
			bear_text = (str(e))
			json['bear_text'] = bear_text
			return jsonify(json)
		status = 0
		boot = False
		for word in person_text.split(' '):
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
				boot = True

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
			whereAreYou = {"where are you from", "where you from", "where are you at", "where you at", "where are you"}
			howOld = {"how old are you", "what's your age", "whats your age", "how old"}
			
			if boot:
				bots = {"I'm simply a husky, Hacker the husky!", "Look at me, I'm a dog!", "Last time I checked, I was indeed a dog!"}
				bear_text = random.sample(bots,1)[0]
				done = True
				for val in howAreYou:
					if val in person_text.lower():
						okThanks = {"I'm good thank you! How are you?", "I'm pretty great, what about you?", "I'm alright actually. Are you okay?", "Doing well, you?"}
						bear_text = random.sample(okThanks,1)[0]
						done = True
						break
				for val in whatAreYouDoing:
					if val in person_text.lower():
						stuff = {"Talking to you, of course!", "Just enjoying my time, talking to you, what about you?", "Just chilling, you?"}
						bear_text = random.sample(stuff,1)[0]
						done = True
						break
				for val in whereAreYou:
					if val in person_text.lower():
						stuff = {"I've always have been and always will be just here, here with you", "I'll always be by your side", "Just by your side, exactly where I want to be"}
						bear_text = random.sample(stuff,1)[0]
						done = True
						break
			if not done:
				bear_text = bot.sendMessage(person_text)[1:-1]


		if rand < 5:
			drinkRes = {"Hey, make sure you've been drinking enough.", "Have you been drinking? It's been a while", "Make sure you have a glass of water!"}
			bear_text += ". " + random.sample(drinkRes,1)[0]

		json['bear_text'] = bear_text
		return jsonify(json)

	return jsonify({'user_id': '1',
					'person_text':'',
					'timestamp':datetime.datetime.now().isoformat(),
					'bear_text':'You have made a development error.'})


@app.route('/newmessage', methods=['POST'])
def newmessage():
	json = request.get_json()
	if json and room_for_messages(json['user_id']):
		store_message(json)
		return jsonify(True)
	return jsonify(False)


@app.route('/getqueuedmessages', methods=['POST'])
def getqueuedmessages():
	user_id = request.get_json()
	if user_id:
		return jsonify(fetch_messages(user_id))
	return jsonify(None)


@app.route('/ping')
def ping():
	return jsonify('pong')

@app.route('/dance')
def dance():
	danceMove.setDance(DanceMove.DANCE)
	return jsonify('done!')
@app.route('/wave')
def wave():
	danceMove.setDance(DanceMove.WAVE)
	return jsonify('done!')
@app.route('/cuddle')
def cuddle():
	danceMove.setDance(DanceMove.CUDDLE)
	return jsonify('done!')

@app.route('/DanceMove')
def getDance():
	response = "Nothing"
	if danceMove.DANCE_MOVE == DanceMove.DANCE:
		response = "Dance"
	elif danceMove.DANCE_MOVE == DanceMove.WAVE:
		response = "Wave"
	elif danceMove.DANCE_MOVE == DanceMove.CUDDLE:
		response = "Cuddle"
	
	danceMove.setDance(DanceMove.NOTHING)
	
	return jsonify(response)


@app.route('/dailytextfakefakefake')
def sendsms():
	oneday = timedelta(days=1)
	timedata = [[e['timestamp'] for e in fetch_speeches_for_date(date.today() - i*oneday)] for i in range(5)]
	moodtoday = [e['mood_value'] for e in fetch_speeches_for_date(date.today())]
	db = Database()

	long, short = db.analysis(timedata, "Alice", moodtoday)



	account_sid = os.environ['TWILIO_SID']
	auth_token = os.environ['TWILIO_AUTH_TOKEN']
	client = Client(account_sid, auth_token)

	message = client.messages \
		.create(
		body="Test environment variables",
		from_='+12054330045',
		to='+447730692762'
	)

	print(message.sid)




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
	
