try:
    # python 3.x
    import tkinter as tk
except ImportError:
    # python 2.x
    import Tkinter as tk

import custom_widgets as cw
import mystyle as stl
import math # to correct numerical errors

class Move(tk.Frame):
    """A GUI for moving the printer head. It generates buttons
    to move in every (x, y, z) direction and to control the extruder.
    Movements have a base step size, which can be changed by the user.
    To every direction belongs 3 buttons, which multiply the base step
    size by 10, 1 or 0.1. Pressing one button sends a G-code to the
    printer accordingly. 
    
    'Movements' is an extension of the Frame class, with one extra
    parameter, 'printer', which is 'Printer' class and represents the
    printer the G-codes are sent to."""
    def __init__(self, *args, printer, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # subframes and subtitles
        self.printer = printer
        self.subtitle_xy = cw.Subtitle(self, text = "head")
        self.subtitle_z  = cw.Subtitle(self, text = "table")
        self.subtitle_ex = cw.Subtitle(self, text = "extruder")
        self.xy_frame = tk.Frame(self, pady=5, padx=5, borderwidth=2, relief=tk.GROOVE)
        self.z_frame  = tk.Frame(self, pady=18, padx=5, borderwidth=2, relief=tk.GROOVE)
        self.ex_frame = tk.Frame(self, pady=18, padx=5, borderwidth=2, relief=tk.GROOVE)

        self.subtitle_xy.grid(sticky="ew", row = 0, column=0)
        self.subtitle_z.grid( sticky="ew", row = 0, column=1)
        self.subtitle_ex.grid(sticky="ew", row = 0, column=2)
        self.xy_frame.grid(row=1,  column=0, sticky="nsew")
        self.z_frame.grid( row=1,  column=1, sticky="nsew")
        self.ex_frame.grid(row=1,  column=2, sticky="nsew")

        # entries and buttons
        self.entries = {}
        self.buttons = {}

        self.xy_entry_value = tk.IntVar()
        self.z_entry_value  = tk.IntVar()
        self.ex_entry_value = tk.IntVar()
        self.xy_entry_value.set(1)
        self.z_entry_value.set( 1)
        self.ex_entry_value.set(0.1) # fine step for the extruder
        
        
        self.button_img = []
        # images for directions (up 0.1, up 1, up 10, down..., left..., right... )
        for i in range(12):
            self.button_img.append(tk.PhotoImage(file=stl.imgpath+"gl"+ str(i*5+2000) +".png"))
        # images for changing values
        self.button_img.append(tk.PhotoImage(file = stl.imgpath+"plus.png"))
        self.button_img.append(tk.PhotoImage(file = stl.imgpath+"minus.png"))

        # images to explain directions
        self.xy_label_img = tk.PhotoImage(file = stl.imgpath+"xy_label.png")
        self.z_label1_img = tk.PhotoImage(file = stl.imgpath+"z_raise.png")
        self.z_label2_img = tk.PhotoImage(file = stl.imgpath+"z_lower.png")
        self.ex_label1_img = tk.PhotoImage(file = stl.imgpath+"ex_push.png")
        self.ex_label2_img = tk.PhotoImage(file = stl.imgpath+"ex_pull.png")

        self.entries["xy"] = cw.Editbox(self.xy_frame, text =self.xy_entry_value, width=6)
        self.buttons["up01"] = tk.Button(self.xy_frame, image=self.button_img[0], command=lambda: self.move_head("Y", -0.1))
        self.buttons["up"  ] = tk.Button(self.xy_frame, image=self.button_img[1], command=lambda: self.move_head("Y", -1))
        self.buttons["up10"] = tk.Button(self.xy_frame, image=self.button_img[2], command=lambda: self.move_head("Y", -10))
        self.buttons["down01"] = tk.Button(self.xy_frame, image=self.button_img[3], command=lambda: self.move_head("Y", 0.1))
        self.buttons["down"  ] = tk.Button(self.xy_frame, image=self.button_img[4], command=lambda: self.move_head("Y", 1))
        self.buttons["down10"] = tk.Button(self.xy_frame, image=self.button_img[5], command=lambda: self.move_head("Y", 10))
        self.buttons["left01"] = tk.Button(self.xy_frame, image=self.button_img[6], command=lambda: self.move_head("X", -0.1))
        self.buttons["left"  ] = tk.Button(self.xy_frame, image=self.button_img[7], command=lambda: self.move_head("X", -1))
        self.buttons["left10"] = tk.Button(self.xy_frame, image=self.button_img[8], command=lambda: self.move_head("X", -10))
        self.buttons["right01"] = tk.Button(self.xy_frame, image=self.button_img[9], command=lambda: self.move_head( "X", 0.1))
        self.buttons["right"  ] = tk.Button(self.xy_frame, image=self.button_img[10], command=lambda: self.move_head("X", 1))
        self.buttons["right10"] = tk.Button(self.xy_frame, image=self.button_img[11], command=lambda: self.move_head("X", 10))
        self.buttons["xy_plus" ] = tk.Button(self.xy_frame, image=self.button_img[12], command=lambda: self.add("xy", 1))
        self.buttons["xy_minus"] = tk.Button(self.xy_frame, image=self.button_img[13], command=lambda: self.add("xy", -1))
        self.xy_label = tk.Label(self.xy_frame, image=self.xy_label_img)

        self.entries["table"] = cw.Editbox(self.z_frame, text = self.z_entry_value, width=6)
        self.buttons["table_up01"] = tk.Button(self.z_frame, image=self.button_img[0], command=lambda: self.move_table("Z", -0.1))
        self.buttons["table_up"  ] = tk.Button(self.z_frame, image=self.button_img[1], command=lambda: self.move_table("Z", -1))
        self.buttons["table_up10"] = tk.Button(self.z_frame, image=self.button_img[2], command=lambda: self.move_table("Z", -10))
        self.buttons["table_down01"] = tk.Button(self.z_frame, image=self.button_img[3], command=lambda: self.move_table("Z", 0.1))
        self.buttons["table_down"  ] = tk.Button(self.z_frame, image=self.button_img[4], command=lambda: self.move_table("Z", 1))
        self.buttons["table_down10"] = tk.Button(self.z_frame, image=self.button_img[5], command=lambda: self.move_table("Z", 10))
        self.buttons["table_plus"  ] = tk.Button(self.z_frame, image=self.button_img[12], command=lambda: self.add("table", 1))
        self.buttons["table_minus"] = tk.Button(self.z_frame, image=self.button_img[13], command=lambda: self.add("table", -1))
        self.z_label1 = tk.Label(self.z_frame, image=self.z_label1_img)
        self.z_label2 = tk.Label(self.z_frame, image=self.z_label2_img)

        self.entries["ex"] = cw.Editbox(self.ex_frame, text = self.ex_entry_value, width=6)
        self.buttons["ex_up01"] = tk.Button(self.ex_frame, image=self.button_img[0], command=lambda: self.move_extruder("E", 0.1))
        self.buttons["ex_up"  ] = tk.Button(self.ex_frame, image=self.button_img[1], command=lambda: self.move_extruder("E", 1))
        self.buttons["ex_up10"] = tk.Button(self.ex_frame, image=self.button_img[2], command=lambda: self.move_extruder("E", 10))
        self.buttons["ex_down01"] = tk.Button(self.ex_frame, image=self.button_img[4], command=lambda: self.move_extruder("E", -0.1))
        self.buttons["ex_down"  ] = tk.Button(self.ex_frame, image=self.button_img[3], command=lambda: self.move_extruder("E", -1))
        self.buttons["ex_down10"] = tk.Button(self.ex_frame, image=self.button_img[5], command=lambda: self.move_extruder("E", -10))
        self.buttons["ex_plus"  ] = tk.Button(self.ex_frame, image=self.button_img[12], command=lambda: self.add("ex", 0.1))
        self.buttons["ex_minus"] = tk.Button(self.ex_frame, image=self.button_img[13], command=lambda: self.add("ex", -0.1))
        self.ex_label1 = tk.Label(self.ex_frame, image=self.ex_label1_img)
        self.ex_label2 = tk.Label(self.ex_frame, image=self.ex_label2_img)

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
        #print("moving {}, {}".format(direction, d))
        self.printer.m.send(direction+str(d))

    def move_table(self, direction, multiplier):
        d = eval(self.entries["table"].get())*multiplier
        #print("moving {}, {}".format(direction, d))
        self.printer.m.send(direction+str(d))

    def move_extruder(self, direction, multiplier):
        d = eval(self.entries["ex"].get())*multiplier
        #print("moving {}, {}".format(direction, d))
        self.printer.m.send(direction+str(d))

    def add(self, label, val, allow_negative=False):
        x = eval(self.entries[label].get())
        x = math.ceil(x*10)
        if (x + val*10) >= 0 or allow_negative: x += val*10
        x /= 10
        self.entries[label].delete(0, "end")
        self.entries[label].insert("end", x)