#!/usr/bin/env python

import rospy
import sys
from tf.transformations import euler_from_quaternion as efq

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import numpy as np

OBSTACLE_STALL_DELAY = 20
OBSTACLE_DEBOUNCE = 10

def foobar(index):

  pub = rospy.Publisher('robot%d/cmd_vel' % index, Twist, queue_size=10)

  # curr_dir, prev_pose, stuck_time
  params = {'cd': 1, 'pp': None, 'stuck': 0, 'debounce': 0}

  def callback(message):
    oldTwist = Twist()
    curr_pose = message.pose.pose
    curr_dir, prev_pose = params['cd'], params['pp']
    stuck_time, deb = params['stuck'], params['debounce']

    # 1. Obstacle bounce detection
    if prev_pose is not None:

      # a. get current pose
      del_x = prev_pose.position.x == curr_pose.position.x
      del_y = prev_pose.position.y == curr_pose.position.y
      
      eul = [
              curr_pose.orientation.x,
              curr_pose.orientation.y,
              curr_pose.orientation.z,
              curr_pose.orientation.w
              ]

      one_axis_only = np.isclose(np.mod(efq(eul, axes='sxyz')[0], np.pi/2), 0)

      # b. robot is "stuck" if both x and y locations don't change, but looser
      # conditions for obstacles moving only along x- or y- axis
      curr_stuck = (del_x and del_y) if one_axis_only else (del_x or del_y)

      # we only chdir if the robot has been stuck here for above a threshold
      # time in order to remove in-place bouncing
      if curr_stuck:
          stuck_time += 1
          if stuck_time > OBSTACLE_STALL_DELAY and deb > OBSTACLE_DEBOUNCE:
              curr_dir *= -1
              deb = 0
          else:
              deb += 1
      else:
          stuck_time = 0
          deb += 1

    # 2. Update prev_pose for next run
    prev_pose = curr_pose
    params['cd'], params['pp'] = curr_dir, prev_pose
    params['stuck'], params['debounce'] = stuck_time, deb

    # 3. Publish new twist to cmd_vel
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
