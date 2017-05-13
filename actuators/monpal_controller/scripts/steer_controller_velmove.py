#!/usr/bin/env python
# cording: utf-8
import RPi.GPIO as GPIO
import sys, time,math
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseArray, Pose
import tf

class steer_controller:
	pins = [pin_cw,pin_ccw] = [15,13]
	minmax = 35				#max arg(degree) 
	speed_ratio = 7.2
	s_arg = 0.1125 / speed_ratio				#step arg(degree)
	width = 0.00025
	speed = 0.27
	wheel_base = 0.9
	next_pose_num = 4

	def __init__(self):
		self.subscriber = rospy.Subscriber("move_base/TebLocalPlannerROS/teb_poses", PoseArray, self.callback)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pins,GPIO.OUT)
		GPIO.output(self.pins, GPIO.LOW)
		self.current_step = 0 #current position
		self.arg_step = 0
		self.arg = 0

	def callback(self, ros_data):
		current_pose = ros_data.poses[1]
		if len(ros_data.poses) < self.next_pose_num:
			next_pose = ros_data.pose[-1]
		else:
			next_pose = ros_data.poses[self.next_pose_num]

		current_arg = 2 * math.asin(current_pose.orientation.z)
		next_arg = 2 * math.asin(next_pose.orientation.z)

		#current_arg =  tf.transformations.euler_from_quaternion(current_pose)
		#next_arg = tf.transformations.euler_from_quaternion(next_pose)
		self.arg = math.degrees(next_arg - current_arg)

		print "current_pose_angle:" + str(math.degrees(current_arg))
		print "next_pose_angle" + str(math.degrees(next_arg))
		#self.arg = math.degrees(math.pi - self.arg / 2)
		if abs(self.arg) > self.minmax:
			self.arg = self.minmax * (self.arg / abs(self.arg))
		self.arg_step = int(self.arg / self.s_arg)
		print "steering angele:" + str(self.arg)
		self.drive_motor()

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
		
