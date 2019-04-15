class Settings:
    def __init__(self):
        self.settings = {
            "dst":[2.5, "distance"],
            "d":  [1.0, "size"],
            "h"  :[3.0, "head height while moving"],
            "row":[3,   "columns"],
            "col":[3,   "rows"],
            "h++":[0.0, "change head height"],
            "t"  :[0.0, "wait time between droplets"],
            "t++":[0.0, "change waiting time"],
            "eh" :[1,   "extrude when head is lifted"],
            "s"  :[1,   "print grid in an S route"],
            "cor":[2.3, "correct hysteresys"],
            "pul":[1,   "last extruder action"],
            "d++":[0.0, "change size"],
            "hex":[False  , "hexagonal pattern"]
            }

        self.names = ["dst", "d", "h"  , "row", 
            "col", "h++", "eh" , "s",
            "cor", "pul", "d++", "t"  , "t++", "hex"]
    
    def value(self, name=None, index=None):
        if name:
            return self.settings[name][0]
        elif index:
            return self.settings[self.names[index]][0]
        else:
            return None

    def description(self, name=None, index=None):
        if name:
            return self.settings[name][1]
        elif index:
            return self.settings[self.names[index]][1]
        else:
            return None
    
    def set_value(self, val, name=None, index=None):
        if name:
            self.settings[name][0] = val
        elif index:
            self.settings[self.names[index]][0] = val

    def set_description(self, descr, name=None, index=None):
        if name:
            self.settings[name][1] = descr
        elif index:
            self.settings[self.names[index]][1] = descr