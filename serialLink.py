#!/usr/bin/python -u

# the serial sometimes has an error which is every time:
# Error: No Line Number with checksum, Last Line:0
# it comes with a header 0R0
# good one: ZTPS100
# bad one:  ZTP*0R0

import serial
import socket
import time
import argparse
import glob
import sys,os
import select

MyID = 'S'
ReqID = '*'

def getLineTrim(s):
    try:
        ans = s.recv(14323)
        print ans
        #return ans[7:]
        return ans[8:].strip(), ans[3]
    except:
        #print 'No answer recived...'
        return None, ReqID

def readline():
	buf=[]
	while True:
		c=os.read(0,1)
		if not c or c == '\n': break
		buf.append(c)
	return ''.join(buf)

def sort_and_send(s, text):
    '''Adds special headers to the message according to 
    the content (which is determined by its first letter)
    and sends them'''
    c = text[0] # the reply is...
    if  c == 'o': # ...confirming responnse (starts with 'ok')
        s.send("ZT" + ReqID + MyID + "100 " + text)

    elif  c == 'X': # ...g-code
        s.send("ZT" + ReqID + MyID + "200 " + text)

    else:
        s.send(text) 
        return

s=socket.socket()
while True:
    try:
        s.connect(('localhost',14323))
        s.settimeout(0.02)
        print "Connected to router at '14323'..."
        s.send("ZX*" + MyID + "0000\n")
        break
    except:
        print "Router not found at '14323', trying again..."
        time.sleep(3)

exit = False
while not exit:
    ser=None
    try:
        ser=serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_741323435303516172E0-if00", baudrate=250000, timeout=0.02)
        print "connected..."
        time.sleep(3)
        ser.write("M105\n")         #first command behaves in a strange way
        while ser.readline():       #skip the starting messages of the printer
            pass
        ser.write("M302 P1\n")      #allow cold extrusion
        ser.write("T1\n")           #switch to syringe pump as head2
        ser.write("G91\n")          #switch to relative coordinates
        ser.write("M92 E969.76\n")  #set step per unit for 1 unit = 1 ul
        ser.write("M203 E4\n")      #set extrude speed lower
        ser.write("M201 X10 Y10 E10") #set max acceleration
        while ser.readline():       #read all remaining answers 
            pass
        print "setup completed..."
        
        while not exit:
            i,o,e = select.select( [sys.stdin], [], [], .02)
            if i == "exit":
                exit = True
                #raise KeyboardInterrupt
            cmd, ReqID = getLineTrim(s)
            if cmd:
                print "In:  " + cmd.strip()
                ser.write(cmd + '\n')
                        
            recivedLine = ser.readline() #blocking w timeout
            if recivedLine:
                print "Out: " + recivedLine.strip()
                #s.send("ZX" + str(ReqID) + MyID + "000" + recivedLine)
                sort_and_send(s, recivedLine)
    except: 
        if ser is not None:
            ser.close()
        time.sleep(5)
        print "Connection failed trying again..."
