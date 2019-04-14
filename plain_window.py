# this is a plain window, actually for the cellprinter app
from tkinter import *
import math


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

class Petri_preview:
    def __init__(self, root_window, row=0, col=0):
        preview = Frame(root)
        preview.grid(row=row,  column=col)
        canvas = Canvas(preview, width=canvas_x, height=canvas_y, borderwidth=0, highlightthickness=0, bg=bg_color)
        canvas.create_rectangle(canvas_x, canvas_x, border, border, fill=bg_color, outline="")
        canvas.create_circle(canvas_x/2+border, canvas_y/2+border, canvas_y/2, fill=wall_color, outline="")
        canvas.create_circle(canvas_x/2+border, canvas_y/2+border, canvas_y/2-dish_wall, fill=dish_color, outline="")


class Setting_list:
    def __init__(self, root_window, settings):
        self.labels = {}
        self.entries = {}
        self.names = settings.names
        self.buttons = {}
        for name in self.names:
            self.labels[name] = Label(root_window, text = settings.description(name), borderwidth=3, font=(label_font, label_size))
            v = IntVar()
            v.set(settings.value(name = name))
            self.entries[name] = Entry(root_window, text = v, borderwidth=1, width=6, justify=CENTER, font=(entry_font, entry_size))

    def plus_int(self, name):
        x = eval(prs.entries[name].get())
        x += 1
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        if is_hexgrid[0]:
            draw_hexgrid()
        else:
            draw_grid()

    def minus_int(self, name):
        x = eval(prs.entries[name].get())
        if x > 1:
            x -= 1
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        if is_hexgrid[0]:
            draw_hexgrid()
        else:
            draw_grid()

    def plus(self, name):
        x = eval(prs.entries[name].get())
        x = math.ceil(x*10)
        x += 1
        x /= 10
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        if is_hexgrid[0]:
            draw_hexgrid()
        else:
            draw_grid()

    def minus(self, name):
        x = eval(prs.entries[name].get())
        x = math.floor(x*10)
        if x > 0:
            x -= 1
        x /= 10
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        if is_hexgrid[0]:
            draw_hexgrid()
        else:
            draw_grid()

    def minus_alloweg(self, name):
        x = eval(prs.entries[name].get())
        x -= 0.1
        x = math.ceil(x*10)/10
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        if is_hexgrid[0]:
            draw_hexgrid()
        else:
            draw_grid()
    def refresh(self):
        if is_hexgrid[0]:
            is_hexgrid[0] = False
            draw_grid()
        else:
            is_hexgrid[0] = True
            draw_hexgrid()
    def make(self, name):
        i = 0
        for name in self.names:
            self.entries[name].grid(row = i)
            self.labels[name].grid(row = i, sticky=W, column=1)
            i+= 1

    def make_with_buttons(self):
        for name in ["h++", "eh" , "s", "cor", "pul", "d++", "t", "t++"]:            
            self.buttons[name] = Checkbutton(root, text = print_opt.description(name), font=("Courier", 10))
            #self.buttons[name+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus(name))
            #self.buttons[name+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus(name))
        self.buttons["hex"] = Checkbutton(root, text = print_opt.description("hex"), font=("Courier", 10), command=self.refresh)

        self.buttons["dst"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus("dst"))
        self.buttons["dst"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus("dst"))
        
        self.buttons["d"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus("d"))
        self.buttons["d"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus("d"))
        
        self.buttons["row"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus_int("row"))
        self.buttons["row"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus_int("row"))
        
        self.buttons["col"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus_int("col"))
        self.buttons["col"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus_int("col"))
        
        self.buttons["d++"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus("d++"))
        self.buttons["d++"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus("d++"))
        
        self.buttons["h"+"_left"] = Button(root, image=l_a_p, command=lambda: self.minus("h"))
        self.buttons["h"+"_right"] = Button(root, image=r_a_p, command=lambda: self.plus("h"))

        # options with values
        i=1   
        for name in ["row", "col", "dst", "d"]:#, "h++", "d++", "t"  , "t++"]:
            self.buttons[name+"_left"].grid( row = i, column=0)
            self.entries[name].grid(         row = i, column=1)
            self.buttons[name+"_right"].grid(row = i, column=2)
            self.labels[name].grid(sticky=W, row = i, column=3)
            i+=1

        # yes or no options
        for name in ["eh" , "s", "hex"]:
            self.buttons[name].grid(sticky=W, row = i, column=0, columnspan=4)
            i+=1
        
        # double options
        

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def draw_dish():
    radius = (canvas_x-border)/2
    canvas.create_rectangle(canvas_x, canvas_y, 0, 0, fill=bg_color, outline="")
    canvas.create_circle(canvas_x/2, canvas_y/2, radius, fill=wall_color, outline="")
    canvas.create_circle(canvas_x/2, canvas_y/2, radius-dish_wall, fill=dish_color, outline="")

def draw_grid():
    is_hexgrid[0] = False
    dots_in_row  = eval(prs.entries["row"].get())
    dots_in_col  = eval(prs.entries["col"].get())
    dot_distance = eval(prs.entries["dst"].get())*droplet_ratio
    dot_diameter = eval(prs.entries["d"].get())
    grow = eval(prs.entries["d++"].get())

    grid_width  = (dots_in_row-1)*dot_distance
    grid_heigth = (dots_in_col-1)*dot_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    draw_dish()
    for col in range(dots_in_col):
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0] + dot_distance*row,
                                starting_dot[1] + dot_distance*col,
                                dot_diameter/2*droplet_ratio + ((row+col*dots_in_row)*grow), fill=drop_color, outline=drop_line)

def draw_hexgrid():
    is_hexgrid[0] = True
    distance_ratio = 0.866025403784 # sqrt(3)/2
    dots_in_row  = eval(prs.entries["row"].get())
    dots_in_col  = eval(prs.entries["col"].get())
    dot_distance = eval(prs.entries["dst"].get())*droplet_ratio
    reduced_distance = dot_distance * distance_ratio
    dot_diameter = eval(prs.entries["d"].get())
    grow = eval(prs.entries["d++"].get())

    grid_width  = (dots_in_row-1)*dot_distance
    grid_heigth = (dots_in_col-1)*reduced_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    draw_dish()
    indent = -1.0 * dot_distance/4.0
    for col in range(dots_in_col):
        indent *= -1
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0]+ indent + dot_distance*row,
                                starting_dot[1] + reduced_distance*col,
                                dot_diameter/2*droplet_ratio + ((row+col*dots_in_row)*grow), fill=drop_color, outline=drop_line)
    return True

# style ------------------------------- #
#bg_color = '#b7c6d8'
bg_color = '#f0f0f0' #gray
dish_color = '#e0e7ee'
wall_color = '#577892'
drop_color = '#915aa7' #light purple
#drop_color = '#412847' #dark purple
drop_line = '' # no color
canvas_x = canvas_y = 400
border = 10
dish_wall = 10
droplet_ratio = 10
label_size = 10
label_font = "Courier"
entry_size = 13
entry_font = "Courier"

is_hexgrid = [False]
print_opt = Settings()
root = Tk()
root.title("Cellprinter GUI")
r_a_p = PhotoImage(file = "rightarrow.png")
l_a_p = PhotoImage(file = "leftarrow.png")
pb_pic = PhotoImage(file = "button_print.png")
main_label = Label(root, text='Welcome to hell',fg='red')
prs = Setting_list(root, print_opt)
prs.make_with_buttons()

canvas = Canvas(root, width=canvas_x, height=canvas_y, borderwidth=0, highlightthickness=0, bg=bg_color)
draw_dish()
draw_grid()
canvas.grid(row = 0, column=6, columnspan = 3, rowspan=len(prs.names))
button_print = Button(root, image=pb_pic, command=lambda: print("printing..."))
button_print.grid(row = len(prs.names), column=0, columnspan = 4)
root.mainloop()