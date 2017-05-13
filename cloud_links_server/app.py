#!/usr/bin/env python
# cording: utf-8

#setup env
#pip install flask-socketio pyjsonrpc

from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, send, emit, disconnect
import json
import pyjsonrpc
import send_socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
count = 0
msg = ""

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/post', methods = ['POST'])
def hello():
	global msg
	if request.method == 'POST':
		## set destination with lat and long
		if request.form['action'] == 'post':
			data = {'latitude' : request.form['latitude'], 'longitude' : request.form['longitude']}
			request_json = pyjsonrpc.create_request_json("DriverlessCar.set_destination",data)
			parsed_response = json.loads(request_json)
			print json.dumps(parsed_response, indent=4)
			send_socketio.send_data(socketio,request_json)
		## set fixed destination with key value
		if request.form['action'] == 'setfixed':
			data = { 'location_name' : request.form['fixedkey']}
			request_json = pyjsonrpc.create_request_json("DriverlessCar.set_fixed_destination",data)
			parsed_response = json.loads(request_json)
			print json.dumps(parsed_response, indent=4)
			send_socketio.send_data(socketio,request_json)
		## get current status of driverlesscar
		if request.form['action'] == 'getpos':
			request_json = pyjsonrpc.create_request_json("DriverlessCar.get_status")
			send_socketio.send_data(socketio,request_json)
		## load keyvalue of fixed destination
		if request.form['action'] == 'loadpos':
			request_json = pyjsonrpc.create_request_json("DriverlessCar.load_fixed_destination")
			send_socketio.send_data(socketio,request_json)
	return render_template('index.html', message = msg)


@socketio.on('my_response')
def print_response_message(response):
	parsed_response = json.loads(response)
	print json.dumps(parsed_response, indent=4)
	global msg
	if "result" in parsed_response:
		if parsed_response["result"]['method'] == u"get_status":
			lat = parsed_response["result"]["lat"]
			lon = parsed_response["result"]["lon"]
			msg = "lat:" + str(lat) + "  " + "lon:" + str(lon)
	elif "error" in parsed_response:
		msg = parsed_response["error"]

	emit('redirect',{'url': url_for('hello')}, broadcast=True)


if __name__ == '__main__':
	socketio.run(app, port=5000)
