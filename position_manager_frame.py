try:
    # python 3.x
    import tkinter as tk
except ImportError:
    # python 2.x
    import Tkinter as tk

from time import strftime

import printer
import mystyle as stl
import custom_widgets as cw


class Controls(tk.Frame):
    """Generates the buttons and pop-up windows used to modify
    the position list and to send the printer to the given position"""
    def __init__(self, *args, position_manager, **kwargs):
        self.posman = position_manager
        tk.Frame.__init__(self, *args, **kwargs)

        self.set_btn = tk.Button(self, text="set", font=stl.entry_font,
                                command=self.posman.select_default)
        self.new_btn = tk.Button(self, text="new", font=stl.entry_font,
                                command=self.popup_save)
        self.delete_btn = tk.Button(self, text="delete", font=stl.entry_font,
                                command=lambda: self.posman.position_list.delete(tk.ANCHOR))
        self.go_btn = tk.Button(self, text="go", font=stl.entry_font,
                                command=self.go_to_position)

        self.new_btn.grid(   row=0, sticky='ew')
        self.set_btn.grid(   row=1, sticky="ew")
        self.delete_btn.grid(row=2, sticky="ew")
        self.go_btn.grid(    row=3, sticky="ew")

    def popup_save(self):
        """Creates a pop-up window that shows the parsed coordinates.
        The user can save it, choosing its type from a rolldown menu."""
        
        # dummy position
        there = printer.Position(1, 1, 1)
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
        namevar.set("new" + strftime("%H%M%S"))
        
        new_name = tk.Entry(popup, text=namevar,
                        width=15,
                        font=stl.entry_font,
                        bg=stl.entry_color,
                        borderwidth=1,
                        justify="left",
                        takefocus = 0)

        new_type = tk.StringVar(popup)
        new_type.set(printer.Position.postype_list[0])

        new_type_menu = tk.OptionMenu(popup,
                        new_type,
                        *printer.Position.postype_list)

        coordinates.grid(column=0, row=0, columnspan=2, sticky='ew')
        new_name.grid(row = 1, column=0, sticky='ew')
        new_type_menu.grid(row = 1, column=1, sticky="ew")
        save_btn.grid(row = 2, column=0, columnspan=1, sticky='we')
        cancel_btn.grid(row = 2, column=1, columnspan=1, sticky='we')
        popup.mainloop()
    
    def save_position(self, popup_win, name, x, y, z, postype):
        """This is the real saving of a position, we get there from
        the pop-up menu"""
        print("name = " + name + "; type: " + postype)
        self.posman.printer.save_position2(name, x, y, z, postype)
        self.posman.refresh()
        popup_win.destroy()

    def go_to_position(self):
        """If there is a ceiling, sends the printer to the
        given positions. If there is no ceiling set, the 
        user has co confirm the movement."""
        if self.posman.printer.use_ceiling == None:
            warning = tk.Tk()
            warning.geometry('%dx%d+%d+%d' % (600, 120, 30, 200))
            warning.wm_title("Warning")
            warning_frame = tk.Frame(warning, padx = 15, pady = 15)
            warning_frame.grid()
            proceed_btn = tk.Button(warning_frame,
                                text="Proceed",
                                font=stl.button_font,
                                command=lambda: self.go_but_really(warning) )

            cancel_btn = tk.Button(warning_frame,
                                text="Cancel",
                                font=stl.button_font,
                                command=warning.destroy)

            warning_label = tk.Label(warning_frame,
                                text=" Warning, no ceiling set. This might result in collosion.",
                                font=stl.title_font,
                                justify='left',
                                borderwidth=2, relief=tk.GROOVE,
                                bg=stl.warning_color)
            warning_label.grid(column=0, row=0, columnspan=2)
            proceed_btn.grid(column=0, row=1, sticky='ew')
            cancel_btn.grid(column=1, row=1, sticky='ew')
        else:
            self.go_but_really(None)
    
    def go_but_really(self, root):
        """The real G-code sending to the printer happens there"""
        try:
            name = self.posman.position_list.get(tk.ANCHOR).split(" ")[1]
        except IndexError:
            return
        self.posman.printer.move(name)
        if root != None:
            root.destroy()


class Positionlist(tk.Frame):
    """Creates a scrollable list from the saved positions. The
    saved positions are part of the Printer class. It also places
    the control buttons (using Control class) next to it.
    Displays the name, coordinates, type and marks the default
    (used by printing) positions with a '#'  """
    def __init__(self, *args, printer, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.printer = printer

        self.pos_title = cw.Subtitle(self, text = "positions")
        self.column_titles = tk.Label(self,
                        font=stl.entry_font,
                        bg=stl.entry_color,
                        borderwidth=2,
                        relief=tk.GROOVE,
            text = " name       " + "        X       Y       Z" +
            "    " + "type    ", 
                        justify="left")
        self.pos_title.grid(row=0, columnspan=3, sticky="ew")
        self.column_titles.grid(row=1, sticky="ew")
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=1, rowspan=2, sticky='ns')

        self.btn = Controls(self, position_manager=self, padx=20)
        self.btn.grid(row=1, column=2, rowspan=2, sticky='nsew')

        self.position_list = tk.Listbox(self,
                                yscrollcommand = self.scrollbar.set,
                                width = (12+8+8+8+8+8),
                                height = 9,
                                font=stl.entry_font,
                                bg=stl.entry_color,
                                justify="left",
                                borderwidth = 2,
                                relief=tk.GROOVE)
        
        for k in self.printer.positions:
            x, y, z = self.printer.positions[k].string_c()
            postype = self.printer.positions[k].get_type()
            tick = " "
            self.position_list.insert(tk.END,
                                    " " + k + (" "*(12-len(k))) +
                                    (" "*(8-len(x))) + x +
                                    (" "*(8-len(y))) + y +
                                    (" "*(8-len(z))) + z +
                                    "   " + postype + (" "*(8-len(postype))) +
                                    " "+tick+" ")

        self.position_list.grid(row=2, column=0, sticky='nsew')
        self.scrollbar.config(command = self.position_list.yview )

    def select_default(self):
        """Sets the selected position for use by grid printing.
        Marked ceiling is also used in every movement to avoid
        collosion."""
        try:
            name = self.position_list.get(tk.ANCHOR).split(" ")[1]
        except IndexError:
            return
        postype = self.printer.positions[name].postype
        self.printer.use_for_printing(name, postype)
        self.refresh()

    def refresh(self):
        """Deletes the whole list and refills it with the
        current positions. This is necessary to display newly
        added positions and the markers of the used ones."""
        self.position_list.delete(0, tk.END)  #clear listbox
        for k in self.printer.positions:
            tick = " "
            if k == self.printer.use_ceiling\
                or k == self.printer.use_petri\
                or k == self.printer.use_source: tick="#"
            x, y, z = self.printer.positions[k].string_c()
            postype = self.printer.positions[k].get_type()
            self.position_list.insert(tk.END,
                                    " " + k + (" "*(12-len(k))) +
                                    (" "*(8-len(x))) + x +
                                    (" "*(8-len(y))) + y +
                                    (" "*(8-len(z))) + z +
                                    "   " + postype + (" "*(8-len(postype))) +
                                    " "+tick+" ")