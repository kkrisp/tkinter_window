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
    notebook.add(f1, text='    Move     ')
    notebook.pack()

    # first tab (movements, camera and positions)
    move = mv.Move(    f1, printer=printer, pady=5, padx=5)
    #pman = pm.Managerwindow(f1, printer=printer, pady=5, padx=5)
    #camc = mv.CameraControl(f1, main_socket=None,pady=5, padx=5)

    move.grid(row=0, column=0, columnspan = 1)
    #camc.grid(row=0, column=1, columnspan = 1)
    #pman.grid(row=2, column=0, columnspan = 3)
    root.mainloop()


if __name__ == '__main__':
    UMO = printer.Printer()
    main(UMO)