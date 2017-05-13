#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

import rospy
from nmea_msgs.msg import Sentence

import socket
from contextlib import closing

class reach_tcp_nmea_node:

	def __init__(self):
		self.pub = rospy.Publisher('nmea_sentence', Sentence, queue_size=50)
		
	def publish_nmea(self,sentence, frame_id):
		msg = Sentence()
		msg.header.stamp = rospy.get_rostime()
		msg.header.frame_id = frame_id
		msg.sentence = sentence
		
		self.pub.publish(msg)
		

def main():
	rospy.init_node('reach_tcp_nmea_node', anonymous=True)

	host = rospy.get_param('~host','192.168.42.1')
	port = rospy.get_param('~port',8080)
	frame_id = "gps"

	try:
		nmea = reach_tcp_nmea_node()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		with closing(sock):
			sock.connect((host, port))
			while not rospy.is_shutdown():
				recv_msg = sock.recv(1024)
				for i in recv_msg.splitlines():
					try:
						nmea.publish_nmea(i, frame_id)
					except ValueError as e:
						rospy.logwarn("Value Error")


	except rospy.ROSInterruptException:
		sock.close()
	
	
if __name__ == '__main__':
	main()
