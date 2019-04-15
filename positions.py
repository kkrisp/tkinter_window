from tkinter import *

# style ------------------------------- #
#bg_color = '#b7c6d8'
bg_color = '#f0f0f0' #gray
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

class Positions:
    def __init__(self):
        self.pos = {}
        self.pos["dish_centre"] = [111, 23, 14]
        self.pos["origo"] = [0, 0, 0]
        self.pos["ceiling"] = [51, 62, 0]

class Position_list:
    def __init__(self, root, pos, row=0, col=0):
        self.x_y = pos
        for p in self.x_y.pos:
            print("x: {}, y:{}, z:{}".format(self.x_y.pos[p][0], self.x_y.pos[p][1],self.x_y.pos[p][2]))

        main_frame = Frame(root, pady=15, padx=15, bg="blue")
        main_frame.grid(row=row,  column=col, sticky="nsew")
