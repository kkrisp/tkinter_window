import socket
import time
import gcontrol as g
from gcontrol import Position as Position_o


class Position(Position_o):
    """Extending the position class. Contains the
    coordinates and the type of the position of the
    printer head (X, Z) and table (Z)."""

    # the valid types of the positions
    postype_list = ["plain", "petri", "source", "ceiling"]

    def __init__(self, x=0, y=0, z=0, postype="plain"):
        self.x = x
        self.y = y
        self.z = z
        self.postype = None

        # in case of invalid type 'plain' is used instead
        if postype in Position.postype_list:
            self.postype = postype
        else:
            self.postype = "plain"
    
    def get_type(self):
        return self.postype

    def set_type(self, postype):
        if postype in Position.postype_list:
            self.postype = postype

    def string_c(self):
        return str(self.x), str(self.y), str(self.z)


class Message:
    """Simplifies the g-code sending via gcontrol.send
    by storing the header, socket and sending options"""
    def __init__(self, link_socket, header, wait=True, tries=3):
        self.link_socket = link_socket
        self.header = header
        self.wait = wait
        self.tries = tries
    def send(self, gcode):
        print("Sending: "+gcode)
        return #TODO dummy action here for testing
        g.send(self.link_socket, self.header, self.wait, self.tries)


class Printer:
    """Represents the printer, the program is connected to.
    Contains the
        -saved printer head positions in a dictionary
        -settings for grid printing in a dictionary
    Has functions for saving the current head position
    and printing grids using the settings dict."""

    prID = "P" # the default ID used in the communication with the router

    def __init__(self, socket=None, settings=None, positions=None, target_ID="*"):
        self.header = "ZT" + target_ID + Printer.prID +"000 "
        self.socket = socket
        self.settings = settings
        self.positions = positions
        self.m = Message(self.socket, self.header, wait=True, tries=3)
        if settings == None:
            self.settings={
                "dst":1.0,  # distance
                "d":  0.2,  # size
                "h"  :3.0,  # travel height
                "row":3,    # columns
                "col":3,    # rows
                "h++":0.0,  # change print height
                "t"  :0.0,  # sleep between droplets
                "t++":0.0,  # change sleep time
                "eh" :False,# extrude with head high
                "s"  :False,# print grid in an S route
                "cor":2.3,  # correct hysteresys
                "pul":False,# last extruder action
                "d++":0.0,  # change size
                "hex":False # "hexagonal patter
                }
        if positions == None:
            self.positions = {}
        self.use_petri = None
        self.use_ceiling = None
        self.use_source = None

    def use_for_printing(self, name, postype):
        if postype == "petri":
            self.use_petri = name
        if postype ==  "source":
            self.use_source = name
        if postype ==  "ceiling":
            self.use_ceiling = name

    def parse_position(self):
        # this is what we need to parse:
        # X:51.90 Y:-45.80 Z:-47.70 E:38.96 Count X: 51.90 Y:-45.80 Z:-47.70
        self.socket.send(self.header + "M114" + "\n")
        while True:
            try:
                ans = self.socket.recv(14323)
                #print ans[8:].strip()
            except socket.timeout:
                return None, None, None
            try:
                if ans[4] == '1':
                    return None, None, None
                elif ans[4] == '2': # we got a position back...
                    parsedAns = ans[8:].split(' ')
                    return parsedAns[0][2:], parsedAns[1][2:], parsedAns[2][2:]
            except:
                pass
    
    def save_position(self, name, postype="plain"):
        if postype not in Position.postype_list:
            postype="plain"
        x, y, z = self.parse_position()
        self.positions[name] = Position(x, y, z, postype)
    
    def save_position2(self, name, x, y, z, postype):
        if postype not in Position.postype_list:
            postype="plain"
        self.positions[name] = Position(x, y, z, postype)
        
    def move(self, name):
        self.m.send("G90")              # switch to absolute coordinates
        try:
            self.m.send("G1 " + self.positions[self.use_ceiling].getz() )  # lift head to ceiling
        except KeyError:
            pass
        self.m.send("G1 " + self.positions[name].getxy() ) # go over position
        self.m.send("G1 " + self.positions[name].getz() )  # lower head
        self.m.send("G91")              # switch to relative coordinates

    def printGrid(self):
        opt = self.settings # to shorten lines

        self.m.send("G91")      # switch to relative coordinates
        if opt['pul']:
            self.m.send("G1 E" + str(opt["cor"]))
            opt['pul'] = False
        leftToRight = 1 # 1 if left to right, -1 if right to left
        cnt = 0
        for y in range(opt["row"]):
            for x in range(opt["col"]):
                # extrude high
                if opt["eh"]: self.m.send("G1 E" + str(opt["d"] + opt["d++"] * cnt))
                # lower head
                self.m.send("G1 Z" + str(-opt["h"]))
                # extrude low
                if not opt["eh"]: self.m.send("G1 E" + str(opt["d"] + opt["d++"] * cnt))
                # lift head
                self.m.send("G1 Z" + str(opt["h"]+opt["h++"]*cnt))
                # move over the next dot
                if x < (opt["col"]-1): self.m.send("G1 X" + str(leftToRight*opt["dst"]))
                # wait between dots
                time.sleep(opt["t"] + opt["t++"]*cnt)
                cnt += 1
            # move over the first dot in the next row
            if y<(opt["row"]-1):
                # if S route, move one row down and change direction
                if opt["s"]:
                    self.m.send("G1 Y" + str(-opt["dst"]))
                    leftToRight *= -1
                # if terminal route, move back the whole length and move down
                else:
                    self.m.send("G1 X" + str(-(opt["col"]-1)*opt["dst"]) + " Y" + str(-opt["dst"]))

    def printGrid_hex(self):

        opt = self.settings # to shorten lines
        distance_ratio = 0.866025403784 # sqrt(3)/2
        dst_re = opt["dst"] * distance_ratio # reduced distance
        indent = dst_re/3.33333333

        self.m.send("G91")      # switch to relative coordinates
        if opt['pul']:
            self.m.send("G1 E" + str(opt["cor"]))
            opt['pul'] = False
        leftToRight = 1 # 1 if left to right, -1 if right to left
        cnt = 0
        for y in range(opt["row"]):
            indent *= -1
            for x in range(opt["col"]):
                # extrude high
                if opt["eh"]: self.m.send("G1 E" + str(opt["d"] + opt["d++"] * cnt))
                # lower head
                self.m.send("G1 Z" + str(-opt["h"]))
                # extrude low
                if not opt["eh"]: self.m.send("G1 E" + str(opt["d"] + opt["d++"] * cnt))
                # lift head
                self.m.send("G1 Z" + str(opt["h"]+opt["h++"]*cnt))
                # move over the next dot
                if x < (opt["col"]-1): self.m.send("G1 X" + str(leftToRight*opt["dst"]))
                # wait between dots
                time.sleep(opt["t"] + opt["t++"]*cnt)
                cnt += 1
            # move over the first dot in the next row
            if y<(opt["row"]-1):
                # if S route, move one row down and change direction
                if opt["s"]:
                    self.m.send("G1 Y" + str(-dst_re))
                    leftToRight *= -1
                # if terminal route, move back the whole length and move down
                else:
                    self.m.send("G1 X" + str(-(opt["col"]-1)*opt["dst"]-indent) + " Y" + str(-dst_re))

    def connect(self):
        self.socket=socket.socket()
        socketID = 14323
        while True:
            try:
                s.connect(('localhost', socketID))
                s.settimeout(1)
                print( "Connected to router at '" + str(socketID) + "'")
                s.send("ZX*" + MyID + "0000\n")
                break
            except:
                print( "Router not found at '" + str(socketID) + "', trying again...")
                time.sleep(5)
        time.sleep(1.5)

    def disconnect(self):
        self.socket.close()
        print("Disconnected from router.")

class Config:
    """Saves or loads the grid printing settings
     and the saved positions to / from a text file.
     Stores the filename only. For saving or loading
     it needs a printer as paramether, where the data
     is imported to / from."""
    def __init__(self, filename="cellprinter.cfg"):
        self.fn = filename

    def save(self, printer):
        #open(self.fn, 'w').close() # earse former contents
        cfg = open(self.fn, 'w')
        cfg.write("#Settings:\n")
        for k in printer.settings:
            cfg.write(k +
                    " " + str(printer.settings[k]) + " \n")
        cfg.write("@Positions:\n")
        for k in printer.positions:
            x, y, z = printer.positions[k].string_c()
            t = printer.positions[k].postype 
            cfg.write(k + " " + x + " " + y + " " + z + " " + t + " \n")
        cfg.close()

    def load(self, printer):
        cfg = open(self.fn, 'r')
        at_pos = False
        while True:
            try:
                line = cfg.readline()
                lineID = line[0]
            except IndexError:
                break
            if lineID == '#':
                at_pos = False
                continue
            elif lineID == '@':
                at_pos = True
                continue
            elif at_pos:
                w = line.split(" ")
                printer.positions[w[0]] = Position(int(w[1]), int(w[2]), int(w[3]), w[4])
            else:
                w = line.split(" ")
                if w[0] in ["row", "col"]:
                    w[1] = int(w[1])
                elif w[0] in ["eh", "s", "pul", "hex"]:
                    if w[1] == "True": w[1] = True
                    else: w[1] = False
                else:
                    w[1] = float(w[1])
                printer.settings[w[0]] = w[1]
        cfg.close()