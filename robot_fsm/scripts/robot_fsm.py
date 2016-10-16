#!/usr/bin/env python

import rospy

from std_msgs.msg import Empty
############# Configuration area ############
TIMEOUT = 7
ALLOWED_COMMANDS = ['PARK_THERE', 'GO_THERE','RETURN_TO_BASEEEE']
#############################################

class FsmState:
    Idle = 0
    startTrig = 1
    StartCaptureTrig = 2
    CaptureCountDown = 3
    TakeCapture = 4


class FSM(object):

    def __init__(self):

        self.received_manual_trigger = False
        self.state = FsmState.Idle
        rospy.Subscriber('manual_trigger', Empty, self.manual_trigger_callback)

        self.pause_pub = rospy.Publisher('/pause_navigation',Empty)
        self.resume_pub = rospy.Publisher('/resume_navigation',Empty)

        rospy.on_shutdown(self.shutdown_callback)


    def manual_trigger_callback(self, msg):
        self.received_manual_trigger = True




    def shutdown_callback(self):
        rospy.loginfo('Shutting down')


    def run_fsm(self):

        chakalaka = 0

        while not rospy.is_shutdown():
            rospy.sleep(0.1)

            chakalaka += 1
            print chakalaka
            if chakalaka == 20:
                chakalaka = 0
                print 'chakalaka off'
            elif chakalaka >= 10 and chakalaka < 20:
                print 'chakalaka off'
            elif chakalaka < 10 and chakalaka >= 0 :
                print 'chakalaka on'
            else:
                chakalaka = 0



            if self.state == FsmState.Idle: 
                resume = 1
                pause = 0 
                time_out = 0        
                print 'state 1 - idle'
                msg = Empty()
                rospy.sleep(0.5)
                self.resume_pub.publish(msg)  
                if self.received_manual_trigger:
                    self.state = FsmState.startTrig
                    self.received_manual_trigger =False
                    rospy.loginfo('Transition: Idle --> startTrig')
                continue

            elif self.state == FsmState.startTrig:
                resume = 0
                pause = 1
                print 'state 2 - startTrig'
                print 'align robot view - pass values to navigation block '
                msg = Empty()
                rospy.sleep(0.5)
                self.pause_pub.publish(msg)  
                time_out += 1
                if time_out == 300:
                    self.state = FsmState.Idle
                    self.received_manual_trigger = False
                    print 'time out - return to idle mode'
                    continue

                if self.received_manual_trigger:
                    self.state = FsmState.CaptureCountDown
                    self.received_manual_trigger = False
                    rospy.loginfo('Transition: Idle --> CaptureCountDown')
                continue


            elif self.state == FsmState.CaptureCountDown:
                resume = 0
                pause = 1
                print 'state 3 - captureCountDown'
                print 'stop passing values to the robot '                
                msg = Empty()
                rospy.sleep(0.5)
                self.pause_pub.publish(msg)  
                for num in range(10):
                    rospy.sleep(1)
                    print '%d' % (10-num)
                self.state = FsmState.TakeCapture
                rospy.loginfo('Transition: Idle --> TakeCapture')
                continue

            elif self.state == FsmState.TakeCapture:
                resume = 0
                pause = 1
                print 'state 4 - TakeCapture'
                print 'take snap shot'
                msg = Empty()
                rospy.sleep(0.5)
                self.pause_pub.publish(msg)                
                rospy.sleep(2)
                print 'waited for 2 sec'
                self.state = FsmState.Idle
                self.received_manual_trigger = False
                continue






if __name__ == '__main__':
    rospy.init_node('robot_fsm', anonymous=True)

    fsm = FSM()

    fsm.run_fsm()
