#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import os,sys
import rospy
from sensor_msgs.msg import NavSatFix, NavSatStatus
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import requests, pyjsonrpc, json

base = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.normpath(os.path.join(base,'../data'))

class DriverlessCar:
	def __init__(self,state_fix_topic):
		self._latitude = '31.253708'
		self._longitude = '130.655714'
		#Load destination fixed (x,y,z,w)
		filename = os.path.join(datapath,'fixeddestination.json')
		with open(filename,'r') as f:
			self._lists = json.load(f)
		self._subscriber = rospy.Subscriber('/fix', NavSatFix, self.__callback)
		#goal in llh
		self._goalfixpub = rospy.Publisher('utm', NavSatFix, queue_size=50)
		#goal in map pose
		self._goalpub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=50)

	def get_status(self):
		status = {'method':"get_status", 'lat' : self._latitude, 'lon' : self._longitude, 'car_number': 1}
		return status

	def set_destination(self,destination):
		msg = NavSatFix()
		msg.header.stamp = rospy.get_rostime()
		msg.header.frame_id = "utm"
		msg.latitude = float(destination['latitude'])
		msg.longitude = float(destination['longitude'])
		msg.altitude = 0
		msg.status.status = NavSatStatus.STATUS_GBAS_FIX
		msg.status.service = 0
		msg.position_covariance = [0] * 9
		msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN
		self._goalfixpub.publish(msg)
		ret = {'method':"set_destination", 'msg': "set"}
		return ret

	def set_fixed_destination(self,fixedkey):
		name = fixedkey['location_name']
		print name
		if name in self._lists:
			goal = PoseStamped()
			goal.header.frame_id = "map"
			goal.pose.position.x = self._lists[name]['position.x']
			goal.pose.position.y = self._lists[name]['position.y']
			goal.pose.orientation.z = self._lists[name]['orientation.z']
			goal.pose.orientation.w = self._lists[name]['orientation.w']
			goal.header.stamp = rospy.Time()
			print "pub goal"
			self._goalpub.publish(goal)
			ret = {'method':"set_fixed_destination", 'msg': "set destination"}
		else:
			ret = {'method':"set_fixed_destination", 'msg': "unknow destination"}
		return ret

	def load_fixed_destination(self):

		ret = {'method':"load_fixed_destination", 'location_name' : self._lists.keys()}
		return ret

	def save_fixed_destination(self,keyvalue,destination):
		
		return "save it"


	def pick_user_up(self,current_location, destination):
		pass

	def __callback(self,ros_data):
		self._latitude = ros_data.latitude
		self._longitude = ros_data.longitude


if __name__ == '__main__':
	dc = DriverlessCar()
	rospy.init_node('driverless_car', anonymous=True)
	try:
		rospy.spin()
	except rospy.ROSInterruptException:
		print "Shutting down ROS driverless_car"
