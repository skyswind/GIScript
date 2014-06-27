# coding: GB2312
#!/usr/bin/env python

"""
SMPP,SuperMap Parallel Processor
Desc: 
	Worker to process jobs from SMB. 
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
import SMB
#=================================================================

global handle_Worker

def on_connect():
	SMB.createStatusChannel()
	SMB.createJobsReceiver(on_job)

#on received job.
def on_job(msg):
	'Main Worker, Process the job.'
	print "Received Job: %r" % msg.body
	strJob = json.loads(msg.body)
	if strJob[0]=="job":
		SMB.sendStatus(strJob[1])		
		handle_Worker(strJob[1])
	else:
		print "That's not My Job:"
		print "Head:",strJob[0]
		print "Body:",strJob[1]
	msg.ack()

#Just for test.	
def do_job(job):
	SMB.sendStatus("Job Begin: %r"%job)
	print "Doing Job:", job
	time.sleep(2)
	SMB.sendStatus("Job Finish: %r"%job)

if __name__ == '__main__':
	handle_Worker=do_job
	SMB.start(on_connect)
