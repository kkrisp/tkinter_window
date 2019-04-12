# this is a plain window, actually for the cellprinter app
from Tkinter import *

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

settings = {
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

setting_names = ["dst", "d", "h"  , "row", 
                "col", "h++", "eh" , "s",
                "cor", "pul", "d++", "t"  , "t++"]

def generate_field_list(my_window, fields):
    """'my_window' is a ktinker window,
    'fields' is the dictionary of the field names and values"""
    fn = {}
    f = {}
    for name in setting_names:
        fn[name] = Label(my_window, text = settings[name][1], borderwidth=3)
        v = IntVar()
        v.set(settings[name][0])
        f[name] = Entry(my_window, text = v, borderwidth=1)
    return fn, f

def draw_grid ():
    dots_in_row  = eval(my_fields["row"].get())
    dots_in_col  = eval(my_fields["col"].get())
    dot_distance = eval(my_fields["dst"].get())
    dot_diameter = eval(my_fields["d"].get())
    grow = eval(my_fields["d++"].get())

    grid_width  = (dots_in_row-2)*dot_distance
    grid_heigth = (dots_in_col-2)*dot_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    canvas.create_circle(canvas_x/2+10, canvas_y/2+10, canvas_y/2, fill="white", outline="")
    for col in range(dots_in_col):
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0] + dot_distance*row,
                                starting_dot[1] + dot_distance*col,
                                dot_diameter/2 + ((row+col*dots_in_row)*grow), fill="green", outline="")

def draw_hexgrid():
    distance_ratio = 0.866025403784 # sqrt(3)/2
    dots_in_row  = eval(my_fields["row"].get())
    dots_in_col  = eval(my_fields["col"].get())
    dot_distance = eval(my_fields["dst"].get())
    reduced_distance = dot_distance * distance_ratio
    dot_diameter = eval(my_fields["d"].get())
    grow = eval(my_fields["d++"].get())

    grid_width  = (dots_in_row-2)*dot_distance
    grid_heigth = (dots_in_col-2)*reduced_distance

    starting_dot = [canvas_x/2.0-grid_width/2.0, canvas_y/2.0-grid_heigth/2.0]
    
    canvas.create_circle(canvas_x/2+10, canvas_y/2+10, canvas_y/2, fill="white", outline="")
    indent = -1.0 * dot_distance/4.0
    for col in range(dots_in_col):
        indent *= -1
        for row in range(dots_in_row):
            canvas.create_circle(starting_dot[0]+ indent + dot_distance*row,
                                starting_dot[1] + reduced_distance*col,
                                dot_diameter/2 + ((row+col*dots_in_row)*grow), fill="green", outline="")

my_window = Tk()
main_label = Label(my_window, text='Welcome to hell',fg='red')
my_field_names, my_fields = generate_field_list(my_window, settings)
i = 0
for sn in setting_names:
    my_fields[sn].grid(row = i)
    my_field_names[sn].grid(row = i, sticky=W, column=1)
    i+= 1

canvas_x = canvas_y = 400

canvas = Canvas(my_window, width=canvas_x, height=canvas_y, borderwidth=10, highlightthickness=0, bg="blue")
#canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, sticky='NSEW')

canvas.create_circle(canvas_x/2+10, canvas_y/2+10, canvas_y/2, fill="white", outline="")
draw_grid()
canvas.grid(row = 0, column=3, columnspan = 3, rowspan=len(my_fields))
yes_button = Button(my_window, text='Grid', command=draw_grid)
yes_button.grid(row = len(my_fields), column = 3, columnspan=2)
no_button = Button(my_window, text='Hexagonal grid', command=draw_hexgrid)
no_button.grid(row = len(my_fields), column = 4, columnspan=2)
my_window.mainloop()