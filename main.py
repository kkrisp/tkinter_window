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

def main(printer):
    # tkinter window, notebook style - tabs in the main window
    root = tk.Tk()
    root.title("Cellprinter GUI")
    style = ttk.Style(root)
    style.configure('lefttab.TNotebook', tabposition='nl')
    notebook = cw.Autoresized_Notebook(root, style='lefttab.TNotebook')

    #tabs
    f1 = tk.Frame(notebook, bg='#f0f0f0', width=200, height=200)
    f2 = tk.Frame(notebook, bg='#f0f0f0', width=200, height=200)
    notebook.add(f1, text='    Move     ')
    notebook.add(f2, text='    Print    ')
    notebook.pack()

    # first tab (movements, camera and positions)
    move = mv.Move(    f1, printer=printer, pady=5, padx=5)
    pman = pm.Positionlist(f1, printer=printer, pady=5, padx=5)
    camc = cc.CameraControl(f1, main_socket=None,pady=5, padx=5)
    
    # second tab (grid printing settings and preview)
    prev = pg.Preview(f2, printer=printer, pady=5, padx=5)
    pset = pg.Settings(f2, printer=printer, preview=prev, pady=5, padx=5)
    pset.grid(row=0, column=0, sticky="nsew")
    prev.grid(row=0, column=1, sticky="nsew")

    move.grid(row=0, column=0, columnspan = 1)
    camc.grid(row=0, column=1, columnspan = 1, sticky='n')
    pman.grid(row=1, column=0, columnspan = 2)
    root.mainloop()


if __name__ == '__main__':
    UMO = printer.Printer()
    main(UMO)