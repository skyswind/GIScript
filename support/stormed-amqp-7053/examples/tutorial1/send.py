#! /usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from stormed import Connection, Message

msg = Message('Hello World!')

def on_connect():
	ch = conn.channel()
	ch.queue_declare(queue='hello')	
	SendHello(ch)
	SendNo(ch)	
	conn.close(callback=done)

def SendHello(ch):
	ch.publish(msg, exchange='', routing_key='hello')
	print "Send Hello Finish"
	
def SendNo(ch):
	for i in range(1,10):
		msgno = Message('Hello %(ID)02d'%{"ID":i})
		ch.publish(msgno, exchange='', routing_key='hello')
		print "Send No ",i,"Finish"
		
def done():
	print " End."
	io_loop.stop()

logging.basicConfig()
conn = Connection(host='localhost')
conn.connect(on_connect)
io_loop = IOLoop.instance()
io_loop.start()
