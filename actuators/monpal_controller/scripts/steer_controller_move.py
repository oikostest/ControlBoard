#!/usr/bin/env python
# cording: utf-8
import RPi.GPIO as GPIO
import sys, time,math
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class steer_controller:
	pins = [pin_cw,pin_ccw] = [13,15]
	minmax = 35				#max arg(degree) 
	speed_ratio = 3.6
	s_arg = 0.1125 / speed_ratio				#step arg(degree)
	width = 0.00025
	speed = 0.27
	wheel_base = 0.9

	def __init__(self):
		self.subscriber = rospy.Subscriber("cmd_vel", Twist, self.callback)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pins,GPIO.OUT)
		self.current_step = 0 #current position
		self.arg_step = 0
		self.arg = 0

	def callback(self, ros_data):
		self.arg = math.degrees(self.convert_trans_rot_vel_to_steering_angle(ros_data.linear.x, ros_data.angular.z))
		if abs(self.arg) > self.minmax:
			self.arg = self.minmax * (self.arg / abs(self.arg))
		self.arg_step = int(self.arg / self.s_arg)
		print(self.arg)
		self.drive_motor()
	
	def convert_trans_rot_vel_to_steering_angle(self,v,omega):
		if omega == 0 or v == 0:
			return 0
		radius = self.speed / omega
		return math.atan( self.wheel_base / radius)

	def drive_motor(self):		
		self.step_n = self.arg_step - self.current_step
		if self.step_n != 0:
			self.stepper = int(self.step_n / abs(self.step_n))
			self.direction = int((self.stepper + 1) / 2)
			while abs(self.step_n) > 0:
				self.step(self.direction)
				self.step_n -= self.stepper
		else:
			GPIO.output(self.pins,GPIO.LOW)
		GPIO.output(self.pins, GPIO.LOW)

	def step(self,direction):
		GPIO.output(self.pins[direction], GPIO.HIGH)
		time.sleep(self.width)
		GPIO.output(self.pins[direction], GPIO.LOW)
		time.sleep(self.width)
		self.current_step += self.stepper
	
	def close_pin(self):
		GPIO.cleanup()

def main(args):
	rospy.init_node('steer_controller', anonymous=True)
	sc = steer_controller()

	try:
		rospy.spin()
	except KeyboardInterruput:
		print "Shutting down ROS motor controller"
		mc.close_pin()	

if __name__ == '__main__':
	main(sys.argv)
		
