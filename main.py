# this is a plain window, actually for the cellprinter app
from tkinter import *
import math

# style ------------------------------- #
#bg_color = '#b7c6d8'
bg_color = '#f0f0f0' #gray
dish_color = '#e0e7ee'
wall_color = '#577892'
drop_color = '#915aa7' #light purple
#drop_color = '#412847' #dark purple
drop_line = '' # no color

preview_size = 400
border = 10
dish_size = preview_size-border
dish_wall = 10
droplet_ratio = 100
label_size = 10
label_font = "Courier"
entry_size = 13
entry_font = "Courier"


class Petri_preview:
    def __init__(self, root, row=0, col=0):
        prev_frame = Frame(root)
        prev_frame.grid(row=row,  column=col)
        self.prev_area = Canvas(prev_frame, width=preview_size, height=preview_size, borderwidth=0, highlightthickness=0, bg=bg_color)
        self.prev_area.grid(row = 0, column=0)
        self.clear()
    
    def clear(self):
        self.prev_area.create_rectangle(preview_size, preview_size, border, border, fill=bg_color, outline="")
        self.prev_area.create_oval(border, # petri dish wall
                              border,
                              dish_size,
                              dish_size,
                              fill=wall_color,
                              outline='')
        self.prev_area.create_oval(border+dish_wall, # petri dish area
                              border+dish_wall,
                              dish_size-dish_wall,
                              dish_size-dish_wall,
                              fill=dish_color,
                              outline='')

    def droplets(self, row=3, col=3, drop_size=0.1, distance=0.2, growth=0.0):
        self.clear()
        dst = distance*droplet_ratio
        dia = drop_size*droplet_ratio
        height = distance*(row-1)*droplet_ratio
        width =  distance*(col-1)*droplet_ratio
        offset_x = (dish_size-width)/2
        offset_y = (dish_size-height)/2
        for i in range(col):
            for j in range(row):
                self.prev_area.create_oval(offset_x + j*dst,
                              offset_y + i*dst,
                              offset_x + j*dst+dia+growth*(j+row*i),
                              offset_y + i*dst+dia+growth*(j+row*i),
                              fill=drop_color,
                              outline='')

class Settings:
    def __init__(self):
        self.settings = {
            "dst":[2.0,  "distance"],
            "d":  [1.0,"size"],
            "h"  :[3.0, "head height while moving between droplets"],
            "row":[3,   "columns"],
            "col":[3,   "rows"],
            "h++":[0.0, "raise head slightly between every dot"],
            "t"  :[0.0, "waiting time between each drolpet"],
            "t++":[0.0, "extra waiting time"],
            "eh" :[1,   "extrude when head is lifted"],
            "s"  :[1,   "print grid in an S route"],
            "cor":[2.3, "amount of hysteresis correction"],
            "pul":[1,   "last extruder action"],
            "d++":[0.0, "make every next dot this bigger"],
            "hex":[0.0, "hexagonal pattern"]
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

class Printsettings:
    def __init__(self, root, row=0, col=0, settings):
        frame = Frame(root)
        frame.grid(row=row,  column=col)
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        
        self.buttons["dst"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus("dst"))
        self.buttons["dst"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus("dst"))
        # options with value
        for name in ["row", "col", "dst", "d"]:#, "h++", "d++", "t"  , "t++"]:
            self.buttons[name+"_left"].grid( row = i, column=0)
            self.entries[name].grid(         row = i, column=1)
            self.buttons[name+"_right"].grid(row = i, column=2)
            self.labels[name].grid(sticky=W, row = i, column=3)
            i+=1
        for name in self.names:
            self.labels[name] = Label(root_window, text = settings.description(name), borderwidth=3, font=(label_font, label_size))
            v = IntVar()
            v.set(settings.value(name = name))
            self.entries[name] = Entry(root_window, text = v, borderwidth=1, width=6, justify=CENTER, font=(entry_font, entry_size))

root = Tk()
root.title("Cellprinter GUI")
pprev = Petri_preview(root)
#pprev.droplets()

root.mainloop()