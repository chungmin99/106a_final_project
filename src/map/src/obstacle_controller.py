#!/usr/bin/env python
import rospy
import sys

#Import the String message type from the /msg directory of
#the std_msgs package.

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf.transformations import euler_from_quaternion as efq

import numpy as np

def foobar(index):

  pub = rospy.Publisher('robot%d/cmd_vel' % index, Twist, queue_size=10)

  # curr_dir, prev_pose
  params = {'cd': 1, 'pp': None}

  def callback(message):
    oldTwist = Twist()
    curr_pose = message.pose.pose
    
    curr_dir, prev_pose = params['cd'], params['pp']
    # TODO: need to avoid wall sliding
    if prev_pose is not None:
      del_x = prev_pose.position.x == curr_pose.position.x
      del_y = prev_pose.position.y == curr_pose.position.y
      
      eul = [
              curr_pose.orientation.x,
              curr_pose.orientation.y,
              curr_pose.orientation.z,
              curr_pose.orientation.w
              ]

      if np.isclose(np.mod(efq(eul, axes='sxyz')[0], np.pi/2), 0):
        if del_x and del_y:
          curr_dir *= -1
      else:
        if del_x or del_y:
          curr_dir *= -1
    prev_pose = curr_pose

    params['cd'], params['pp'] = curr_dir, prev_pose
    twist = Twist()
    twist.linear.x = curr_dir
    
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    
    pub.publish(twist)
    oldTwist = twist

  return callback

# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /talker.
  rospy.init_node('talker', anonymous=True)
  
  # TODO we should've launched whatever turtle obstacles from launch file
  try:
    for i in range(1, int(sys.argv[1])+1):
      rospy.Subscriber("robot%d/odom" % i, Odometry, foobar(i))
    rospy.spin()
  except rospy.ROSInterruptException: 
    pass
