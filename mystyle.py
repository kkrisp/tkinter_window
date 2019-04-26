title_font = "Courier 13"
title_color = '#d7dce0' #light, blueish gray
entry_font = "Courier 13"
entry_color = "white"
label_font = "Courier 11"
button_font = "Courier 12"
small_font = "Courier 12"

imgpath = 'img/' # path to the image files

warning_color = '#e0948d' #pastel red
bg_color = '#f0f0f0' #gray
frame_color = '#d7dce0' #a bit darker blueish gray
title_bg_color = '#a1a9c6'
dish_color = '#e0e7ee' # light blue
wall_color = '#577892' # dark grey blue
drop_color = '#915aa7' #light purple
drop_color_dark = '#412847' #dark purple
drop_line = '' # no color
large_font = "Courier 14 bold"

border = 10
dish_wall = 10
droplet_ratio = 20.0

dish_real_diameter = 35000 #um
ratio = 1.0/90.0
dish_size = dish_real_diameter*ratio
preview_size = dish_size+dish_wall+border
volume_ratio = 1
safety_factor = 2
dscr = { # descriptions
        "dst": "distance",
        "d":   "size",
        "h"  : "travel height",
        "row": "columns",
        "col": "rows",
        "h++": "change print height",
        "t"  : "sleep between droplets",
        "t++": "change sleep time",
        "eh" : "extrude with head down",
        "s"  : "print grid in an S route",
        "cor": "correct hysteresys",
        "pul": "last extruder action",
        "d++": "change size",
        "hex": "hexagonal pattern"
        }