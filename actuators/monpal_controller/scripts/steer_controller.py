#!/usr/bin/env python
# cording: utf-8
import RPi.GPIO as GPIO
import sys, time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class steer_controller:
	pins = [pin_Ap,pin_An,pin_Bp,pin_Bn] = [13,15,16]
	minmax = 30				#max arg(degree) 
	s_arg = 0.5				#step arg(degree)
	width = 0.01

	stepper = [[0,1],[2,3]]
	hl = [GPIO.HIGH,GPIO.LOW]

	def __init__(self):
		self.subscribe()
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pins,GPIO.OUT)
		GPIO.output()
		self.current_step = 0 #current position
		self.arg_step = 0

	def callback(self, ros_data):
		self.arg = self.minmax * ros_data.angular.z
		self.arg_step = int(self.arg / self.s_arg)

	def drive_motor(self):		
		self.step_n = self.arg_step - self.current_step
		print(self.current_step ,self.step_n)
		if self.step_n != 0:
			direction = -1 * int(self.step_n / abs(self.step_n))
			self.step(direction)
			self.step_n -= direction
		else:
			for i in range(0,4):
				GPIO.output(self.pins[i],GPIO.LOW)

	def step(self,direction):
		var = direction -1
		for i in range(0,2):
			for j in self.stepper:
				GPIO.output(self.pins[j[0] + var], self.hl[i])
				GPIO.output(self.pins[j[1] + var], self.hl[i - 1])
				time.sleep(self.width)
		self.current_step -= direction
	
	def subscribe(self):
		self.subscriber = rospy.Subscriber("cmd_vel", Twist, self.callback)
		
	def close_pin(self):
		GPIO.cleanup()

def main(args):
	rospy.init_node('steer_controller', anonymous=True)
	rate = rospy.Rate(100)

	sc = steer_controller()

	while not rospy.is_shutdown():
		sc.subscribe()
		sc.drive_motor()
		rate.sleep()

if __name__ == '__main__':
	main(sys.argv)
		
