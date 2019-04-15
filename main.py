# this is a plain window, actually for the cellprinter app
from tkinter import *
from tkinter import ttk
import math
import print_grid
from print_grid import Petri_preview
from print_grid import Printsettings
from print_settings import Settings
import movements as mv

myopt = Settings()
root = Tk()
root.title("Cellprinter GUI")
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='nl')
notebook = ttk.Notebook(root, style='lefttab.TNotebook')

f1 = Frame(notebook, bg='red', width=200, height=200)
f2 = Frame(notebook, bg='#f0f0f0', width=200, height=200)
notebook.add(f1, text='Move      ')
notebook.add(f2, text='Print grid')
notebook.pack()

pprev = Petri_preview(f2, myopt, row=0, col=1)
pset = Printsettings(f2, myopt, pprev, row=0, col=0)
move = mv.Movements(f1, row=0, col=0)
cam = mv.Camera_preview(f1, row=0, col=1)
pprev.draw()

root.mainloop()