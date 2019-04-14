# this is a plain window, actually for the cellprinter app
from tkinter import *

class Settings:
    def __init__(self):
        self.settings = {
            "dst":[20,  "distance between droplets"],
            "d":  [10.0,"size of droplets"],
            "h"  :[3.0, "head height while moving between droplets"],
            "row":[3,   "number of columns"],
            "col":[3,   "number of rows"],
            "h++":[0.0, "raise head slightly between every dot"],
            "t"  :[0.0, "waiting time between each drolpet"],
            "t++":[0.0, "extra waiting time"],
            "eh" :[1,   "extrude when head is lifted"],
            "s"  :[1,   "print grid in an S route"],
            "cor":[2.3, "amount of hysteresis correction"],
            "pul":[1,   "last extruder action"],
            "d++":[0.0, "make every next dot this bigger"]
            }

        self.names = ["dst", "d", "h"  , "row", 
            "col", "h++", "eh" , "s",
            "cor", "pul", "d++", "t"  , "t++"]
    
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

class Setting_list:
    def __init__(self, root_window, settings):
        self.labels = {}
        self.entries = {}
        self.names = settings.names
        for name in self.names:
            self.labels[name] = Label(root_window, text = settings.description(name), borderwidth=3)
            v = IntVar()
            v.set(settings.value(name = name))
            self.entries[name] = Entry(root_window, text = v, borderwidth=1)

    def make(self, align="W"):
        i = 0
        for name in self.names:
            self.entries[name].grid(row = i)
            self.labels[name].grid(row = i, sticky=W, column=1)
            i+= 1




def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def draw_dish():
    canvas.create_rectangle(canvas_x, canvas_x, border, border, fill=bg_col, outline="")
    canvas.create_circle(canvas_x/2+border, canvas_y/2+border, canvas_y/2, fill=wall_col, outline="")
    canvas.create_circle(canvas_x/2+border, canvas_y/2+border, canvas_y/2-dish_wall, fill=dish_col, outline="")

def draw_grid ():
    dots_in_row  = eval(prs.entries["row"].get())
    dots_in_col  = eval(prs.entries["col"].get())
    dot_distance = eval(prs.entries["dst"].get())
    dot_diameter = eval(prs.entries["d"].get())
    grow = eval(prs.entries["d++"].get())

    grid_width  = (dots_in_row-2)*dot_distance
    grid_heigth = (dots_in_col-2)*dot_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    draw_dish()
    for col in range(dots_in_col):
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0] + dot_distance*row,
                                starting_dot[1] + dot_distance*col,
                                dot_diameter/2 + ((row+col*dots_in_row)*grow), fill=drop_col, outline=drop_line)

def draw_hexgrid():
    distance_ratio = 0.866025403784 # sqrt(3)/2
    dots_in_row  = eval(prs.entries["row"].get())
    dots_in_col  = eval(prs.entries["col"].get())
    dot_distance = eval(prs.entries["dst"].get())
    reduced_distance = dot_distance * distance_ratio
    dot_diameter = eval(prs.entries["d"].get())
    grow = eval(prs.entries["d++"].get())

    grid_width  = (dots_in_row-2)*dot_distance
    grid_heigth = (dots_in_col-2)*reduced_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    draw_dish()
    indent = -1.0 * dot_distance/4.0
    for col in range(dots_in_col):
        indent *= -1
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0]+ indent + dot_distance*row,
                                starting_dot[1] + reduced_distance*col,
                                dot_diameter/2 + ((row+col*dots_in_row)*grow), fill=drop_col, outline=drop_line)

print_opt = Settings()
root = Tk()
main_label = Label(root, text='Welcome to hell',fg='red')
prs = Setting_list(root, print_opt)
prs.make()

bg_col = '#b7c6d8'
dish_col = '#e0e7ee'
wall_col = '#577892'
drop_col = '#915aa7' #light purple
#drop_col = '#412847' #dark purple
drop_line = ''
canvas_x = canvas_y = 400
border = 10
dish_wall = 10
canvas = Canvas(root, width=canvas_x, height=canvas_y, borderwidth=border, highlightthickness=0, bg=bg_col)
draw_dish()
draw_grid()
canvas.grid(row = 0, column=3, columnspan = 3, rowspan=len(prs.names))
yes_button = Button(root, text='Grid', command=draw_grid)
yes_button.grid(row = len(prs.names), column = 3, columnspan=2)
no_button = Button(root, text='Hexagonal grid', command=draw_hexgrid)
no_button.grid(row = len(prs.names), column = 4, columnspan=2)
root.mainloop()