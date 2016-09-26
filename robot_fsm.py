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
                rospy.sleep(2)
                print 'waited for 2 sec'
                self.state = FsmState.Idle
                self.received_manual_trigger = False
                continue






if __name__ == '__main__':
    rospy.init_node('robot_fsm', anonymous=True)

    fsm = FSM()

    fsm.run_fsm()

'''

 def Run_FSM(self):



        while True :
            time.sleep(0.1)

            print 'in the loop'

            if self.state == FsmState.Idle:
                # navigate outputs
                print 'state 1'

                pause = 0
                resume = 1
                left_navigate = 0
                right_navigate = 0

                # tablet outputs


                return_to_normal = 1
                trig_start = 0
                capture_take = 0
                count = 0
                start_count = 0

                # internal

                start_time_out = 0
                end_time_out = 0

                if self.trigger == 1:
                    self.state = FsmState.startTrig
                else:
                    self.state = FsmState.Idle
                continue

            elif self.state == FsmState.startTrig:

                # navigate outputs
                print 'state 2'

                pause = 1
                resume = 0
                left_navigate = self.left_turn
                right_navigate = self.right_turn

                # tablet outputs


                return_to_normal = 0
                trig_start = 1
                capture_take = 0
                count = 10
                start_count = 0

                # internal

                start_time_out = 1
                end_time_out = 0

                if self.trigger == 0:
                    self.state =  FsmState.WaitForCaptureTrig
                else:
                    self.state = FsmState.startTrig
                continue

            elif self.state == FsmState.WaitForCaptureTrig:

                # navigate outputs
                print 'state 3'

                pause = 1
                resume = 0
                left_navigate = self.left_turn
                right_navigate = self.right_turn

                # tablet outputs


                return_to_normal = 0
                trig_start = 1
                capture_take = 0
                count = 10
                start_count = 0

                # internal

                start_time_out = 1
                end_time_out = 0

                if self.trigger == 1:
                    self.state =  FsmState.CaptureCountDown
                else:
                    self.state = FsmState.WaitForCaptureTrig
                continue

            elif self.state == FsmState.CaptureCountDown:

                # navigate outputs
                print 'state 4'

                pause = 1
                resume = 0
                left_navigate = 0
                right_navigate = 0

                # tablet outputs


                return_to_normal = 0
                trig_start = 1
                capture_take = 0
                count = 10
                start_count = 1


                for num in range(count):
                    print num
                    time.sleep(1)

                # internal

                start_time_out = 1
                end_time_out = 0

                if num == 9:
                    self.state =  FsmState.TakeCapture
                else:
                    self.state = FsmState.CaptureCountDown
                continue

            elif self.state == FsmState.TakeCapture:

                # navigate outputs
                print 'state 5'

                pause = 1
                resume = 0
                left_navigate = 0
                right_navigate = 0

                # tablet outputs


                return_to_normal = 0
                trig_start = 0
                capture_take = 1
                count = 0
                start_count = 0


                # internal

                start_time_out = 1
                end_time_out = 0


                time.sleep(1)

                self.state = FsmState.Idle

                continue

            else:
                self.state = FsmState.Idle


            if pause == 1:
                outputs = 'move right %d move left %d' % (right_navigate, left_navigate)
            else:
                outputs = 'not triggered'

            print outputs


            '''