from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import PhotoImage

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

class Movements:
    def __init__(self, root, row=0, col=0):
        self.button_pics = []
        self.base = 3
        for d in ['up', 'down', 'left', 'right']:
            self.button_pics.append(PhotoImage(file = "move_" + d + ".png"))
            self.button_pics.append(PhotoImage(file = "move10_" + d + ".png"))

        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")

        xy_frame = Frame(main_frame, pady=15, padx=15)
        xy_frame.grid(row=2,  column=0, sticky="nsew", columnspan=2)
        z_frame = Frame(main_frame, pady=15, padx=15)
        z_frame.grid(row=4,  column=0, sticky="nsew")
        ex_frame = Frame(main_frame, pady=15, padx=15)
        ex_frame.grid(row=4,  column=1, sticky="nsew")

        #spacer = Frame(main_frame, bg=bg_color, height=20, width=300)
        #spacer.grid(row=1, column=0, columnspan=3)

        self.subtitle_xy = Label(main_frame, text = "Move head", borderwidth=5, font=(label_font, label_size+3))
        self.subtitle_xy.grid(sticky="w", row = 0, column=0)
        self.subtitle_z = Label(main_frame, text = "Move table", borderwidth=5, font=(label_font, label_size+3))
        self.subtitle_z.grid(sticky="w", row = 3, column=0)
        self.subtitle_ex = Label(main_frame, text = "Move extruder", borderwidth=5, font=(label_font, label_size+3))
        self.subtitle_ex.grid(sticky="w", row = 3, column=1)

        self.labels = {}
        self.entries = {}
        self.buttons = {}

        self.buttons[   "up"] = Button(xy_frame, image=self.button_pics[0],   command=lambda: self.move_head("up",    self.base))
        self.buttons[ "down"] = Button(xy_frame, image=self.button_pics[2],   command=lambda: self.move_head("down",  self.base))
        self.buttons[ "left"] = Button(xy_frame, image=self.button_pics[4],   command=lambda: self.move_head("left",  self.base))
        self.buttons["right"] = Button(xy_frame, image=self.button_pics[6],   command=lambda: self.move_head("right", self.base))
        self.buttons[   "up10"] = Button(xy_frame, image=self.button_pics[1], command=lambda: self.move_head("up",    self.base*10))
        self.buttons[ "down10"] = Button(xy_frame, image=self.button_pics[3], command=lambda: self.move_head("down",  self.base*10))
        self.buttons[ "left10"] = Button(xy_frame, image=self.button_pics[5], command=lambda: self.move_head("left",  self.base*10))
        self.buttons["right10"] = Button(xy_frame, image=self.button_pics[7], command=lambda: self.move_head("right", self.base*10))

        self.buttons["table_up"] =    Button(z_frame, image=self.button_pics[0], command=lambda: self.move_head("table_up",    self.base))
        self.buttons["table_down"]  = Button(z_frame, image=self.button_pics[2], command=lambda: self.move_head("table_down",  self.base))
        self.buttons["table_up10"]  = Button(z_frame, image=self.button_pics[1], command=lambda: self.move_head("table_up",    self.base*10))
        self.buttons["table_down10"]= Button(z_frame, image=self.button_pics[3], command=lambda: self.move_head("table_down",  self.base*10))

        self.buttons["ex_up"] =     Button(ex_frame, image=self.button_pics[0], command=lambda: self.move_head(  "ex_up",    self.base))
        self.buttons["ex_down"] =   Button(ex_frame, image=self.button_pics[2], command=lambda: self.move_head("ex_down",  self.base))
        self.buttons["ex_up10"] =   Button(ex_frame, image=self.button_pics[1], command=lambda: self.move_head(  "ex_up",    self.base*10))
        self.buttons["ex_down10"] = Button(ex_frame, image=self.button_pics[3], command=lambda: self.move_head("ex_down",  self.base*10))

        self.buttons[   "up"  ].grid(row=1, column=2)
        self.buttons[ "down"  ].grid(row=2, column=2)
        self.buttons[ "left"  ].grid(row=1, column=1, rowspan=2)
        self.buttons["right"  ].grid(row=1, column=3, rowspan=2)
        self.buttons[   "up10"].grid(row=0, column=2)
        self.buttons[ "down10"].grid(row=3, column=2)
        self.buttons[ "left10"].grid(row=1, column=0, rowspan=2)
        self.buttons["right10"].grid(row=1, column=4, rowspan=2)
        
        self.buttons["table_up"].grid(row=1, column=0)
        self.buttons["table_down"].grid(row=2, column=0)
        self.buttons["table_up10"].grid(row=0, column=0)
        self.buttons["table_down10"].grid(row=3, column=0)
        self.buttons["ex_up"].grid(row=1, column=0)
        self.buttons["ex_down"].grid(row=2, column=0)
        self.buttons["ex_up10"].grid(row=0, column=0)
        self.buttons["ex_down10"].grid(row=3, column=0)

    def move_head(self, direction, length):
        print("moving {}, {}".format(direction, length))


class Camera_preview:
    def __init__(self, root, row=0, col=0):
        self.button_pics = []
        self.base = 3
        for d in ['up', 'down', 'left', 'right']:
            self.button_pics.append(PhotoImage(file = "move_" + d + ".png"))
            self.button_pics.append(PhotoImage(file = "move10_" + d + ".png"))

        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")

        buttons_frame = Frame(main_frame, pady=15, padx=15)
        buttons_frame.grid(row=0,  column=0, sticky="nsew")
        camera_frame = Frame(main_frame, pady=15, padx=15, width=600, height=600, bg="blue")
        camera_frame.grid(row=0,  column=1, sticky="nsew")

        self.labels = {}
        self.entries = {}
        self.buttons = {}

        self.buttons["zoom_in"] = Button(buttons_frame, text = "zoom in")
        self.buttons["zoom_out"] = Button(buttons_frame, text = "zoom out")
        self.buttons["snap"] = Button(buttons_frame, text = "snap")
        self.buttons["rec"] = Button(buttons_frame, text = "start recording")

        self.buttons["zoom_in"].grid(row=0 , sticky="ew")
        self.buttons["zoom_out"].grid(row=1, sticky="ew")
        self.buttons["snap"].grid(row=2    , sticky="ew")
        self.buttons["rec"].grid(row=3     , sticky="ew")

