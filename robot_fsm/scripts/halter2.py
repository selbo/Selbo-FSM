#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
import json
import websocket
from geometry_msgs.msg import Twist
import datetime

class Halter(object):
    def __init__(self):
        rospy.init_node('halter')
        self.pub_pause = rospy.Publisher('/pause_navigation',Empty, queue_size=1)
        self.pub_resume = rospy.Publisher('/resume_navigation',Empty, queue_size=1)
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)

        websocket.enableTrace(True)
        self.my_ws = websocket.WebSocketApp("ws://104.198.196.211:8000",
                                on_message = self.on_ws_message,
                                on_error = self.on_ws_error,
                                on_close = self.on_ws_close)
        self.my_ws.on_open = self.on_ws_open
        self.last_cmd_vel = None

        self.my_ws.run_forever()

    def on_ws_open(self, ws):
        pass

    def cmd_vel_callback(self, msg):
        self.last_cmd_vel = datetime.datetime.now()
        
    def on_ws_message(self, ws, message):
        print "### inside on_message ###"
        print message
        try:
            j = json.loads(str(message))    
            if j['cmd'] == 'nav':
                if j['data'] == 'pause':
                    print 'received pause'
                    msg = Empty()
                    rospy.sleep(0.5)
                    self.pub_pause.publish(msg)
                    json_ack_dict = {}
                    json_ack_dict['cmd'] = 'nav_status'
                    json_ack_dict['data'] = 'paused'
                    jack_ack = json.dumps(json_ack_dict)
                    self.my_ws.send(jack_ack)
                elif j['data'] == 'resume':
                    print 'received resume'
                    msg = Empty()
                    rospy.sleep(0.5)
                    self.pub_resume.publish(msg)
                    json_ack_dict = {}
                    json_ack_dict['cmd'] = 'nav_status'
                    json_ack_dict['data'] = 'resumed'
                    jack_ack = json.dumps(json_ack_dict)
                    self.my_ws.send(jack_ack)

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
        h = Halter()
    finally:
        h.my_ws.close()
    #rospy.spin()
    #h.run()

