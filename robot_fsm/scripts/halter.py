#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty


class Halter(object):
    def __init__(self):
        rospy.init_node('halter')
        self.pub_pause = rospy.Publisher('/pause_navigation',Empty, queue_size=1)
        self.pub_resume = rospy.Publisher('/resume_navigation',Empty, queue_size=1)

    def run(self):
        while not rospy.is_shutdown():
            msg = Empty()
            rospy.sleep(10)
            self.pub_pause.publish(msg)
            msg = Empty()
            rospy.sleep(5)
            self.pub_resume.publish(msg)

if __name__ == '__main__':
    h = Halter()
    h.run()

