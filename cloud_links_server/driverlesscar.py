#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from move_base_msgs.msg import MoveBaseActionGoal
from std_msgs.msg import String
import requests, pyjsonrpc, json


class DriverlessCar:
	def __init__(self):
		self.latitude = '31.253708'
		self.longitude = '130.655714'
		self.subscriber = rospy.Subscriber("fix", NavSatFix, self.__callback)
		self.goalpub = self.publisher = rospy.Publisher('goal', MoveBaseActionGoal, queue_size=50)

	def get_status(self):
		status = {'lat' : self.latitude, 'lon' : self.longitude}
		return status

	def set_destination(self,destination):
		print destination['latitude']
		print destination['longitude']
		msg = MoveBaseActionGoal()
		msg.header.stamp = rospy.get_rostime()
		msg.header.frame_id = frame_id
		msg.sentence = sentence
		
		self.pub.publish(msg)
		return "a"

	def pick_user_up(self,current_location, destination):
		pass

	def __callback(self,ros_data):
		self.latitude = ros_data.latitude
		self.longitude = ros_data.longitude


if __name__ == '__main__':
	dc = DriverlessCar()
	rospy.init_node('driverless_car', anonymous=True)
	try:
		rospy.spin()
	except rospy.ROSInterruptException:
		print "Shutting down ROS driverless_car"
