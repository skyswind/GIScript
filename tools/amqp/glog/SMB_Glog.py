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

#启动链接到消息服务总线	
def start():
	global smbHost
	global conn
	global io_loop
	logging.basicConfig()
	conn = Connection(host=smbHost)
	conn.connect(on_connect)
	io_loop = IOLoop.instance()
	io_loop.start()

#消息发送主流程
def on_connect():
	global str_Glog
	global ch_Glog

	#建立任务分发通道
	ch_Glog = conn.channel()
	ch_Glog.exchange_declare(exchange=str_Glog,type='fanout')
	writeLog()
	close()

#内部调用,写入消息服务总线	
def writeLog():
	'Send status to Monitor on another queue.'
	ch_Glog.publish(msgLog, exchange=str_Glog, routing_key='')

#关闭链接
def close():
	conn.close(callback=done)

#发送结束,执行清理工作	
def done():
	io_loop.stop()
	print "Glog:", msgLog.body

#外部调用,写入日志信息
def log(strLogInfo):
	global msgLog
	strLog = ["glog","glog info."]
	strLog[1] = strLogInfo
	strLog_json = json.dumps(strLog)
	msgLog = Message(strLog_json)
	start()

#测试一下
def test_glog():
	print "Dispatch Glog:"
	for i in range(1,10):
		log(i)
		time.sleep(2)

smbHost = 'localhost'
str_Glog = 'com.supermap.smpp.glog'
	
if __name__ == '__main__':

	test_glog()
