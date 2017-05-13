#!/usr/bin/env python
# cording: utf-8
import RPi.GPIO as GPIO
import sys, time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

ACCEL = 11
STEER = 12

class ms_controller:

	def __init__(self):
                self.subscriber = rospy.Subscriber("cmd_vel", Twist, self.callback)
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(ACCEL,GPIO.OUT) #Accel
		#GPIO.setup(12,GPIO.OUT) #Steering
		GPIO.output(ACCEL, False)
                
	def callback(self, ros_data):
		if ros_data.linear.x > 0:
			GPIO.output(ACCEL, True)
		else:
			GPIO.output(ACCEL, False)

		#st = OFFSET - int(ros_data.angular.z * AMP_RANGE)

	def close_pin(self):
		GPIO.cleanup()

def main(args):
	mc = ms_controller()
	rospy.init_node('monpal_controller', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterruput:
		print "Shutting down ROS motor controller"
		mc.close_pin()	

if __name__ == '__main__':
	main(sys.argv)
		
