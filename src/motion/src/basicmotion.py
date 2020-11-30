#!/usr/bin/env python

import rospy
import tf2_ros
import sys
import numpy as np
from numpy import inf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Range


def motion_controller():

	test_sonar = rospy.Subscriber('/robot1/sonar_0', Range, sonar0callback, queue_size=10)
	test_sonar1 = rospy.Subscriber('/robot1/sonar_1', Range, sonar1callback, queue_size=10)
	test_sonar2 = rospy.Subscriber('/robot1/sonar_2', Range, sonar2callback, queue_size=10)
	laser_subscriber  = rospy.Subscriber('/robot1/laser_0', LaserScan, straightLineAvoidance, queue_size=10)
	
	rospy.spin()

def sonar0callback(message):
	global sonar0
	sonar0 = message

def sonar1callback(message):
	global sonar1
	sonar1 = message

def sonar2callback(message):
	global sonar2
	sonar2 = message	
	
def straightLineAvoidance(message):
	motion_publisher = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)
	
	laser_data = message

	
	midsonar = sonar0.range
	leftsonar = sonar1.range
	rightsonar = sonar2.range


	Angle_min = laser_data.angle_min
	Angle_max = laser_data.angle_max
	Angle_incr = laser_data.angle_increment
	Laser_ranges = np.asarray(laser_data.ranges)

	# sets all inf to max laser dist
	Laser_ranges[Laser_ranges == inf] = laser_data.range_max
		
	size = len(Laser_ranges)
	Rightranges = Laser_ranges[0:size/5]
	Rightmidranges = Laser_ranges[size/5+1:2*size/5]
	Middleranges = Laser_ranges[2*size/5+1:3*size/5]
	Leftmidranges = Laser_ranges[3*size/5+1:4*size/5]
	Leftranges = Laser_ranges[4*size/5+1:size]

	avgRight = np.mean(Rightranges)
	avgRightmid = np.mean(Rightmidranges)
	avgLeft = np.mean(Leftranges)
	avgLeftmid = np.mean(Leftmidranges)
	avgMid = np.mean(Middleranges)

	control_command = Twist()

	# FORWARD CONDITIONS
	if (midsonar < 0.5):
	    control_command.linear.x = 0
	else:
	    control_command.linear.x = avgMid/laser_data.range_max*1


	# SIDEWAYS CONDITIONS
	if (avgLeftmid >= avgRightmid):
	    print("avgleft")

	    control_command.linear.y = avgLeftmid/laser_data.range_max*1
	elif (avgLeftmid < avgRightmid):
	    print("avgright")
	    control_command.linear.y = avgRightmid/laser_data.range_max*-1

	# STUCK CONDITIONS
	if (leftsonar < 0.36):
	    print("stuckleft")
	    control_command.linear.x = 0.1
	    control_command.linear.y = -0.3
	elif (rightsonar < 0.36):
	    print("stuckright")
	    control_command.linear.x = 0.1
	    control_command.linear.y = 0.3

     	motion_publisher.publish(control_command)
"""
	if (midsonar < 0.5):
		if (rightsonar > 2*midsonar):
			print("sonarright")
			control_command.linear.y = -1
			control_command.linear.x = 0
		elif (leftsonar > 2*midsonar):
			print("sonarleft")
			control_command.linear.y = 1
			control_command.linear.x = 0
		else:
			print("up")
			control_command.linear.x = avgMid/laser_data.range_max*1
			control_command.linear.y = 0
	elif (avgMid > 0.6*laser_data.range_max):
		print("up")
		control_command.linear.x = avgMid/laser_data.range_max*1
		control_command.linear.y = 0
	elif (avgLeftmid > avgRightmid):
		print("avgleft")
		control_command.linear.y = 1
		control_command.linear.x = 0
	elif (avgLeftmid > avgRightmid):
		print("avgright")
		control_command.linear.y = -1
		control_command.linear.x = 0
"""

if __name__ == '__main__':

  rospy.init_node('robot_controller', anonymous=True)

  try:
    motion_controller()
  except rospy.ROSInterruptException:
    pass

