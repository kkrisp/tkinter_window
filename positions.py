from tkinter import *
from gcontrol import Position
from time import gmtime, strftime

# style ------------------------------- #
#bg_color = '#b7c6d8'
bg_color = '#f0f0f0' #gray
frame_color = '#d7dce0' #a bit darker blueish gray
dish_color = '#e0e7ee'
wall_color = '#577892'
drop_color = '#915aa7' #light purple
#drop_color = '#412847' #dark purple
drop_line = '' # no color

border = 10
dish_wall = 10
droplet_ratio = 10.0
label_size = 10
label_font = "Courier"
entry_size = 13
entry_font = "Courier"
#preview_size = root.winfo_screenheight()
dish_real_diameter = 35000 #um
ratio = 1.0/100.0
dish_size = dish_real_diameter*ratio
preview_size = dish_size+dish_wall+border


class Positionlist:
    def __init__(self, position_list=None):
        self.postypes = ["simple position", "petri dish centre", "material source", "ceiling"]
        self.pos = None
        self.types = {}
        if position_list:
            self.pos = position_list
            for k in self.pos:
                self.types[k] = "simple position"
        else:
            self.pos = {}

    def add(self, pos, name=None, postype="simple position"):
        if postype not in self.postypes:
            print("Invalid position type!")
            return
        if not name:
            name = "new_"
            name += strftime("%H_%M_%S", gmtime())
        self.pos[name] = pos
        self.types[name] = postype

    def delete(self, name):
        self.pos.pop(name, None)
        self.types.pop(name, None)



class Manager:
    def __init__(self, root, pos, row=0, col=0, rowspan=1, columnspan=1):
        self.pos_types = ["simple position", "petri dish centre", "material source", "ceiling"]
        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")
        
        subtitle_pos = Label(main_frame, text = "positions", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        subtitle_pos.grid(sticky="ew", row = 0, column=0, columnspan=2)

        pos_frame = Frame(main_frame, pady=5, padx=5, borderwidth=2, relief=GROOVE)
        pos_frame.grid(row=1,  column=0, sticky="nsew")

        action_frame = Frame(main_frame, pady=5, padx=5, borderwidth=2, relief=GROOVE)
        action_frame.grid(row=1,  column=1, sticky="nsew")

        labels = {}
        # generating list
        labels[ "name_title"] = Label(pos_frame, text = "name", font=(label_font, label_size))
        labels["coord_title"]= Label(pos_frame, text = "coordinates", font=(label_font, label_size))
        labels[ "type_title"] = Label(pos_frame, text = "type", font=(label_font, label_size))
        for k in pos.pos:
            labels[k + "_name"] = Label(pos_frame, text = k, font=(label_font, label_size))
            labels[k + "_coord"]= Label(pos_frame, text = pos.pos[k].getxyz(), font=(label_font, label_size))
            labels[k + "_type"] = Label(pos_frame, text = pos.types[k], font=(label_font, label_size))
        labels[ "name_title"].grid(row=0, column=0, sticky="w")
        labels["coord_title"].grid(row=0, column=1, sticky="w")
        labels[ "type_title"].grid(row=0, column=2, sticky="w")
        spacer = Frame(pos_frame, height=2, width=400, bg=wall_color)
        spacer.grid(row=1, columnspan=3, sticky="ew")
        i=2
        for k in pos.pos:
            labels[k + "_name" ].grid(row=i, column=0, sticky="w") 
            labels[k + "_coord"].grid(row=i, column=1, sticky="w")
            labels[k + "_type" ].grid(row=i, column=2, sticky="w")
            i+=1

class Save:
    def __init__(self, root, row=0, col=0):
        self.pos_types = ["simple position", "petri dish centre", "material source", "ceiling"]

        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")
        
        subtitle_pos = Label(main_frame, text = "positions", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        subtitle_pos.grid(sticky="ew", row = 0, column=0, columnspan=2)
        pos_frame = Frame(main_frame, pady=15, padx=15, borderwidth=2, relief=GROOVE)
        pos_frame.grid(row=1,  column=0, sticky="nsew")

        variable = StringVar(pos_frame)
        variable.set(self.pos_types[0]) # default value

        select_pos_type = OptionMenu(pos_frame, variable, *self.pos_types)
        select_pos_type["font"]=(label_font, label_size)
        select_pos_type["border"]=2

        pos_type_label = Label(pos_frame, text = "type:", font=(label_font, label_size))
        pos_name_label = Label(pos_frame, text = "name:", font=(label_font, label_size))
        pos_name_entry = Entry(pos_frame, text = "", font=(label_font, label_size), borderwidth=3, width=22)
        save_pos_btn = Button(pos_frame, text = "save position", font=(label_font), borderwidth=5)
        pos_name_label.grid(row=0, column=0, sticky="nw")
        pos_name_entry.grid(row=0, column=1, sticky="nw")
        pos_type_label.grid(row=1, column=0, sticky="w")
        select_pos_type.grid(row=1, column=1, sticky="nw") 
        save_pos_btn.grid(row=2, columnspan=2, sticky="w")
        
        