# coding: GB2312
#!/usr/bin/env python

"""
SMPP,SuperMap Parallel Processor
Desc:
	The Worker example to process jobs from SMB. 
Author: WangEQ, SuperMap GIS Institute.
All rights reserved.
"""

import math
import time
import sys

import SMB
import SMB_Worker

#=================================================================
def do_job(job):
	print "Do Job:", job
	SMB.sendStatus("Job Begin: %r"%job)
	print "Doing something:", job
	time.sleep(2)
	SMB.sendStatus("Job Finish: %r"%job)
	
if __name__ == '__main__':
	SMB_Worker.handle_Processor = do_job	
	SMB.start(SMB_Worker.on_connect)
