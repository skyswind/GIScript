# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 17:02:55 2012

@author: supermap
"""
import time
from datetime import datetime
from threading import Timer

import httplib
import SMB_Glog

def  mon_SuperMapCloud(ch):
	conn = httplib.HTTPConnection("www.supermapcloud.com")
	conn.request("GET", "/cloudweb/")
	
	r1 = conn.getresponse()
	#print r1.status, r1.reason
	print "[",datetime.now(),"]",
	if r1.status==200:
		print "SuperMapCloud OK."
		SMB_Glog.log("SuperMapCloud Status: OK")
	else:
		SMB_Glog.log("SuperMapCloud Problem!")
	#data1 = r1.read()
	#print data1
	conn.close()

def mon_smcloud():
	print "Dispatch Glog:"
	#while(1):
	for i in range(1,10):
		Mon_SuperMapCloud(ch)
		time.sleep(1)

if __name__ == '__main__':
	mon_smcloud()
	