# circle creating slippet
# source: https://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python
from ktinker import *
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)

Canvas.create_circle = _create_circle
Canvas.create_circle_arc = _create_circle_arc