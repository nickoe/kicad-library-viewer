import cairo as C
from math import pi

width, height = 400, 250
output = "circle.png"

surf = C.ImageSurface(C.FORMAT_RGB24,width,height)
ctx = C.Context(surf)

# fill everyting with white
ctx.new_path()
ctx.set_source_rgb(0.9,0.9,0.9)
ctx.rectangle(0,0,width,height)
ctx.fill()  # fill current path

# display text in the center
ctx.set_source_rgb(0,0,0)  # black
txt = "Hello, world!"
ctx.select_font_face("Ubuntu", C.FONT_SLANT_NORMAL, C.FONT_WEIGHT_NORMAL)
ctx.set_font_size(18)
x_off, y_off, tw, th = ctx.text_extents(txt)[:4]
ctx.move_to(width/2-x_off-tw/2,height/2-y_off-th/2)
ctx.show_text(txt)

# draw a circle in the center
ctx.new_path()
ctx.set_source_rgb(0,0.2,0.8)  # blue
ctx.arc(width/2,height/2,tw*0.6,0,2*pi)
ctx.stroke()  # stroke current path

# save to PNG
surf.write_to_png(output)

