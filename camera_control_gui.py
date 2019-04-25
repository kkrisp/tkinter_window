try:
    # python 3.x
    import tkinter as tk
except ImportError:
    # python 2.x
    import Tkinter as tk
    
from tkinter_window.mywidgets import Subtitle
from tkinter_window.mywidgets import Editbox


class CameraControl(tk.Frame):
    def __init__(self, *args, main_socket, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # message syntact for the router
        MyID = "J"
        camID='C' #sending messages only to adress with 'C'
        self.header = "ZT" + camID + MyID +"000 "
        
        self.main_socket = main_socket
        self.preview_on = False
        self.zoom_value = 0

        self.subtitle_cam = Subtitle(self, "camera")
        self.buttons_frame = tk.Frame(self, pady=5, padx=5)#, borderwidth=2, relief=tk.GROOVE)

        self.subtitle_cam.grid(sticky="ew", row = 0, column=0)
        self.buttons_frame.grid(row=1,  column=0, sticky="nsew")

        self.entries = {}
        self.buttons = {}
       
        self.buttons["cam_on"] = tk.Button(self.buttons_frame, text = "preview", font=(label_font))
        self.buttons["zoom_in"] = tk.Button(self.buttons_frame, text = "zoom in", font=(label_font), command=self.zoom_in)
        self.buttons["zoom_out"] = tk.Button(self.buttons_frame, text = "zoom out", font=(label_font), command=self.zoom_out)
        self.buttons["snap"] = tk.Button(self.buttons_frame, text = "snap", font=(label_font), command=self.snap)
        self.buttons["rec"] = tk.Button(self.buttons_frame, text = "rec", font=(label_font))
        
        self.buttons["cam_on"].grid(row=0, columnspan=2, sticky="ew")
        self.buttons["zoom_in"].grid(row=1, column=0, sticky="ew")
        self.buttons["zoom_out"].grid(row=2, sticky="ew")
        self.buttons["snap"].grid(row=3, sticky="ew")
        #self.buttons["rec"].grid(row=4, sticky="ew")

    def zoom_in(self):
        if self.zoom_value < 6:
            self.zoom_value += 1
            self.main_socket.send(self.header + "z" + str(self.zoom_value) + "\n")
    def zoom_out(self):
        if self.zoom_value > 1:
            self.zoom_value -= 1
            self.main_socket.send(self.header + "z" + str(self.zoom_value) + "\n")
    
    def preview(self):
        if self.preview:
            self.main_socket.send(self.header + "ps" + "\n")
        else:
            self.main_socket.send(self.header + "px" + "\n")

    def snap(self):
        print("snap")