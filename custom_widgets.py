try:
    # python 3.x
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # python 2.x
    import Tkinter as tk
from gcontrol import Position as o_Position
import style

class Autoresized_Notebook(ttk.Notebook):
  """Snippet from stackoverflow"""
  def __init__(self, master=None, **kw):

    ttk.Notebook.__init__(self, master, **kw)
    self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

  def _on_tab_changed(self,event):
    event.widget.update_idletasks()

    tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(width=tab.winfo_reqwidth())


class Subtitle_o(tk.Label):
    """Label with darker colour and a border"""
    def __init__(self, master, text):
        tk.Label.__init__(self, master, text=text,
                        font=title_font,
                        bg=title_color,
                        borderwidth=2,
                        relief=tk.GROOVE)


class Subtitle(tk.Label):
    """Label with darker colour and a border"""
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args,
                        font=style.title_font,
                        bg=style.title_color,
                        borderwidth=2,
                        relief=tk.GROOVE)


class Editbox(tk.Entry):
    """Standard entry used in the gui
    Entry widget with white background
    and larger, monospace font"""
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args,
                    font=style.entry_font,
                    bg  =style.entry_color,
                    borderwidth=1,
                    justify="center",
                    takefocus = 0,
                    **kwargs)
    #def __init__(self, master, text, width):
    #    tk.Entry.__init__(self, master, text=text,
    #                    width=width,
    #                    font=entry_font,
    #                    bg=entry_color,
    #                    borderwidth=1,
    #                    justify="center",
    #                    takefocus = 0)