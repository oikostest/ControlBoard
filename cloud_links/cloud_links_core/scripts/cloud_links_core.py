#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import sys,os
import rospy
from std_msgs.msg import String
from socketIO_client import SocketIO
import requests, pyjsonrpc, json
from driverlesscar import DriverlessCar

class cloud_links_core:

	def __init__(self, host, port, post_namespace, rpc):
		self.host = host
		self.port = port
		self.post_namespace = post_namespace
		self.host_url = host + ":" + str(port) + post_namespace
		self.rpc = rpc
		#self.__onReady()

		self.socketIO = SocketIO(self.host, port)
		self.socketIO.on('my_request', self.on_my_resquest)
		# self.socketIO.on('redirect', self.on_redirect)

	def __onReady(self):
		request_json = pyjsonrpc.create_request_json("onReady")
		self.send_msg(request_json)

	def send_msg(self,value):
		requests.post(self.host_url, value)
		# parsed_response = json.loads(response)
		# print json.dumps(parsed_response, indent=4)

	def on_my_resquest(self,request):
		parsed_request = json.loads(request)
		print json.dumps(parsed_request, indent=4)
		response_json = self.rpc.call(request)	
		#self.socketIO.emit('my_response', response_json)

	# def on_redirect(self,request):
	# 	print "hello"
	# 	pass


class JsonRpc(pyjsonrpc.JsonRpc):
	def __init__(self, api_obj):
		api_methods = dir(api_obj)
		apis = filter(lambda m: not m.startswith('_'), api_methods)
		[self.__setitem__(api_obj.__class__.__name__ + "." + api ,getattr(api_obj,api)) for api in apis]


def main():
	rospy.init_node('cloud_links_core', anonymous=True)

	host_url = rospy.get_param('~host_url','http://124.219.162.203')
	port = rospy.get_param('~port',5300)
	namespace = rospy.get_param('~namespace', '/car_status_post')
	status_pubfreq = rospy.get_param('~status_publish_frequency', 10)
	publish_status = rospy.get_param('~publish_status', True)
	state_fix_topic = rospy.get_param('~state_fix_topic', "fix")

	driverlesscar = DriverlessCar(state_fix_topic)
	rpc = JsonRpc(driverlesscar)

	try:
		core = cloud_links_core(host_url, port, namespace, rpc)
		while not rospy.is_shutdown():
			if publish_status:
				#request_json = pyjsonrpc.create_request_json("CarStatus",driverlesscar.get_status())
				jsonmsg = json.dumps(driverlesscar.get_status())
				print json.loads(jsonmsg)
				core.send_msg(jsonmsg)
				core.socketIO.wait(seconds = status_pubfreq)
	except rospy.ROSInterruptException:
		sock.close()
 
if __name__ == '__main__':
    main()