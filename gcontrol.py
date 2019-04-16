#!/usr/bin/python -u

import socket
import time

class Position:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    # change position by the given coordinates
    def move(self, x=None, y=None, z=None):
        if x: self.x += x
        if y: self.y += y
        if z: self.z += z
    
    # sets the position to the given coords
    def setTo(self, x=None, y=None, z=None):
        if x: self.x = x
        if y: self.y = y
        if z: self.z = z

    def toString(self):
        print("X:" + str(self.x), " Y:" + str(self.y) + " Z:" + str(self.z))
    
    def getxy(self):
        return "X" + str(self.x) + " Y" + str(self.y)

    def getz(self):
        return "Z" + str(self.z)
    def getxyz(self):
        return "X" + str(self.x) + " Y" + str(self.y) + " Z" + str(self.z)

# sends the header and gcode sting to a socket
# if 'wait' is true, it needs two 'ok' responses...
# ...from the socket (printer) to return
# TODO could be a timeout here...
def send(soc, header, gcode, wait=True):
    soc.send(header + gcode + "\n")
    if wait: soc.send(header + "M400\n")
    recived = executed = not wait
    
    exec_try = 0
    while not executed and exec_try > 20:
        try:
            ans = soc.recv(14343)
        except socket.timeout: 
            ans = None
        try:
             # if the printer echoes 'ok', the header is '100'
            if ans[4] == '1':
                if recived == True:
                    executed = True
                else:
                    recived = True
        except:
            exec_try += 1
            pass