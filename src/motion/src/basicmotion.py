#!/usr/bin/env python

import rospy
import tf2_ros
import sys
import numpy as np
from numpy import inf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def motion_controller():
	
	
	laser_subscriber  = rospy.Subscriber('/robot1/laser_0', LaserScan, straightLineAvoidance, queue_size=10)
	

	rospy.spin()

	
def straightLineAvoidance(message):
	motion_publisher = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)
	
	laser_data = message
			
	Angle_min = laser_data.angle_min
	Angle_max = laser_data.angle_max
	Angle_incr = laser_data.angle_increment
	Laser_ranges = np.asarray(laser_data.ranges)

	# sets all inf to max laser dist
	Laser_ranges[Laser_ranges == inf] = laser_data.range_max
		
	size = len(Laser_ranges)
	Leftranges = Laser_ranges[0:size/3]
	Middleranges = Laser_ranges[size/3+1:2*size/3]
	Rightranges = Laser_ranges[2*size/3+1:size]

	avgLeft = np.mean(Leftranges)
	avgRight = np.mean(Rightranges)
	avgMid = np.mean(Middleranges)

	control_command = Twist()

	if (avgMid > 0.6*laser_data.range_max):
		control_command.linear.x = 1
		control_command.linear.y = 0
	elif (avgRight > avgLeft):
		control_command.linear.y = 1
		control_command.linear.x = 0
	else:
		control_command.linear.y = -1
		control_command.linear.x = 0
		
	

     	motion_publisher.publish(control_command)

if __name__ == '__main__':

  rospy.init_node('robot_controller', anonymous=True)

  try:
    motion_controller()
  except rospy.ROSInterruptException:
    pass

