try:
    # python 3.x
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # python 2.x
    import Tkinter as tk
    import ttk

import custom_widgets as cw
import movements_frame as mv
import position_manager_frame as pm
import camera_control_frame as cc
import grid_setup_frame as pg
import printer
import math

def _create_circle(self, x, y, r, **kwargs):
    """This is a snippet from stackoverflow"""
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


class Preview(tk.Frame):
    def __init__(self, *args, print_settings, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.print_settings = print_settings
        self.subtitle = Subtitle(self, text="Preview")
        self.subtitle.grid(row = 0, column=1, sticky="nsew")
        prev_frame = tk.Frame(self, pady=5, padx=5, borderwidth=2, relief=tk.GROOVE)
        prev_frame.grid(row=1,  column=1, sticky="nsew")


        self.x_offset_label = tk.Label(prev_frame, text="Horizontal offset  (mm)", borderwidth=3, font=(label_font, label_size))
        self.y_offset_label = tk.Label(prev_frame, text="Vertical offset    (mm)", borderwidth=3, font=(label_font, label_size))
        x_offset_value = tk.IntVar()
        x_offset_value.set(dish_real_diameter/200)
        y_offset_value = tk.IntVar()
        y_offset_value.set(dish_real_diameter/200)
        self.x_offset_entry = Editbox(prev_frame, text = x_offset_value, width=6)
        self.y_offset_entry = Editbox(prev_frame, text = y_offset_value, width=6)
        self.refresh_button = tk.Button(prev_frame, text ="refresh", borderwidth=4, width=7, height=1, font=(entry_font, label_size), command=self.refresh)
        self.center_button = tk.Button(prev_frame, text = "center",  borderwidth=4, width=7, height=1, font=(entry_font, label_size), command=self.center)
        self.spacer = tk.Frame(prev_frame, borderwidth=1)

        self.x_offset_label.grid(row=1, column=0, sticky="w")
        self.x_offset_entry.grid(row=1, column=1, sticky="w")
        self.y_offset_label.grid(row=2, column=0, sticky="w")
        self.y_offset_entry.grid(row=2, column=1, sticky="w")
        self.refresh_button.grid(row=1, column=3, sticky="w")
        self.center_button.grid(row=2, column=3,  sticky="w")
        self.spacer.grid(row=1, column=4, rowspan=2, sticky="ew")

        self.prev_area = tk.Canvas(prev_frame, width=preview_size, height=preview_size, borderwidth=0, highlightthickness=0, bg=bg_color)
        self.prev_area.grid(row = 3, column=0, columnspan=5)
        #elf.clear()
        self.draw()
    
    def refresh(self):
        self.draw()
    def center(self):
        self.x_offset_entry.delete(0, tk.END) # this will delete everything inside the entry
        self.x_offset_entry.insert(tk.END, dish_real_diameter/200) # and this will insert the word "WORLD" in the entry.
        self.y_offset_entry.delete(0, tk.END) # this will delete everything inside the entry
        self.y_offset_entry.insert(tk.END, dish_real_diameter/200) # and this will insert the word "WORLD" in the entry.
        self.draw()

    def clear(self):
        self.prev_area.create_rectangle(preview_size, preview_size, 0, 0, fill=bg_color, outline="")
        self.prev_area.create_oval(border, # petri dish wall
                              border,
                              dish_size+dish_wall,
                              dish_size+dish_wall,
                              fill=wall_color,
                              outline='')
        self.prev_area.create_oval(border+dish_wall, # petri dish area
                              border+dish_wall,
                              dish_size,
                              dish_size,
                              fill=dish_color,
                              outline='')
    def draw(self):
        row=int(self.print_settings["col"])
        col=int(self.print_settings["row"])
        dia = self.print_settings["d"] * droplet_ratio
        dst = self.print_settings["dst"] * droplet_ratio
        growth = self.print_settings["d++"] * droplet_ratio

        self.clear()
        width =  dst*(col-1)/2.0
        offset_x = eval(self.x_offset_entry.get())*ratio*100-width +dish_wall

        if self.print_settings["hex"]:
            distance_ratio = 0.866025403784 # sqrt(3)/2
            dst_red = dst * distance_ratio
            height = dst_red*(row-1)/2.0
            offset_y = eval(self.y_offset_entry.get())*ratio*100-height+dish_wall
            indent = dst_red/3.33333333
            for i in range(row):
                indent *= -1
                for j in range(col):
                    self.prev_area.create_circle(
                        offset_x + j*dst + indent,
                        offset_y + i*dst_red,
                        dia +  growth*(j+col*i),
                        fill=drop_color,
                        outline='')
        else:
            height = dst*(row-1)/2.0
            offset_y = eval(self.y_offset_entry.get())*ratio*100-height+dish_wall
            for i in range(row):
                for j in range(col):
                    self.prev_area.create_circle(
                        offset_x + j*dst,
                        offset_y + i*dst,
                        dia +  growth*(j+col*i),
                        fill=drop_color,
                        outline='')


class Settings(tk.Frame):
    dscr = { # descriptions
            "dst": "distance",
            "d":   "size",
            "h"  : "travel height",
            "row": "columns",
            "col": "rows",
            "h++": "change print height",
            "t"  : "sleep between droplets",
            "t++": "change sleep time",
            "eh" : "extrude with head down",
            "s"  : "print grid in an S route",
            "cor": "correct hysteresys",
            "pul": "last extruder action",
            "d++": "change size",
            "hex": "hexagonal pattern"
            }
    def __init__(self, *args, print_settings, preview=None, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.preview = preview
        self.print_settings = print_settings
        self.img_rightarrow = tk.PhotoImage(file = img_path+"plus_small.png")
        self.img_leftarrow = tk.PhotoImage(file = img_path+"minus_small.png")

        settings_frame = tk.Frame(self, pady=5, padx=5, borderwidth=2, relief=tk.GROOVE)
        subtitle = Subtitle(self, "Grid printing settings")
        print_frame = tk.Frame(self, pady=5, padx=5, borderwidth=2, relief=tk.GROOVE)

        subtitle.grid(      row=0, column=0, sticky="nsew")
        settings_frame.grid(row=1,  column=0, sticky="nsew")
        print_frame.grid(   row=2,  column=0, sticky="nsew")

        self.print_btn = tk.Button(print_frame,
                                text="start printing",
                                bg=wall_color,
                                fg="white",
                                font=big_font,
                                activebackground=wall_color,
                                activeforeground="white",
                                command=self.view_settings)

        self.def_petri_box = tk.Checkbutton(print_frame, text="find petri dish automatically", font=small_font)
        self.def_source_box = tk.Checkbutton(print_frame, text="get material automatically", font=small_font)
        self.print_btn.grid(     row=0, column=0, sticky="w",)
        self.def_petri_box.grid( row=1, column=0, sticky="w",)
        self.def_source_box.grid(row=2, column=0, sticky="w",)
        
        i=0
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        
        for name in ["row", "col", "dst", "d", "d++", "t", "t++", "h", "h++", "cor"]:
            self.labels[name] = tk.Label(settings_frame, text = Settings.dscr[name], borderwidth=3, font=(label_font, label_size))
            v = tk.IntVar()
            v.set(self.print_settings[name])
            self.entries[name] = Editbox(settings_frame, text = v, width=6)

        self.buttons["dst"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "dst"))
        self.buttons["dst"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "dst"))
        
        self.buttons["d"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "d"))
        self.buttons["d"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "d"))
        
        self.buttons["row"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-1,"row"))
        self.buttons["row"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(1,"row"))
        
        self.buttons["col"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-1,"col"))
        self.buttons["col"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(1,"col"))
        
        self.buttons["d++"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.01, "d++", allow_negative=True))
        self.buttons["d++"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.01, "d++", allow_negative=True))
        
        self.buttons["h"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "h"))
        self.buttons["h"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "h"))
        
        self.buttons["h++"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.01, "h++"))
        self.buttons["h++"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.01, "h++"))
        
        self.buttons["t"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "t"))
        self.buttons["t"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "t"))
        
        self.buttons["t++"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "t++", allow_negative=True))
        self.buttons["t++"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "t++", allow_negative=True))
        
        self.buttons["cor"+"_left"] = tk.Button(settings_frame, image=self.img_leftarrow, command=lambda: self.add(-0.1, "cor"))
        self.buttons["cor"+"_right"] = tk.Button(settings_frame, image=self.img_rightarrow, command=lambda: self.add(0.1, "cor"))
        
        self.buttons["cor"] = tk.Checkbutton(settings_frame,
                                            command=self.change_correction)
        self.buttons["hex"] = tk.Checkbutton(settings_frame,
                                            text=Settings.dscr["hex"],
                                            font=("Courier", 10),
                                            command=lambda: self.change("hex"))
        self.buttons["eh" ] = tk.Checkbutton(settings_frame,
                                            text=Settings.dscr["eh"], 
                                            font=("Courier", 10),
                                            command=lambda: self.change("eh"))
        
        self.spacer = tk.Frame(settings_frame, bg=bg_color, height=20, width=300)

        # options with value
        for name in ["row", "col", "dst", "d", "d++", "h", "h++", "t", "t++", "cor"]:
            self.buttons[name+"_left"].grid( row = i, column=0)
            self.entries[name].grid(         row = i, column=1)
            self.buttons[name+"_right"].grid(row = i, column=2)
            self.labels[name].grid(sticky="w", row = i, column=3, columnspan=2)
            i+=1
        self.spacer.grid(row=i, column=0, columnspan=4)
        i+=1
        # yes or no options
        for name in ["hex", "eh"]:
            self.buttons[name].grid(sticky="w", row = i, column=0, columnspan=4)
            i+=1

    def add(self, val, name, allow_negative=False):
        x = eval(self.entries[name].get())
        x = math.ceil(x*1000)
        if (x + val*1000) >= 0 or allow_negative:
            x += val*1000
        x /= 1000
        self.entries[name].delete(0, tk.END) # this will delete everything inside the entry
        self.entries[name].insert(tk.END, x) # and this will insert the word "WORLD" in the entry.
        self.print_settings[name] = x
        self.preview.draw()

    def change(self, name):
        self.print_settings[name] = not self.print_settings[name]
        self.preview.draw()

    def change_correction(self):
        if self.print_settings["cor"]:
            self.print_settings["cor"] = False
            self.entries["cor"].config(state='disabled')
            #self.entries["cor"].config(bg="red")
            #self.buttons["cor"+"_right"].grid(row = 9, column=2)
        else:
            print("was: not setting to yes")
            self.print_settings["cor"] = True
            self.entries["cor"].config(state='normal')
            #self.entries["cor"].config(bg="white")
            #self.buttons["cor"+"_right"].grid(row = 9, column=2)

    def view_settings(self):
        for k in self.print_settings:
            print(self.print_settings[k])