# coding: GB2312
#!/usr/bin/env python

"""
SMPP,SuperMap Parallel Processor
Desc: 
	SMPP basic function using SMB logic. 
	SMB is Super Message Bus, here using AMQP via RabbitMQ
Author: WangEQ, SuperMap GIS Institute.
All rights reserved.
"""

import math
import time
import sys

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message
import simplejson as json

#=====Global variable===================================
str_Jobs = 'com.supermap.smpp.jobs'
str_Status = 'com.supermap.smpp.status'
str_Server = 'localhost'
global ch_Status
global ch_Jobs

def start(on_connect):
	global conn
	global io_loop

	logging.basicConfig()
	conn = Connection(host=str_Server)
	conn.connect(on_connect)
	io_loop = IOLoop.instance()
	io_loop.start()

def createStatusChannel():
	global ch_Status
	ch_Status = conn.channel()
	ch_Status.exchange_declare(exchange=str_Status,type='fanout')

def createJobsSender():
	global ch_Jobs
	ch_Jobs = conn.channel()
	ch_Jobs.queue_declare(queue=str_Jobs)	
	
def createJobsReceiver(on_job):	
	global ch_Jobs
	ch_Jobs = conn.channel()
	ch_Jobs.queue_declare(queue=str_Jobs,durable=True)	
	ch_Jobs.qos(prefetch_count=1)
	ch_Jobs.consume(str_Jobs, on_job, no_ack=False)

def send_job(job):
	global ch_Jobs
	ch_Jobs.publish(job, exchange='', routing_key=str_Jobs)
	
def sendStatus(strStatusInfo):
	'Send status to Monitor on another queue.'
	global ch_Status
	strReport = ["status","status info."]
	strReport[1] = strStatusInfo
	strReport_json = json.dumps(strReport)
	msgReport = Message(strReport_json)
	ch_Status.publish(msgReport, exchange=str_Status, routing_key='')
	return strReport_json

def close():
	conn.close(callback=done)
	
def done():
	print " End."
	io_loop.stop()

if __name__ == '__main__':
	print "SMB base definition."
