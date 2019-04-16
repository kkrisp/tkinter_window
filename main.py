# this is a plain window, actually for the cellprinter app
from tkinter import *
from tkinter import ttk
import math
import print_grid
from print_grid import Petri_preview
from print_grid import Printsettings
from print_settings import Settings
import movements as mv
import positions as pos
from gcontrol import Position

myopt = Settings()
root = Tk()
root.title("Cellprinter GUI")
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='nl')
notebook = ttk.Notebook(root, style='lefttab.TNotebook')

f1 = Frame(notebook, bg='#f0f0f0', width=200, height=200)
f2 = Frame(notebook, bg='#f0f0f0', width=200, height=200)
f3 = Frame(notebook, bg='#f0f0f0', width=200, height=200)
notebook.add(f1, text='Move      ')
notebook.add(f2, text='Print grid')
notebook.add(f3, text='Positions ')
notebook.pack()

mypositions = {}
mypositions["old"] = Position()
mypositions["old2"] = Position(100, 100, 100)

mypos = pos.Positionlist(mypositions)
mypos.add(Position(234, 112, 76), "new", "petri dish centre")
mypos.add(Position(234, 112, 76), postype="material source")

pprev = Petri_preview(f2, myopt, row=0, col=1)
pset = Printsettings(f2, myopt, pprev, row=0, col=0)
move = mv.Movements(f1, row=0, col=0)
cam = mv.Camera_preview(f1, row=0, col=1)
pmanager = pos.Manager(f3, mypos, row=0, col=0)
pslist = pos.Save(f1, mypos, pmanager, row=1, col=0)
pprev.draw()

root.mainloop()