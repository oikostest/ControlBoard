#!/usr/bin/env python
# cording: utf-8
import RPi.GPIO as GPIO
import sys, time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

AMP_RANGE = 2.9
OFFSET = 8.7

class ms_controller:

	def __init__(self):
                self.subscriber = rospy.Subscriber("cmd_vel", Twist, self.callback)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18,GPIO.OUT)
		GPIO.setup(12,GPIO.OUT)
                self.st_pin = GPIO.PWM(12,58)
                self.st_pin.start(0)
                self.st_pin.ChangeDutyCycle(8.7)
                self.sp_pin = GPIO.PWM(18,58)
                self.sp_pin.start(0)
                self.sp_pin.ChangeDutyCycle(8.7)
                
	def callback(self, ros_data):
		sp = OFFSET - int(ros_data.linear.x * AMP_RANGE)
		st = OFFSET - int(ros_data.angular.z * AMP_RANGE)
		sp_duty = float(sp)
		st_duty = float(st)
		self.sp_pin.ChangeDutyCycle(sp_duty)
		self.st_pin.ChangeDutyCycle(st_duty)

	def close_pin(self):
		self.sp_pin.stop(0)
		self.st_pin.stop(0)
		GPIO.cleanup()

def main(args):
	mc = ms_controller()
	rospy.init_node('ms_controller', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterruput:
		print "Shutting down ROS motor controller"
		mc.close_pin()	

if __name__ == '__main__':
	main(sys.argv)
		
