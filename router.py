#!/usr/bin/python -u
 
from Queue import Queue
from threading import Thread, Event
from socket import *
import serial
import time
from select import select
import argparse

p = argparse.ArgumentParser(description='message router')
p.add_argument('--port', metavar='14323', type=int, default=14323, help='socket port (default: 14323)')
p.add_argument('--filter', metavar='T', type=float, default=-1.0, help='filter duplicate messages by remembering IDs for T seconds. No filtering (default) for T<0. ')
p.add_argument('--log', action='store_true', help='printing message traffic')
cla=p.parse_args()

#queue bundle, for two-way communication between threads
class qb(object):
  def __init__(self):
	self.used=Event()		#events are flags that can be waited for
	self.reset()

  def reset(self):
	self.addresses=set('*')		#a set, containing the broadcast address
	self.used.clear()			#object is not used
	self.toR=Queue()			#to router hub
	self.fromR=Queue()			#to socket connections

N_MAX = 20					#number of connections
qbs = []
for i in range(N_MAX):
	qbs.append(qb())

def parse(line):
	if line[0]=='Z': return line[2], line[3], line[4]
	return None 

def router():
  seen={}
  while True:
		for q,qb in enumerate(qbs):
			if qb.toR.empty(): continue
			line=qb.toR.get()
			if cla.log: 
				print
				print time.strftime("%a, %d %b %Y %H:%M:%S ",time.localtime()),
				print "{0:<22}".format(line.strip()), "\t | ", q,
			try:
				TO,FRM,ID=parse(line)
			except: continue					#bad format
			if (TO,FRM,ID) in seen and seen[(TO,FRM,ID)] > time.time(): continue
			seen[(TO,FRM,ID)] = time.time() + cla.filter 
			qb.addresses.add(FRM)		#if exists, will not be duplicated
			for i,qb2 in enumerate(qbs):
				if qb2 is not qb and TO in qb2.addresses and qb2.used.isSet():
					if cla.log: print " -> %d " % i,
					qb2.fromR.put(line)
		time.sleep(0.01)
			


def handleConnection(conn, qb):
  conn.setblocking(1)	#calls block until they can proceed
  while True:
	if not qb.fromR.empty():
	  try:
	  	if conn.sendall(qb.fromR.get()) == 0: break
	  except: break
	r,w,e = select([conn],[],[],.01)	
					#returns ready_to_read, ready_to_write, in_error
					#10 msec timeout
  	if r:	#conn has stuff to read
			buf=[]
			while True:
				c=conn.recv(1)
				if not c or c=='\n': break
				buf.append(c)
			line=''.join(buf)
			if not line: break	 # end of input
			qb.toR.put(line+'\n')
  qb.reset()				# either end of input @ socket or @ serial
							# frees up queue object for reuse
  conn.close()
  print "exiting.."


# see https://docs.python.org/2/howto/sockets.html
def runServer(s,port,qbs):
  while True:
  	try:
  		s.bind( ("", port) )
		print "listening as socket port %d." % port
		break
  	except:
		time.sleep(5)
		print "retrying socket port.."
  s.listen(1)  			#we deal with only one connection request at a time
						#other connections are refused

  s.settimeout(2)		#transaction must be completed in 2 sec

  while True:
	for qb in qbs:
	  if not qb.used.isSet(): break		#found a queue bundle not yet connected.
	if qb.used.isSet(): 	# all queue bundles are used, nothing to do
	  time.sleep(1)
	  continue
	try:				# have a queue not connected yet
	  (in_conn, in_addr) = s.accept()
	  print "connected.."
	  qb.used.set() 
	  Thread(target=handleConnection, args=(in_conn, qb)).start()
	except timeout: continue

Thread(target=router).start()
Thread(target=runServer, args=(socket(),cla.port,qbs)).start()
