#!/usr/bin/env python
# cording: utf-8
def send_data(socketio, json_rpc):
	socketio.emit('my_request', json_rpc)