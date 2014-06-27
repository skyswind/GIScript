# coding: GB2312
#! /usr/bin/env python
#Global Log System

from datetime import datetime, date, time

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message
import simplejson as json

str_GlogServer = 'localhost'

ch_Status = None
str_Status = None

def on_connect():
	global ch_Glog
	global str_Glog
	str_Glog = 'com.supermap.smpp.glog'
	ch_Glog = conn.channel()
	ch_Glog.exchange_declare(exchange=str_Glog,type='fanout')	
	ch_Glog.queue_declare(exclusive=True,callback=with_status_queue)	

	#ch_Glog.queue_declare(queue=str_Glog,durable=True)	
	ch_Glog.qos(prefetch_count=1)
	#ch_Glog.consume(str_Glog, on_job, no_ack=False)

def with_status_queue(qinfo):
	ch_Glog.queue_bind(exchange=str_Glog,queue=qinfo.queue)
	ch_Glog.consume(qinfo.queue, on_Glog, no_ack=True)

#显示信息
def on_Glog(msg):
	print "[",datetime.now(),"]"
	#print ">>%s" % msg.body
	glog_analyst(msg)

#后续分析	
def glog_analyst(msg):
	strMsg = json.loads(msg.body)
	if strMsg[0]=="glog":
		print "LOG:",msg.body
	else:
		print "Log: Unknown Data."

def start():
	global conn
	global io_loop
	
	logging.basicConfig()
	conn = Connection(host=str_GlogServer)
	conn.connect(on_connect)
	io_loop = IOLoop.instance()
	io_loop.start()

if __name__ == '__main__':
	print '>>Global Log Service Start...'
	start()	
	
