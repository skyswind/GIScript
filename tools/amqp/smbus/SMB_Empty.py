# coding: GB2312
#!/usr/bin/env python
#SMUP-Parallel,SuperMap Universal Processor Parallel
# File: SMUPP.py
# Author: WangEQ, SuperMap GIS Institute.
# Desc: 

import math
import time
import sys
import SMUP
import SMUP_Image
import SMB
import subprocess

#=================================================================
def do_empty(job):
	SMB.sendStatus("Job Empty: %r"%job)
	
if __name__ == '__main__':
	SMB.handle_Processor = do_empty
	SMB.Start()
