# coding: GB2312
#!/usr/bin/env python
#SMUP-Parallel,SuperMap Universal Processor Parallel
# File: SMUPP.py
# Author: WangEQ, SuperMap GIS Institute.
# Desc: 

import math
import time
import sys

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message
import simplejson as json


#=================================================================
global handle_Dispatcher

def on_connect():
	global str_Glog
	global ch_Glog
	
	str_Glog = 'com.supermap.smpp.glog'
	
	#建立任务分发通道
	ch_Glog = conn.channel()
	ch_Glog.exchange_declare(exchange=str_Glog,type='fanout')
	#ch_Glog.queue_declare(exclusive=True,callback=with_status_queue)
	
	handle_Dispatcher(ch_Glog)
	
def start():
	global conn
	global io_loop

	logging.basicConfig()
	conn = Connection(host='localhost')
	conn.connect(on_connect)
	io_loop = IOLoop.instance()
	io_loop.start()

def close():
	conn.close(callback=done)
	
def done():
	print " End."
	io_loop.stop()
	
def log(strLogInfo):
	'Send status to Monitor on another queue.'
	strLog = ["glog","glog info."]
	strLog[1] = strLogInfo
	strLog_json = json.dumps(strLog)
	msgLog = Message(strLog_json)
	ch_Glog.publish(msgLog, exchange=str_Glog, routing_key='')
	return strLog_json

def dispatch_glog(ch):
	print "Dispatch Glog:"
	for i in range(1,10):
		log(i)
	
if __name__ == '__main__':
	handle_Dispatcher = dispatch_glog
	start()
	
