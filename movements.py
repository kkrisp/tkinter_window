from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import PhotoImage
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Checkbutton
from tkinter import OptionMenu
from tkinter import GROOVE
import math

# style ------------------------------- #
#bg_color = '#b7c6d8'
bg_color = '#f0f0f0' #gray
frame_color = '#d7dce0' #a bit darker blueish gray
title_bg_color = '#a1a9c6'
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
    def __init__(self, root, row=0, col=0, rwsp=1):
        self.button_pics = []
        self.base = 3
        for i in range(12):
            self.button_pics.append(PhotoImage(file = "gl"+ str(i*5+2000) +".png"))

        self.button_pics.append(PhotoImage(file = "plus.png"))
        self.button_pics.append(PhotoImage(file = "minus.png"))
        self.xy_label_pic = PhotoImage(file = "xy_label.png")
        self.z_label1_pic = PhotoImage(file = "z_raise.png")
        self.z_label2_pic = PhotoImage(file = "z_lower.png")
        self.ex_label1_pic = PhotoImage(file = "ex_push.png")
        self.ex_label2_pic = PhotoImage(file = "ex_pull.png")

        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, rowspan=rwsp, sticky="nsew")

        xy_frame = Frame(main_frame, pady=15, padx=5, borderwidth=2, relief=GROOVE)
        z_frame = Frame(main_frame, pady=15, padx=5, borderwidth=2, relief=GROOVE)
        ex_frame = Frame(main_frame, pady=15, padx=5, borderwidth=2, relief=GROOVE)

        self.subtitle_xy = Label(main_frame, text = "head", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        self.subtitle_z = Label(main_frame, text = "table", bg=frame_color, borderwidth=2, relief=GROOVE, font=(label_font, label_size+3))
        self.subtitle_ex = Label(main_frame, text = "extruder", bg=frame_color, borderwidth=2, relief=GROOVE, font=(label_font, label_size+3))
        
        xy_frame.grid(row=1,  column=0, sticky="nsew")
        z_frame.grid(row=1,  column=1, sticky="nsew")
        ex_frame.grid(row=1,  column=2, sticky="nsew")
        self.subtitle_xy.grid(sticky="ew", row = 0, column=0)
        self.subtitle_z.grid(sticky="ew", row = 0, column=1)
        self.subtitle_ex.grid(sticky="ew", row = 0, column=2)

        self.entries = {}
        self.buttons = {}

        self.xy_entry_value = IntVar()
        self.xy_entry_value.set(1)
        z_entry_value = IntVar()
        z_entry_value.set(1)
        ex_entry_value = IntVar()
        ex_entry_value.set(1)

        self.entries["xy"] = Entry(xy_frame, text =self.xy_entry_value, borderwidth=1, width=6, justify="center", font=(entry_font, entry_size))
        self.buttons["up01"] = Button(xy_frame, image=self.button_pics[0], command=lambda: self.move_head("up", 0.1))
        self.buttons["up"  ] = Button(xy_frame, image=self.button_pics[1], command=lambda: self.move_head("up", 1))
        self.buttons["up10"] = Button(xy_frame, image=self.button_pics[2], command=lambda: self.move_head("up", 10))
        self.buttons["down01"] = Button(xy_frame, image=self.button_pics[3], command=lambda: self.move_head("down", 0.1))
        self.buttons["down"  ] = Button(xy_frame, image=self.button_pics[4], command=lambda: self.move_head("down", 1))
        self.buttons["down10"] = Button(xy_frame, image=self.button_pics[5], command=lambda: self.move_head("down", 10))
        self.buttons["left01"] = Button(xy_frame, image=self.button_pics[6], command=lambda: self.move_head("left", 0.1))
        self.buttons["left"  ] = Button(xy_frame, image=self.button_pics[7], command=lambda: self.move_head("left", 1))
        self.buttons["left10"] = Button(xy_frame, image=self.button_pics[8], command=lambda: self.move_head("left", 10))
        self.buttons["right01"] = Button(xy_frame, image=self.button_pics[9], command=lambda: self.move_head("right", 0.1))
        self.buttons["right"  ] = Button(xy_frame, image=self.button_pics[10], command=lambda: self.move_head("right", 1))
        self.buttons["right10"] = Button(xy_frame, image=self.button_pics[11], command=lambda: self.move_head("right", 10))
        self.buttons["xy_plus" ] = Button(xy_frame, image=self.button_pics[12], command=lambda: self.add("xy", 1))
        self.buttons["xy_minus"] = Button(xy_frame, image=self.button_pics[13], command=lambda: self.add("xy", -1))
        self.xy_label = Label(xy_frame, image=self.xy_label_pic)

        self.entries["table"] = Entry(z_frame, text = z_entry_value, borderwidth=1, width=6, justify="center", font=(entry_font, entry_size))
        self.buttons["table_up01"] = Button(z_frame, image=self.button_pics[0], command=lambda: self.move_table("table_up", 0.1))
        self.buttons["table_up"  ] = Button(z_frame, image=self.button_pics[1], command=lambda: self.move_table("table_up", 1))
        self.buttons["table_up10"] = Button(z_frame, image=self.button_pics[2], command=lambda: self.move_table("table_up", 10))
        self.buttons["table_down01"] = Button(z_frame, image=self.button_pics[3], command=lambda: self.move_table("table_down", 0.1))
        self.buttons["table_down"  ] = Button(z_frame, image=self.button_pics[4], command=lambda: self.move_table("table_down", 1))
        self.buttons["table_down10"] = Button(z_frame, image=self.button_pics[5], command=lambda: self.move_table("table_down", 10))
        self.buttons["table_plus"  ] = Button(z_frame, image=self.button_pics[12], command=lambda: self.add("table", 1))
        self.buttons["table_minus"] = Button(z_frame, image=self.button_pics[13], command=lambda: self.add("table", -1))
        self.z_label1 = Label(z_frame, image=self.z_label1_pic)
        self.z_label2 = Label(z_frame, image=self.z_label2_pic)

        self.entries["ex"] = Entry(ex_frame, text = ex_entry_value, borderwidth=1, width=6, justify="center", font=(entry_font, entry_size))
        self.buttons["ex_up01"] = Button(ex_frame, image=self.button_pics[0], command=lambda: self.move_extruder("ex_up", 0.1))
        self.buttons["ex_up"  ] = Button(ex_frame, image=self.button_pics[1], command=lambda: self.move_extruder("ex_up", 1))
        self.buttons["ex_up10"] = Button(ex_frame, image=self.button_pics[2], command=lambda: self.move_extruder("ex_up", 10))
        self.buttons["ex_down01"] = Button(ex_frame, image=self.button_pics[4], command=lambda: self.move_extruder("ex_down", 0.1))
        self.buttons["ex_down"  ] = Button(ex_frame, image=self.button_pics[3], command=lambda: self.move_extruder("ex_down", 1))
        self.buttons["ex_down10"] = Button(ex_frame, image=self.button_pics[5], command=lambda: self.move_extruder("ex_down", 10))
        self.buttons["ex_plus"  ] = Button(ex_frame, image=self.button_pics[12], command=lambda: self.add("ex", 1))
        self.buttons["ex_minus"] = Button(ex_frame, image=self.button_pics[13], command=lambda: self.add("ex", -1))
        self.ex_label1 = Label(ex_frame, image=self.ex_label1_pic)
        self.ex_label2 = Label(ex_frame, image=self.ex_label2_pic)

        self.xy_label.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.buttons["up01"   ].grid(row=2, column=3)
        self.buttons["up"     ].grid(row=1, column=3)
        self.buttons["up10"   ].grid(row=0, column=3)
        self.buttons["down01" ].grid(row=4, column=3)
        self.buttons["down"   ].grid(row=5, column=3)
        self.buttons["down10" ].grid(row=6, column=3)
        self.buttons["left01" ].grid(row=3, column=2, rowspan=1)
        self.buttons["left"   ].grid(row=3, column=1, rowspan=1)
        self.buttons["left10" ].grid(row=3, column=0, rowspan=1)
        self.buttons["right01"].grid(row=3, column=4, rowspan=1)
        self.buttons["right"  ].grid(row=3, column=5, rowspan=1)
        self.buttons["right10"].grid(row=3, column=6, rowspan=1)
        self.buttons["xy_minus"].grid(row=2, column=2)
        self.buttons["xy_plus"].grid(row=2, column=4)
        self.entries["xy"].grid(row=3, column=3)
        
        self.z_label1.grid(row=0, column=0, rowspan=2)
        self.z_label2.grid(row=5, column=0, rowspan=2)
        self.buttons["table_up01"].grid(row=2, column=1)
        self.buttons["table_up"  ].grid(row=1, column=1)
        self.buttons["table_up10"].grid(row=0, column=1)
        self.buttons["table_down01"].grid(row=4, column=1)
        self.buttons["table_down"  ].grid(row=5, column=1)
        self.buttons["table_down10"].grid(row=6, column=1)
        self.buttons["table_plus"].grid(row=3, column=2)
        self.buttons["table_minus"].grid(row=3, column=0)
        self.entries["table"].grid(row=3, column=1)
        
        self.ex_label2.grid(row=0, column=0, rowspan=2)
        self.ex_label1.grid(row=5, column=0, rowspan=2)
        self.buttons["ex_up01"].grid(row=2, column=1)
        self.buttons["ex_up"  ].grid(row=1, column=1)
        self.buttons["ex_up10"].grid(row=0, column=1)
        self.buttons["ex_down01"].grid(row=4, column=1)
        self.buttons["ex_down"  ].grid(row=5, column=1)
        self.buttons["ex_down10"].grid(row=6, column=1)
        self.buttons["ex_plus"].grid(row=3, column=2)
        self.buttons["ex_minus"].grid(row=3, column=0)
        self.entries["ex"].grid(row=3, column=1)

    def move_head(self, direction, multiplier):
        d = eval(self.entries["xy"].get())*multiplier
        print("moving {}, {}".format(direction, d))

    def move_table(self, direction, multiplier):
        d = eval(self.entries["table"].get())*multiplier
        print("moving {}, {}".format(direction, d))

    def move_extruder(self, direction, multiplier):
        d = eval(self.entries["ex"].get())*multiplier
        print("moving {}, {}".format(direction, d))

    def add(self, label, val, allow_negative=False):
        x = eval(self.entries[label].get())
        x = math.ceil(x*10)
        if (x + val*10) >= 0 or allow_negative: x += val*10
        x /= 10
        self.entries[label].delete(0, "end")
        self.entries[label].insert("end", x)

class Camera_preview:
    def __init__(self, root, row=0, col=0, camera_frame=False):
        main_frame = Frame(root, pady=15, padx=15)
        main_frame.grid(row=row,  column=col, sticky="nsew")

        subtitle_cam = Label(main_frame, text = "camera", font=(label_font, label_size+3), bg=frame_color, borderwidth=2, relief=GROOVE)
        subtitle_cam.grid(sticky="ew", row = 0, column=0, columnspan=2)
        buttons_frame = Frame(main_frame, pady=15, padx=15, borderwidth=2, relief=GROOVE)
        buttons_frame.grid(row=1,  column=0, sticky="nsew")
        
        if camera_frame:
            camera_frame = Frame(main_frame, pady=15, padx=15, width=600, height=600, bg=frame_color, borderwidth=2, relief=GROOVE)
            camera_frame.grid(row=0,  column=1, sticky="nsew")

        self.labels = {}
        self.entries = {}
        self.buttons = {}
       
        self.buttons["cam_on"] = Button(buttons_frame, text = "preview", font=(label_font))
        self.buttons["zoom_in"] = Button(buttons_frame, text = "zoom in", font=(label_font))
        self.buttons["zoom_out"] = Button(buttons_frame, text = "zoom out", font=(label_font))
        self.buttons["snap"] = Button(buttons_frame, text = "snap", font=(label_font))
        self.buttons["rec"] = Button(buttons_frame, text = "rec", font=(label_font))
        
        self.buttons["cam_on"].grid(row=0, columnspan=2, sticky="ew")
        self.buttons["zoom_in"].grid(row=1, column=0, sticky="ew")
        self.buttons["zoom_out"].grid(row=2, sticky="ew")
        self.buttons["snap"].grid(row=3, sticky="ew")
        self.buttons["rec"].grid(row=4, sticky="ew")