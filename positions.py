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
        self.default_petri = None
        self.default_source = None
        self.default_ceiling = None
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
    
    def set_default(self, name):
        for this_name in self.pos.keys():
            if this_name == name:
                if self.types[this_name] == "petri dish centre":
                    self.default_petri = this_name
                elif self.types[this_name] == "material source":
                    self.default_source = this_name
                elif self.types[this_name] == "ceiling":
                    self.default_ceiling = this_name


class Highlightline:
    def __init__(self, root, text, action, positions, labels, value=None):
        self.labels = labels
        self.pos = positions
        self.value_to_change = value
        self.action = action
        self.label = Label(root, bg="white", height=1, text = text, font=(label_font, label_size))
        self.label.bind("<Button-1>", self.select)

    def select(self, name):
        for k in self.pos.pos:
            self.labels[k + "_name" ].label.config(bg="white")
            self.labels[k + "_coord" ].config(bg="white")
            self.labels[k + "_type" ].config(bg="white")
        self.value_to_change[0] = self.action
        self.labels[self.action + "_name" ].label.config(bg=frame_color)
        self.labels[self.action + "_coord" ].config(bg=frame_color)
        self.labels[self.action + "_type" ].config(bg=frame_color)


class Manager:
    def __init__(self, root, pos, row=0, col=0, rowspan=1, columnspan=1):
        self.current_position = [None]
        self.pos = pos
        self.pos_types = ["simple position", "petri dish centre", "material source", "ceiling"]
        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")
        
        subtitle_pos = Label(main_frame, text = "positions", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        subtitle_pos.grid(sticky="ew", row = 0, column=0, columnspan=2)

        self.pos_frame = Frame(main_frame, pady=5, padx=5, borderwidth=2, bg="white", relief=GROOVE)
        self.pos_frame.grid(row=1,  column=0, sticky="nsew")

        self.action_frame = Frame(main_frame, pady=5, padx=5, borderwidth=2, relief=GROOVE)
        self.action_frame.grid(row=1,  column=1, sticky="nsew")

        self.labels = {}
        
        self.set_def_btn = Button(self.action_frame, text = "set default", font=(label_font), command=self.set_default)
        self.refresh_btn = Button(self.action_frame, text = "srefresh", font=(label_font), command=self.draw)
        self.delete_btn = Button(self.action_frame, text = "delete", font=(label_font), command=self.delete)
        self.go_btn = Button(self.action_frame, text = "go", font=(label_font), command=self.go)

        self.set_def_btn.grid()
        self.refresh_btn.grid() 

        # generating list
        self.labels[ "name_title"] = Label(self.pos_frame, bg="white", text = "name", font=(label_font, label_size))
        self.labels["coord_title"]= Label(self.pos_frame,  bg="white", text = "coordinates", font=(label_font, label_size))
        self.labels[ "type_title"] = Label(self.pos_frame, bg="white", text = "type", font=(label_font, label_size))
        for k in pos.pos:
            self.labels[k + "_name"] = Highlightline(self.pos_frame, k, k, pos, self.labels, value=self.current_position)
            self.labels[k + "_coord"]= Label(self.pos_frame, bg="white", height=1, text = pos.pos[k].getxyz(), font=(label_font, label_size))
            self.labels[k + "_type"] = Label(self.pos_frame, bg="white", height=1, text = pos.types[k], font=(label_font, label_size))
        
        self.spacer2 = Frame(self.pos_frame, width=400, bg=wall_color)
        self.def_label = Label(self.pos_frame, bg="white", text = "used by printing", font=(label_font, label_size))
        self.spacer3 = Frame(self.pos_frame, width=400, bg=wall_color)
        
        self.draw()
        
    def draw(self):
        self.pos_frame.grid_forget()
        self.pos_frame.grid(row=1,  column=0, sticky="nsew")
        self.labels[ "name_title"].grid(row=0, column=0, sticky="ew")
        self.labels["coord_title"].grid(row=0, column=1, sticky="ew")
        self.labels[ "type_title"].grid(row=0, column=2, sticky="ew")
        spacer = Frame(self.pos_frame, height=2, width=400, bg=wall_color)
        spacer.grid(row=1, columnspan=3, sticky="ew")
        i=2
        for k in self.pos.pos:
            self.labels[k + "_name" ].label.grid(row=i, column=0, sticky="ew") 
            self.labels[k + "_coord"].grid(row=i, column=1, sticky="ew")
            self.labels[k + "_type" ].grid(row=i, column=2, sticky="ew")
            i+=1
        self.spacer2.grid(row=i, column=0, columnspan=3, sticky="ew")
        i+=1
        self.def_label.grid(row=i, column=0, columnspan=3, sticky="ew")
        i+=1
        self.spacer3.grid(row=i, column=0, columnspan=3, sticky="ew")
        if self.pos.default_petri:
            i+=1
            self.labels[self.pos.default_petri + "_name" ].label.grid(row=i, column=0, sticky="ew") 
            self.labels[self.pos.default_petri + "_coord"].grid(row=i, column=1, sticky="ew")
            self.labels[self.pos.default_petri + "_type" ].grid(row=i, column=2, sticky="ew")
        if self.pos.default_ceiling:
            i+=1
            self.labels[self.pos.default_ceiling + "_name" ].label.grid(row=i, column=0, sticky="ew") 
            self.labels[self.pos.default_ceiling + "_coord"].grid(row=i, column=1, sticky="ew")
            self.labels[self.pos.default_ceiling + "_type" ].grid(row=i, column=2, sticky="ew")
        if self.pos.default_source:
            i+=1
            self.labels[self.pos.default_source + "_name" ].label.grid(row=i, column=0, sticky="ew") 
            self.labels[self.pos.default_source + "_coord"].grid(row=i, column=1, sticky="ew")
            self.labels[self.pos.default_source + "_type" ].grid(row=i, column=2, sticky="ew")
    
    def refresh(self, name):
        for k in self.pos.pos:
            self.labels[k + "_name"] = Highlightline(self.pos_frame, k, k, self.pos, self.labels, value=self.current_position)
            self.labels[k + "_coord"]= Label(self.pos_frame, bg="white", height=1, text = self.pos.pos[k].getxyz(), font=(label_font, label_size))
            self.labels[k + "_type"] = Label(self.pos_frame, bg="white", height=1, text = self.pos.types[k], font=(label_font, label_size))
        self.draw()

    def delete(self):
        self.pos.delete(self.current_position[0])
        self.draw()
    def set_default(self):
        self.pos.set_default(self.current_position[0])
        self.draw()
    def go(self):
        print("go")


class Save:
    def __init__(self, root, pos, posman, row=0, col=0):
        self.posman=posman
        pos_types = ["simple position", "petri dish centre", "material source", "ceiling"]
        self.pos = pos
        self.currenttype = pos_types[0]

        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")
        
        subtitle_pos = Label(main_frame, text = "positions", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        subtitle_pos.grid(sticky="ew", row = 0, column=0, columnspan=2)
        pos_frame = Frame(main_frame, pady=15, padx=15, borderwidth=2, relief=GROOVE)
        pos_frame.grid(row=1,  column=0, sticky="nsew")
        
        self.pos_type_label = Label(pos_frame, text = "type:", font=(label_font, label_size))
        self.variable = StringVar(pos_frame)
        self.variable.set(pos_types[0])
        self.select_pos_type = OptionMenu(pos_frame, self.variable, *pos_types, command=self.func)
        self.select_pos_type["font"]=(label_font, label_size)
        self.select_pos_type["border"]=2
        
        self.pos_name_label = Label(pos_frame, text = "name:", font=(label_font, label_size))
        self.pos_entry_value = StringVar()
        self.pos_entry_value.set("new")
        self.pos_name_entry = Entry(pos_frame, text = self.pos_entry_value, font=(label_font, label_size), borderwidth=3, width=22)

        self.save_pos_btn = Button(pos_frame, text = "save position", font=(label_font), borderwidth=5, command=self.save_pos)
        self.pos_name_label.grid(row=0, column=0, sticky="nw")
        self.pos_name_entry.grid(row=0, column=1, sticky="nw")
        self.pos_type_label.grid(row=1, column=0, sticky="w")
        self.select_pos_type.grid(row=1, column=1, sticky="nw") 
        self.save_pos_btn.grid(row=2, columnspan=2, sticky="w")

    def save_pos(self):
        pname = self.pos_name_entry.get()
        self.pos.add(Position(20, 21, 11), name=pname, postype=self.currenttype)
        self.posman.labels[pname + "_name"] = Highlightline(self.posman.pos_frame, pname, pname, self.pos, self.posman.labels, value=self.posman.current_position)
        self.posman.labels[pname + "_coord"]= Label(self.posman.pos_frame, bg="white", height=1, text = self.pos.pos[pname].getxyz(), font=(label_font, label_size))
        self.posman.labels[pname + "_type"] = Label(self.posman.pos_frame, bg="white", height=1, text = self.pos.types[pname], font=(label_font, label_size))
        self.posman.draw()

    def func(self, value):
        self.currenttype = value