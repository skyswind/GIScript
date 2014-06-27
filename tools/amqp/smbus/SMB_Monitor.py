# coding: GB2312
#! /usr/bin/env python

"""
SMPP,SuperMap Parallel Processor
Desc:
	The Monitor of Status, reveived from SMB.
	
Author: WangEQ, SuperMap GIS Institute.
All rights reserved.
"""

from datetime import datetime, date, time

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message
import simplejson as json

ch_Status = None
str_Status = None

def on_connect():
	global ch_Status
	global str_Status
	str_Status = 'com.supermap.smpp.status'
	ch_Status = conn.channel()
	ch_Status.exchange_declare(exchange=str_Status,type='fanout')	
	ch_Status.queue_declare(exclusive=True,callback=with_status_queue)	

def with_status_queue(qinfo):
	ch_Status.queue_bind(exchange=str_Status,queue=qinfo.queue)
	ch_Status.consume(qinfo.queue, on_status, no_ack=True)

def on_status(msg):
	print "[",datetime.now(),"]"
	print ">>%s" % msg.body
	#status_analyst(msg)
	
def status_analyst(msg):
	strMsg = json.loads(msg.body)
	if strMsg[0]=="status":
		print "status analyst:",msg.body
	else:
		print "Status: Unknown Data."
		print "Head:",strMsg[0]
		print "Body:",strMsg[1]

def Start():
	global conn
	global io_loop
	logging.basicConfig()
	conn = Connection(host='localhost')
	conn.connect(on_connect)
	io_loop = IOLoop.instance()
	io_loop.start()
	print ' [*] Waiting for messages. To exit press CTRL+C'

if __name__ == '__main__':
	Start()
#try:
#    io_loop.start()
#except KeyboardInterrupt:
#    conn.close(io_loop.stop)
