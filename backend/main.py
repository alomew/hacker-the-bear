import datetime

from flask import Flask, render_template, jsonify, request
from google.cloud import datastore
from rpi.Mitsuku import MitsukuBot

app = Flask(__name__)


bot = MitsukuBot()


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
	keyWords = {"sad","lonely","unhappy","kill","die","depressed","death","hungry","tired","stiff","pain","aching"}
    if json:
        try:
			person_text = json["person_text"]
			bad = False
			for word in person_text:
				if word in keyWords:
					bad = True
					break
			if not bad:
            	bear_text = bot.sendMessage(person_text)[1:-1]
			else:
				bear_text = "Do you want some help?"
        except:
            bear_text = "I need some sleep."
        json['bear_text'] = bear_text
        return jsonify(json)

    return jsonify({'user_id': '1',
                    'person_text':'',
                    'timestamp':datetime.datetime.now().isoformat(),
                    'bear_text':'You have made a development error.'})



@app.route('/ping')
def ping():
    return jsonify('pong')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
