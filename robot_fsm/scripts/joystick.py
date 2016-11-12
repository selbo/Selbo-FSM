#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
import json
import websocket

class Joystick(object):
    def __init__(self):
        rospy.init_node('joystick')
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
        self.horizontal = 0
        self.vertical = 0

        websocket.enableTrace(True)
        self.my_ws = websocket.WebSocketApp("ws://130.211.184.58:8000",
                        on_message = self.on_ws_message,
                        on_error = self.on_ws_error,
                        on_close = self.on_ws_close)
        self.my_ws.on_open = self.on_ws_open
        self.my_ws.run_forever()        

    def on_ws_open(self, ws):
        pass
        
    def on_ws_message(self, ws, message):
        print "### inside on_message ###"
        print message
        try:
            j = json.loads(str(message))
            cmd = j['cmd']
            data = j['data']
            if cmd in ['joystick_horizontal', 'joystick_vertical']:
                if abs(data) < 10:
                    return
                if cmd == 'joystick_horizontal':
                    self.horizontal = data
                elif cmd == 'joystick_vertical':
                    self.vertical = data

                msg = Twist()
                if self.vertical > self.horizontal:
                    msg.linear.x = -0.001 * self.vertical
                else:
                    msg.angular.z = 0.008 * self.horizontal
                rospy.sleep(0.1)
                self.pub_cmd_vel.publish(msg)

        except:
            print 'Ignoring this message'

    def on_ws_error(self, ws, error):
        print error

    def on_ws_close(self,ws):
        print "### closed ###"

    '''
    def run(self):
        while not rospy.is_shutdown():
            msg = Empty()
            rospy.sleep(10)
            self.pub_pause.publish(msg)
            msg = Empty()
            rospy.sleep(5)
            self.pub_resume.publish(msg)
    '''

        
        
if __name__ == '__main__':
    try:
        j = Joystick()
    finally:
        j.my_ws.close()
    #rospy.spin()
    #h.run()

    

