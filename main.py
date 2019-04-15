# this is a plain window, actually for the cellprinter app
from tkinter import *
from tkinter import ttk
import math

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

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class Petri_preview:
    def __init__(self, root, row=0, col=0):
        prev_frame = Frame(root)
        prev_frame.grid(row=row,  column=col)
        self.subtitle = Label(prev_frame, text = "Preview", borderwidth=5, font=(label_font, label_size+3))
        self.subtitle.grid(sticky=W, row = 0, column=0)

        self.x_offset_label = Label(prev_frame, text="Horizontal offset  (mm)", borderwidth=3, font=(label_font, label_size))
        self.y_offset_label = Label(prev_frame, text="Vertical offset    (mm)", borderwidth=3, font=(label_font, label_size))
        x_offset_value = IntVar()
        x_offset_value.set(dish_real_diameter/2*ratio)
        y_offset_value = IntVar()
        y_offset_value.set(dish_real_diameter/2*ratio)
        self.x_offset_entry = Entry(prev_frame, text = x_offset_value, borderwidth=1, width=6, justify=CENTER, font=(entry_font, label_size))
        self.y_offset_entry = Entry(prev_frame, text = y_offset_value, borderwidth=1, width=6, justify=CENTER, font=(entry_font, label_size))
        self.refresh_button = Button(prev_frame, text ="refresh", borderwidth=4, width=7, height=1, font=(entry_font, label_size), command=self.refresh)
        self.center_button = Button(prev_frame, text = "center",  borderwidth=4, width=7, height=1, font=(entry_font, label_size), command=self.center)
        self.spacer = Frame(prev_frame, borderwidth=1)

        self.x_offset_label.grid(row=1, column=0, sticky="w")
        self.x_offset_entry.grid(row=1, column=1, sticky="w")
        self.y_offset_label.grid(row=2, column=0, sticky="w")
        self.y_offset_entry.grid(row=2, column=1, sticky="w")
        self.refresh_button.grid(row=1, column=3, sticky="w")
        self.center_button.grid(row=2, column=3,  sticky="w")
        self.spacer.grid(row=1, column=4, rowspan=2, sticky="ew")

        self.prev_area = Canvas(prev_frame, width=preview_size, height=preview_size, borderwidth=0, highlightthickness=0, bg=bg_color)
        self.prev_area.grid(row = 3, column=0, columnspan=5)
        self.clear()
    
    def refresh(self):
        self.draw()
    def center(self):
        self.x_offset_entry.delete(0, END) # this will delete everything inside the entry
        self.x_offset_entry.insert(END, dish_real_diameter/2*ratio) # and this will insert the word "WORLD" in the entry.
        self.y_offset_entry.delete(0, END) # this will delete everything inside the entry
        self.y_offset_entry.insert(END, dish_real_diameter/2*ratio) # and this will insert the word "WORLD" in the entry.
        self.draw()

    def clear(self):
        self.prev_area.create_rectangle(preview_size, preview_size, border, border, fill=bg_color, outline="")
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
        row=int(myopt.value(name="row"))
        col=int(myopt.value(name="col"))
        dia = myopt.value("d"  ) * droplet_ratio
        dst = myopt.value("dst") * droplet_ratio
        growth = myopt.value("d++") * droplet_ratio

        self.clear()
        width =  dst*(col-1)/2.0
        offset_x = eval(self.x_offset_entry.get())-width +dish_wall

        if myopt.value(name="hex"):
            distance_ratio = 0.866025403784 # sqrt(3)/2
            dst_red = dst * distance_ratio
            height = dst_red*(row-1)/2.0
            offset_y = eval(self.y_offset_entry.get())-height+dish_wall
            indent = dst_red/3.3
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
            offset_y = eval(self.y_offset_entry.get())-height+dish_wall
            for i in range(row):
                for j in range(col):
                    self.prev_area.create_circle(
                        offset_x + j*dst,
                        offset_y + i*dst,
                        dia +  growth*(j+col*i),
                        fill=drop_color,
                        outline='')


class Settings:
    def __init__(self):
        self.settings = {
            "dst":[2.5, "distance"],
            "d":  [1.0, "size"],
            "h"  :[3.0, "head height while moving"],
            "row":[3,   "columns"],
            "col":[3,   "rows"],
            "h++":[0.0, "change head height"],
            "t"  :[0.0, "wait time between droplets"],
            "t++":[0.0, "change waiting time"],
            "eh" :[1,   "extrude when head is lifted"],
            "s"  :[1,   "print grid in an S route"],
            "cor":[2.3, "correct hysteresys"],
            "pul":[1,   "last extruder action"],
            "d++":[0.0, "change size"],
            "hex":[False  , "hexagonal pattern"]
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

class Printsettings:
    def __init__(self, root, settings, row=0, col=0):
        frame = Frame(root, pady=15, padx=15)
        frame.grid(row=row,  column=col, sticky="nsew")
        i=0
        self.subtitle = Label(frame, text = "Grid printing settings", borderwidth=5, font=(label_font, label_size+3))
        self.subtitle.grid(sticky=W, row = i, column=0, columnspan=4)
        i+=1
        spacer = Frame(frame, bg=bg_color, height=20, width=300)
        spacer.grid(row=i, column=0, columnspan=4)
        i+=1
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        
        for name in ["row", "col", "dst", "d", "d++", "t", "t++", "h", "h++"]:
            self.labels[name] = Label(frame, text = settings.description(name), borderwidth=3, font=(label_font, label_size))
            v = IntVar()
            v.set(settings.value(name = name))
            self.entries[name] = Entry(frame, text = v, borderwidth=1, width=6, justify=CENTER, font=(entry_font, entry_size))

        self.buttons["dst"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "dst"))
        self.buttons["dst"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "dst"))
        
        self.buttons["d"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "d"))
        self.buttons["d"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "d"))
        
        self.buttons["row"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-1,"row"))
        self.buttons["row"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(1,"row"))
        
        self.buttons["col"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-1,"col"))
        self.buttons["col"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(1,"col"))
        
        self.buttons["d++"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "d++", allow_negative=True))
        self.buttons["d++"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "d++", allow_negative=True))
        
        self.buttons["h"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "h"))
        self.buttons["h"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "h"))
        
        self.buttons["h++"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "h++"))
        self.buttons["h++"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "h++"))
        
        self.buttons["t"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "t"))
        self.buttons["t"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "t"))
        
        self.buttons["t++"+"_left"] = Button(frame, image=l_a_p, command=lambda: self.add(-0.1, "t++", allow_negative=True))
        self.buttons["t++"+"_right"] = Button(frame, image=r_a_p, command=lambda: self.add(0.1, "t++", allow_negative=True))

        self.buttons["eh" ] = Checkbutton(frame, text=settings.description("eh"), font=("Courier", 10))
        self.buttons["cor"] = Checkbutton(frame, text=settings.description("cor"), font=("Courier", 10), command=lambda: self.change("cor"))
        self.buttons["hex"] = Checkbutton(frame, text=settings.description("hex"), font=("Courier", 10), command=lambda: self.change("hex"))


        # options with value
        for name in ["row", "col", "dst", "d", "d++", "h", "h++", "t", "t++"]:
            self.buttons[name+"_left"].grid( row = i, column=0)
            self.entries[name].grid(         row = i, column=1)
            self.buttons[name+"_right"].grid(row = i, column=2)
            self.labels[name].grid(sticky=W, row = i, column=3)
            i+=1
        spacer = Frame(frame, bg=bg_color, height=20, width=300)
        spacer.grid(row=i, column=0, columnspan=4)
        i+=1
        # yes or no options
        for name in ["hex", "eh", "cor"]:
            self.buttons[name].grid(sticky=W, row = i, column=0, columnspan=4)
            i+=1
        i+=1
        bottom = Frame(frame, bg=bg_color, height=20, width=300)
        bottom.grid(row=i, column=0, columnspan=4, sticky="ns")

    def add(self, val, name, allow_negative=False):
        x = eval(self.entries[name].get())
        x = math.ceil(x*10)
        if (x + val*10) >= 0 or allow_negative: x += val*10
        x /= 10
        self.entries[name].delete(0, END) # this will delete everything inside the entry
        self.entries[name].insert(END, x) # and this will insert the word "WORLD" in the entry.
        myopt.set_value(x, name=name)
        pprev.draw()

    def change(self, name):
        myopt.set_value((not myopt.value(name)), name)
        pprev.draw()

root = Tk()
root.title("Cellprinter GUI")
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='ws')
notebook = ttk.Notebook(root, style='lefttab.TNotebook')

r_a_p = PhotoImage(file = "rightarrow.png")
l_a_p = PhotoImage(file = "leftarrow.png")
myopt = Settings()

f1 = Frame(notebook, bg='red', width=200, height=200)
f2 = Frame(notebook, bg='blue', width=200, height=200)
notebook.add(f1, text='Move      ')
notebook.add(f2, text='Print grid')
notebook.pack()

opts = Printsettings(f2, myopt, row=0, col=0)
pprev = Petri_preview(f2, row=0, col=1)
pprev.draw()

root.mainloop()