#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty
import json
import websocket

class Halter(object):
    def __init__(self):
        rospy.init_node('halter')
        self.pub_pause = rospy.Publisher('/pause_navigation',Empty, queue_size=1)
        self.pub_resume = rospy.Publisher('/resume_navigation',Empty, queue_size=1)

	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("ws://104.198.196.211:8000",
				    on_message = self.on_ws_message,
				    on_error = self.on_ws_error,
				    on_close = self.on_ws_close)
	ws.on_open = self.on_ws_open
	#ws.run_forever()

    def on_ws_open(self, ws):
	pass
		
    def on_ws_message(self, ws, message):
	print "### inside on_message ###"
	j = json.loads(message)
	if message['cmd'] == 'nav':
	    if message['data'] == 'pause':			
		msg = Empty()
		rospy.sleep(0.5)
		self.pub_pause.publish(msg)
	    elif message['data'] == 'resume':
		msg = Empty()
		rospy.sleep(0.5)
		self.pub_resume.publish(msg)

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
    h = Halter()
    print 'finished halter initialization'
    rospy.spin()
    #h.run()
    ws.close()

    

