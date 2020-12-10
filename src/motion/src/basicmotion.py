#!/usr/bin/env python

import rospy
import tf2_ros
import sys
import numpy as np
from numpy import inf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Range
from nav_msgs.msg import Odometry

import importlib
_map_msg = importlib.import_module('map.msg')

def motion_controller():
	global firstdata
	global boolotherodom
	boolotherodom = False
	firstdata = True
	test = rospy.Subscriber('/robot0/odom', Odometry, odomcallback, queue_size =10)
	pub = rospy.Subscriber('/robot_list/pos', _map_msg.OdomList, otherodom, queue_size=10)
	test_sonar = rospy.Subscriber('/robot0/sonar_0', Range, sonar0callback, queue_size=10)
	test_sonar1 = rospy.Subscriber('/robot0/sonar_1', Range, sonar1callback, queue_size=10)
	test_sonar2 = rospy.Subscriber('/robot0/sonar_2', Range, sonar2callback, queue_size=10)
	laser_subscriber  = rospy.Subscriber('/robot0/laser_0', LaserScan, straightLineAvoidance, queue_size=10)
	
	rospy.spin()

def odomcallback(message):
	global originalodom
	originalodom = message

def otherodom(message):
	global otherodom
	global boolotherodom
	boolotherodom = True
	otherodom = message

def sonar0callback(message):
	global sonar0
	sonar0 = message

def sonar1callback(message):
	global sonar1
	sonar1 = message

def sonar2callback(message):
	global sonar2
	sonar2 = message

def wiggleleft(wigglespeed):
	motion_publisher = rospy.Publisher('/robot0/cmd_vel', Twist, queue_size=10)
	#print("Wiggleleft")
	control_command = Twist()

	control_command.linear.x = 0
	control_command.linear.y = wigglespeed
	motion_publisher.publish(control_command)

	control_command.linear.x = wigglespeed
	control_command.linear.y = 0
	motion_publisher.publish(control_command)


def wiggleright(wigglespeed):
	motion_publisher = rospy.Publisher('/robot0/cmd_vel', Twist, queue_size=10)
	#print("Wiggleright")
	control_command = Twist()

	control_command.linear.x = 0
	control_command.linear.y = -1*wigglespeed
	motion_publisher.publish(control_command)

	control_command.linear.x = wigglespeed
	control_command.linear.y = 0
	motion_publisher.publish(control_command)


def dynamicPassiveAvoid(xdiff, ydiff):
	motion_publisher = rospy.Publisher('/robot0/cmd_vel', Twist, queue_size=10)

	control_command = Twist()

	print("AVOIDING")

	control_command.linear.x = -0.5/ydiff*0.1
	control_command.linear.y = -0.5/xdiff*0.1

	# Limit max movement speed so that the robot does not teleport

	if control_command.linear.x > 0.3:
		control_command.linear.x = 0.3
	if control_command.linear.x < -0.3:
		control_command.linear.x = -0.3
	if control_command.linear.y > 0.3:
		control_command.linear.y = 0.3
	if control_command.linear.y < -0.3:
		control_command.linear.y = -0.3


	print(control_command.linear.x)
	motion_publisher.publish(control_command)


def straightLineAvoidance(message):
	motion_publisher = rospy.Publisher('/robot0/cmd_vel', Twist, queue_size=10)
	
	currx = originalodom.pose.pose.position.x
	curry = originalodom.pose.pose.position.y
	if (curry > 13):
	    control_command = Twist()
	    control_command.linear.x = 0
	    control_command.linear.y = 0
	    motion_publisher.publish(control_command)
	    return

########################### DYNAMIC OBSTACLES ################################


	if boolotherodom:
	    currx = originalodom.pose.pose.position.x
	    curry = originalodom.pose.pose.position.y
	    #print('X:',currx)
	    #print('Y:',curry)
	    robotnum = []
	    robotcoorx = []
	    robotcoory = []
            for i in range(len(otherodom.pointarray)):
		robotnum.append(i+1)
		robotcoorx.append(otherodom.pointarray[i].x)
		robotcoory.append(otherodom.pointarray[i].y)
	    
	    robotnum = np.asarray(robotnum)
	    robotcoorx = np.asarray(robotcoorx)
	    robotcoory = np.asarray(robotcoory)

	    mindistance = 99999
	    closestrobot = 0
        index = 0
        for i in range(len(robotnum)):
        	distance = ((robotcoorx[i]-currx)**2+(robotcoory[i]-curry)**2)**0.5
        	if distance<mindistance and curry < robotcoory[i]+0.5:
		    	mindistance = distance
		    	closestrobot = robotnum[i]
		    	index = i

	    #print('Closest Robot: ',closestrobot)
	    #print('Distance : ', mindistance)
		if (abs(robotcoorx[index]-currx) <= 0.8) and (abs(robotcoory[index]-curry) <= 0.8):
			dynamicPassiveAvoid(robotcoorx[index]-currx,robotcoory[index]-curry)
			return

	    

















############################# STATIC OBSTACLES ##################################


	global pastlaser
	laser_data = message
	global firstdata


	# SPEED PARAMETERS
	wigglespeed = 0.3




	midsonar = sonar0.range
	leftsonar = sonar1.range
	rightsonar = sonar2.range


	Angle_min = laser_data.angle_min
	Angle_max = laser_data.angle_max
	Angle_incr = laser_data.angle_increment
	Laser_ranges = np.asarray(laser_data.ranges)

	# sets all inf to max laser dist
	Laser_ranges[Laser_ranges == inf] = laser_data.range_max

	if (firstdata == False):
	    if np.array_equal(pastlaser,Laser_ranges):
		wiggleleft(wigglespeed)
		wiggleright(wigglespeed)
		pastlaser = Laser_ranges
		return

		
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
	    #print("avgleft")

	    control_command.linear.y = avgLeftmid/laser_data.range_max*1
	elif (avgLeftmid < avgRightmid):
	    #print("avgright")
	    control_command.linear.y = avgRightmid/laser_data.range_max*-1

	# STUCK CONDITIONS
	if (leftsonar < 0.36 and leftsonar < rightsonar):
	    #print("stuckleft")
	    control_command.linear.x = 0.3
	    control_command.linear.y = -0.3
	elif (rightsonar < 0.36 and rightsonar < leftsonar):
	    #print("stuckright")
	    control_command.linear.x = 0.3
	    control_command.linear.y = 0.3

     	motion_publisher.publish(control_command)

	firstdata = False
	pastlaser = Laser_ranges
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

