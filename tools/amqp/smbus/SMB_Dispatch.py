# coding: GB2312
#!/usr/bin/env python

"""
SMPP,SuperMap Parallel Processor
Desc:
	Dispatch jobs information to SMB. 
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
global handle_Dispatcher

def on_connect():
	SMB.createStatusChannel()
	SMB.createJobsSender()	
	handle_Dispatcher()	#Call task dispatcher delegate.

def build_Job(jobCMD):
	strJob = ["job","do job"]
	strJob[1] = jobCMD
	strJob = json.dumps(strJob)	
	msgJob = Message(strJob)
	return msgJob
	
#Just for test.	
def dispatch_jobs(ch):
	print "Dispatch Jobs: Job one. "
	job = build_Job(r'Job One')
	SMB.send_job(job)
	
if __name__ == '__main__':
	handle_Dispatcher = dispatch_jobs
	SMB.start(on_connect)
