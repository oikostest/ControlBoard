#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import rospy
import tf2_ros
import tf2_geometry_msgs
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class utm_simple_goal:
	def __init__(self,utm_odom_topic):
		self.utm_odom = rospy.Subscriber(utm_odom_topic, Odometry, self.callback)
		self.goalpub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=50)		
		self.goal = PoseStamped()
		self.odom_pose = PoseStamped()
		self.odom_pose_flag = False
		#tf2 setup
		self.tfBuffer = tf2_ros.Buffer()
		self.tfListener = tf2_ros.TransformListener(self.tfBuffer)

	def callback(self,odom):
		self.odom_pose_flag = True
		self.odom_pose.header = odom.header
		self.odom_pose.pose = odom.pose.pose

	def publish(self):
		if self.odom_pose_flag == True:
			self.odom_pose_flag = False
			self.goal.header.frame_id = self.odom_pose.header.frame_id
			self.goal = tf2_geometry_msgs.do_transform_pose(self.odom_pose, self.trans)
			self.goal.header.stamp = rospy.Time()
			self.goal.pose.orientation.x = 0
			self.goal.pose.orientation.y = 0
			self.goal.pose.orientation.z = 0.12
			self.goal.pose.orientation.w = 0.99
			self.goalpub.publish(self.goal)
		else:
			rospy.loginfo("it has not get goal odom topic")

	def set_transform(self):
		self.trans = self.tfBuffer.lookup_transform('map','utm', rospy.Time())
		


def main():
	rospy.init_node('utm_simple_goal', anonymous=True)

	#Get Parameters
	utm_odom_topic = rospy.get_param('~utm_odom_topic', "odom/goal")

	simple_goal = utm_simple_goal(utm_odom_topic)
	rate = rospy.Rate(1)

	while not rospy.is_shutdown():
		try:
			try:
				simple_goal.set_transform()
			except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
				rate.sleep()
				continue
			simple_goal.publish()
		except rospy.ROSInterruptException:
			break

 
if __name__ == '__main__':
    main()
