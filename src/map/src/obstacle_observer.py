#!/usr/bin/env python
import rospy
import sys

#Import the String message type from the /msg directory of
#the std_msgs package.

from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry

import importlib
_map_msg = importlib.import_module('map.msg')

from tf.transformations import euler_from_quaternion as efq

import numpy as np


def update_data(index):
  def callback(message):
    curr_pose = message.pose.pose.position
    position_list.pointarray[index] = curr_pose

  return callback    

# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /obstacle_observer.
  rospy.init_node('obstacle_observer', anonymous=True)
  position_list = [0 for i in range(int(sys.argv[1]))]


  position_list = _map_msg.OdomList()
  for i in range(int(sys.argv[1])):
	position_list.pointarray.append(Point())


  # TODO we should've launched whatever turtle obstacles from launch file
  try:
    pub = rospy.Publisher('robot_list/pos', _map_msg.OdomList, queue_size=10)

    for i in range(1, int(sys.argv[1])+1):
      rospy.Subscriber("robot%d/odom" % i, Odometry, update_data(i-1))
   
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
      pub.publish(position_list)
      r.sleep()
    rospy.spin()

  except rospy.ROSInterruptException as e: 
    print(e)
    pass
