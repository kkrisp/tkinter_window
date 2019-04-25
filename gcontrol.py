#!/usr/bin/python -u

import socket
import time

class Position:
    def __init__(self, x, y, z):
         self.x = x
         self.y = y
         self.z = z
    
    # move position with the given coordinates
    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
    
    # sets the position to the given coords
    def setTo(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def toString(self):
        return ("X: " + str(self.x)+ " Y: " + str(self.y) + " Z: " + str(self.z))
    
    def getxy(self):
        return "X" + str(self.x) + " Y" + str(self.y)

    def getz(self):
        return "Z" + str(self.z)

def send(soc, header, gcode, wait=True, tries=1):
    """Sends the G-code to the given socket
    with the given header

    Keyword arguments:
    wait -- waits for an 'ok' answer from the printer (default=True)
    tries -- this many attempts to send the code
    """
    soc.send(header + gcode + "\n")
    if wait: soc.send(header + "M400\n")
    recived = executed = not wait

    while not executed:
        try:
            ans = soc.recv(14343)
        except socket.timeout:
            if tries>1: # resending message, if answer timed out 'tries' times 
                        # starts from 1, because of the first try outside the loop
                soc.send(header + gcode + "\n")
                soc.send(header + "M400\n")
                tries -= 1
                continue
            #print "Error in gcontrol.py: socket timeout while waiting for answer"
            else:
                return
        try:
             # if the printer echoes 'ok', the header is '100'
            if ans[4] == '1':
                if recived == True: # command already recived
                    executed = True # second 'ok' answer for executing the command
                else:
                    recived = True  # first 'ok' answer for reciveing the command
        except:
            pass
