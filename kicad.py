# This file can generate PNGs of a KiCad librarys components
import cairo as C
from math import pi

# Contruct stuff for Cairo
width, height = 800, 500
output = "output.png"
surf = C.ImageSurface(C.FORMAT_RGB24,width,height)
ctx = C.Context(surf)

# fill everyting with white
ctx.new_path()
ctx.set_source_rgb(1,1,1)
ctx.rectangle(0,0,width,height)
ctx.fill()  # fill current path

# Open kicad file
f = open('bc307.lib', 'r')
content = (f.readlines())
f.close()

graphic_color = [0.625,0,0]
label_color = [0,0.625,0.625]

def draw_element(line):
	ctx.set_line_cap(C.LINE_CAP_ROUND)
	ctx.set_line_join(C.LINE_JOIN_ROUND)

	if line[0] == "C": # C posx posy radius unit convert ltrait cc
		ctx.new_path()
		ctx.arc(width/2+int(line[1]),height/2-int(line[2]),float(line[3]),0,2*pi)
		ctx.set_line_width(float(line[6]))
		ctx.set_source_rgb(*graphic_color)
		ctx.stroke()
	elif line[0] == "P": # P Nb parts convert ltrait  x0 y0  x1 y1  xi yi cc
		numpoints = int(line[1])
		ctx.new_path()
		# Some old footprints has a line width of zero, so we set a size
		if float(line[4]) == 0:
			ctx.set_line_width(6)
		else:
			ctx.set_line_width(float(line[4]))
		ctx.move_to(width/2+float(line[6]),height/2-float(line[7]))
		for ii in range(numpoints):
			x = 6 + (ii*3)
			y = (6 + 1) + (ii*3)
			ctx.line_to(width/2+float(line[x]),height/2-float(line[y]))
		ctx.fill_preserve()
		ctx.stroke()
		
	elif line[0] == "X": # X name number posx posy length orientation Snum Snom unit convert Etype [shape]
		ctx.new_path()

		name = line[1]
		number = line[2]
		x = float(line[3])
		y = float(line[4])
		length = float(line[5])
		
		# Draw endpoints
		ctx.new_path()
		ctx.set_source_rgb(*graphic_color)
		ctx.set_line_width(1)
		ctx.arc(width/2+x,height/2-y,10,0,2*pi) # This should be a thin line width
		ctx.stroke()
		
		# Draw the rest of the pin
		ctx.new_path()
		ctx.set_line_width(6)
		ctx.move_to(width/2+x,height/2-y)
		if line[6] == "U":
			#ctx.set_source_rgb(*graphic_color)
			ctx.line_to(width/2+x,height/2+length)
			ctx.set_font_size(float(line[8])*1.5)
			x_off, y_off, tw, th = ctx.text_extents(number)[:4]
			ctx.move_to(width/2-x_off-tw/2+x,height/2-y_off-th/2-y-length/2)
			ctx.rotate(3*pi/2)
			ctx.show_text(number)
			ctx.rotate(-3*pi/2)
		elif line[6] == "D":
			ctx.line_to(width/2+x,height/2-length)
			ctx.set_font_size(float(line[8])*1.5)
			x_off, y_off, tw, th = ctx.text_extents(number)[:4]
			ctx.move_to(width/2-x_off-tw/2+x,height/2-y_off-th/2-y+length/2)
			ctx.rotate(3*pi/2)
			ctx.show_text(number)
			ctx.rotate(-3*pi/2)
		elif line[6] == "R":
			ctx.line_to(width/2+x+length,height/2-y)
			ctx.set_font_size(float(line[8])*1.5)
			x_off, y_off, tw, th = ctx.text_extents(number)[:4]
			ctx.move_to(width/2-x_off-tw/2+x+length/2,height/2-y_off-th/2-y-th)
			ctx.show_text(number)
		elif line[6] == "L":
			ctx.line_to(width/2+x-length,height/2-y)
			ctx.set_font_size(float(line[8])*1.5)
			x_off, y_off, tw, th = ctx.text_extents(number)[:4]
			ctx.move_to(width/2-x_off-tw/2+x-length/2,height/2-y_off-th/2-y-th)
			ctx.show_text(number)

		ctx.stroke()

k = 0
for i in range(len(content)):
	if "DRAW\n" == content[i-1]:	# Drawing area begins
		k = 1
		print("Start of symbol")
	elif "ENDDRAW\n" == content[i]:
		k = 0
		print("End of symbol")
	if k == 1:
#		print(content[i])
		line = content[i].rstrip()	# Removed newline char
		line = line.split(' ') 			# Converts to array
		print(line)
		draw_element(line)

surf.write_to_png(output)

