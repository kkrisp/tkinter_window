try:
    # python 3.x
    import tkinter as tk
except ImportError:
    # python 2.x
    import Tkinter as tk

from time import trftime

import printer
import mystyle as stl
import custom_widgets as cw


class Controls(tk.Frame):
    def __init__(self, *args, position_manager, **kwargs):
        self.posman = position_manager
        tk.Frame.__init__(self, *args, **kwargs)

        self.set_btn = tk.Button(self, text="set", font=entry_font,
                                command=self.posman.select_default)
        self.new_btn = tk.Button(self, text="new", font=entry_font,
                                command=self.popup_save)
        self.delete_btn = tk.Button(self, text="delete", font=entry_font)
        self.go_btn = tk.Button(self, text="go", font=entry_font)

        self.new_btn.grid(   row=0, sticky='ew')
        self.set_btn.grid(   row=1, sticky="ew")
        self.delete_btn.grid(row=2, sticky="ew")
        self.go_btn.grid(    row=3, sticky="ew")

    def popup_save(self):
        # dummy position
        there = Position(1, 1, 1)
        x, y, z = there.string_c()

        popup_root = tk.Tk()
        popup_root.geometry('%dx%d+%d+%d' % (300, 130, 200, 200))
        popup_root.wm_title("New position")
        popup = tk.Frame(popup_root, padx = 15, pady = 15)
        popup.grid()

        coordinates = tk.Label(popup,
                            text=" " + there.toString() + " ",
                            font=stl.title_font,
                            justify='left',
                            borderwidth=2, relief=tk.GROOVE,
                            bg=stl.title_bg_color)

        save_btn = tk.Button(popup,
                            text="Save position",
                            font=stl.button_font,
                            command=lambda: self.save_position(popup_root, namevar.get(), x, y, z, new_type.get()) )

        cancel_btn = tk.Button(popup,
                            text="Cancel",
                            font=stl.button_font,
                            command=popup_root.destroy)
        

        namevar = tk.StringVar(popup)
        namevar.set("new-" + strftime("%m%d%H%M"))
        
        new_name = tk.Entry(popup, text=namevar,
                        width=15,
                        font=stl.entry_font,
                        bg=stl.entry_color,
                        borderwidth=1,
                        justify="left",
                        takefocus = 0)

        new_type = tk.StringVar(popup)
        new_type.set(Position.postype_list[0])

        new_type_menu = tk.OptionMenu(popup,
                        new_type,
                        *Position.postype_list)

        coordinates.grid(column=0, row=0, columnspan=2, sticky='ew')
        new_name.grid(row = 1, column=0, sticky='ew')
        new_type_menu.grid(row = 1, column=1, sticky="ew")
        save_btn.grid(row = 2, column=0, columnspan=1, sticky='we')
        cancel_btn.grid(row = 2, column=1, columnspan=1, sticky='we')
        popup.mainloop()
    
    
    def save_position(self, popup_win, name, x, y, z, postype):
        print("name = " + name + "; type: " + postype)
        self.posman.printer.save_position2(name, x, y, z, postype)
        self.posman.refresh()
        popup_win.destroy()


class Positionlist(tk.Frame):
    def __init__(self, *args, printer, **kwargs):
        entry_font = "Courier 12"
        entry_color = "white"
        tk.Frame.__init__(self, *args, **kwargs)
        self.printer = printer

        self.pos_title = Subtitle(self, text = "positions")
        self.column_titles = tk.Label(self,
                        font=entry_font,
                        bg=entry_color,
                        borderwidth=2,
                        relief=tk.GROOVE,
            text = " name       " + "        X       Y       Z" +
            "    " + "type    ", 
                        justify="left")
        self.pos_title.grid(row=0, columnspan=3, sticky="ew")
        self.column_titles.grid(row=1, sticky="ew")
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=1, rowspan=2, sticky='ns')

        self.btn = Manager_buttons(self, position_manager=self, padx=20)
        self.btn.grid(row=1, column=2, rowspan=2, sticky='nsew')

        self.position_list = tk.Listbox(self,
                                yscrollcommand = self.scrollbar.set,
                                width = (12+8+8+8+8+5),
                                height = 9,
                                font=entry_font,
                                bg=entry_color,
                                justify="left",
                                borderwidth = 2,
                                relief=tk.GROOVE)
        
        for k in self.printer.positions:
            x, y, z = self.printer.positions[k].string_c()
            postype = self.printer.positions[k].get_type()
            self.position_list.insert(tk.END,
                                    " " + k + (" "*(12-len(k))) +
                                    (" "*(8-len(x))) + x +
                                    (" "*(8-len(y))) + y +
                                    (" "*(8-len(z))) + z +
                                    "   " + postype + (" "*(8-len(postype))) )

        self.position_list.grid(row=2, column=0, sticky='nsew')
        self.scrollbar.config(command = self.position_list.yview )

    def select_default(self):
        print("sel.def")

    def refresh(self):
        self.position_list.delete(0, tk.END)  #clear listbox
        for k in self.printer.positions:
            x, y, z = self.printer.positions[k].string_c()
            postype = self.printer.positions[k].get_type()
            self.position_list.insert(tk.END,
                                    " " + k + (" "*(12-len(k))) +
                                    (" "*(8-len(x))) + x +
                                    (" "*(8-len(y))) + y +
                                    (" "*(8-len(z))) + z +
                                    "   " + postype + (" "*(8-len(postype))) )