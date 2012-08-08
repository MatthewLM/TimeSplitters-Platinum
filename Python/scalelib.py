#!/usr/bin/env python2.3
#
#  Automatic Game Scaling and 2D surface library for pygame and OpenGL
#
#  Allows resize of a Window while scaling the game, keeping the aspect ratio.
#
#  Created by Matthew Mitchell on 13/09/2009.
#  Copyright (c) 2009 Matthew Mitchell.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#Import modules
import sys,os,time,httplib2,urllib
import math as maths
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from pygame.font import Font as PygameFont,init
from pygame.image import tostring as image_to_string,load as image_load,save as pygame_save,fromstring as pygame_fromstring
init() #Initialise the font.
from pygame import Rect
from textrect import render_textrect
from ctypes import *
from objc import *
cscalelib = CDLL(os.path.dirname(sys.argv[0]) + "/C++ Extensions/cscalelib.dylib") #Load C++ library
c_2dcoordinate = c_double * 2 #Coordinates for (x,y)
c_3dcoordinate = c_double * 3 #Coordinates for (x,y,z)
c_colour = c_float * 4 #RGBA in array
def c_coordinates(coordinates,type):
	c_array = type * len(coordinates)
	coordinates = [tuple(x) for x in coordinates]
	return c_array(*coordinates)
loadBundle("Scalelib Cocoa Framework",globals(),"/Users/matt/Programming/A computing project - TimeSplitters game/Development/Cocoa Scalelib/Scalelib Cocoa Framework/build/Release/Scalelib Cocoa Framework.framework/") #Load Objective-C library
#Constants
TOP_LEFT = 1
TOP_RIGHT = 2
BOTTOM_RIGHT = 4
BOTTOM_LEFT = 8
OPTION_MUSIC_VOLUME = 0
OPTION_FULLSCREEN_STARTUP = 1
OPTION_THEME = 2
OPTION_FULLSCREEN_SCALE = 3
OPTION_SOUND_VOLUME = 4
#Key constants
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_5 = 53
KEY_6 = 54
KEY_7 = 55
KEY_8 = 56
KEY_9 = 57
KEY_0 = 48
KEY_Q = 113
KEY_W = 119
KEY_E = 101
KEY_R = 114
KEY_T = 116
KEY_Y = 121
KEY_U = 117
KEY_I = 105
KEY_O = 111
KEY_P = 112
KEY_A = 97
KEY_S = 115
KEY_D = 100
KEY_F = 102
KEY_G = 103
KEY_H = 104
KEY_J = 106
KEY_K = 107
KEY_L = 108
KEY_Z = 122
KEY_X = 120
KEY_C = 99
KEY_V = 118
KEY_B = 98
KEY_N = 110
KEY_M = 109
KEY_UP = 63232
KEY_RIGHT = 63235
KEY_DOWN = 63233
KEY_LEFT = 63234
KEY_SPACE = 32
KEY_BACKSPACE = 127
KEY_DELETE = 63272
KEY_ENTER = 13
KEY_ESCAPE = 27
KEY_TAB = 9
#Event constants
MOUSEMOTION = 0
MOUSEUP = 1
MOUSEDOWN = 2
KEYDOWN = 3
LEFT_MOUSE_BUTTON = 0
arc_factors = ((1.0, 0.0), (0.99984769515639127, 0.017452406437283512), (0.99939082701909576, 0.034899496702500969), (0.99862953475457383, 0.052335956242943835), (0.9975640502598242, 0.069756473744125302), (0.99619469809174555, 0.087155742747658166), (0.99452189536827329, 0.10452846326765347), (0.99254615164132198, 0.12186934340514748), (0.99026806874157036, 0.13917310096006544), (0.98768834059513777, 0.15643446504023087), (0.98480775301220802, 0.17364817766693033), (0.98162718344766398, 0.1908089953765448), (0.97814760073380569, 0.20791169081775934), (0.97437006478523525, 0.224951054343865), (0.97029572627599647, 0.24192189559966773), (0.96592582628906831, 0.25881904510252074), (0.96126169593831889, 0.27563735581699916), (0.95630475596303544, 0.29237170472273677), (0.95105651629515353, 0.3090169943749474), (0.94551857559931685, 0.3255681544571567), (0.93969262078590843, 0.34202014332566871), (0.93358042649720174, 0.35836794954530027), (0.92718385456678742, 0.37460659341591201), (0.92050485345244037, 0.39073112848927377), (0.91354545764260087, 0.40673664307580021), (0.90630778703664994, 0.42261826174069944), (0.89879404629916704, 0.4383711467890774), (0.8910065241883679, 0.45399049973954675), (0.88294759285892699, 0.46947156278589081), (0.87461970713939574, 0.48480962024633706), (0.86602540378443871, 0.49999999999999994), (0.85716730070211233, 0.51503807491005416), (0.84804809615642596, 0.5299192642332049), (0.83867056794542405, 0.54463903501502708), (0.82903757255504162, 0.5591929034707469), (0.8191520442889918, 0.57357643635104605), (0.80901699437494745, 0.58778525229247314), (0.79863551004729283, 0.60181502315204827), (0.7880107536067219, 0.61566147532565829), (0.7771459614569709, 0.62932039104983739), (0.76604444311897812, 0.64278760968653925), (0.75470958022277201, 0.65605902899050728), (0.74314482547739424, 0.66913060635885824), (0.73135370161917046, 0.68199836006249848), (0.71933980033865119, 0.69465837045899725), (0.70710678118654757, 0.70710678118654746), (0.70710678118654746, 0.70710678118654757), (0.69465837045899725, 0.71933980033865119), (0.68199836006249848, 0.73135370161917046), (0.66913060635885824, 0.74314482547739424), (0.65605902899050728, 0.75470958022277201), (0.64278760968653925, 0.76604444311897812), (0.62932039104983739, 0.7771459614569709), (0.61566147532565829, 0.7880107536067219), (0.60181502315204827, 0.79863551004729283), (0.58778525229247314, 0.80901699437494745), (0.57357643635104605, 0.8191520442889918), (0.5591929034707469, 0.82903757255504162), (0.54463903501502708, 0.83867056794542405), (0.5299192642332049, 0.84804809615642596), (0.51503807491005416, 0.85716730070211233), (0.49999999999999994, 0.86602540378443871), (0.48480962024633706, 0.87461970713939574), (0.46947156278589081, 0.88294759285892699), (0.45399049973954675, 0.8910065241883679), (0.4383711467890774, 0.89879404629916704), (0.42261826174069944, 0.90630778703664994), (0.40673664307580021, 0.91354545764260087), (0.39073112848927377, 0.92050485345244037), (0.37460659341591201, 0.92718385456678742), (0.35836794954530027, 0.93358042649720174), (0.34202014332566871, 0.93969262078590843), (0.3255681544571567, 0.94551857559931685), (0.3090169943749474, 0.95105651629515353), (0.29237170472273677, 0.95630475596303544), (0.27563735581699916, 0.96126169593831889), (0.25881904510252074, 0.96592582628906831), (0.24192189559966773, 0.97029572627599647), (0.224951054343865, 0.97437006478523525), (0.20791169081775934, 0.97814760073380569), (0.1908089953765448, 0.98162718344766398), (0.17364817766693033, 0.98480775301220802), (0.15643446504023087, 0.98768834059513777), (0.13917310096006544, 0.99026806874157036), (0.12186934340514748, 0.99254615164132198), (0.10452846326765347, 0.99452189536827329), (0.087155742747658166, 0.99619469809174555), (0.069756473744125302, 0.9975640502598242), (0.052335956242943835, 0.99862953475457383), (0.034899496702500969, 0.99939082701909576), (0.017452406437283512, 0.99984769515639127), (0.0, 1.0))
#Functions
def find_angle(dy,dx): #Find angle from dx and dy
	if dx == 0: #Can't divide by 0
		angle = 1.5707963267948966 #Should be pi/2 radians or 90 degrees
		if dy > 0:
			angle = -angle
	else:
		angle = maths.atan(float(dy)/float(dx))  #Find angle of line
	return angle
def find_bearing(dx,dy): #Finds the angle relative to an angle pointing up
	if dy == 0: #Can't divide by 0
		angle = 1.5707963267948966 #Should be pi/2 radians or 90 degrees
		if dx < 0:
			angle = -angle
	else:
		angle = maths.atan(float(dx)/float(dy))  #Find angle of line
	if dy < 0:
		return -angle
	else:
		return 3.141592653589793 - angle
def get_resolution(ss,gs):
	gap = float(gs[0]) / float(gs[1])
	sap = float(ss[0]) / float(ss[1])
	if gap > sap:
		#Game aspect ratio is greater than screen (wider) so scale width
		factor = float(gs[0]) /float(ss[0])
		new_h = gs[1]/factor #Divides the height by the factor which the width changes so the aspect ratio remians the same.
		game_scaled = (ss[0],new_h)
	elif gap < sap:
		#Game aspect ratio is less than the screens.
		factor = float(gs[1]) /float(ss[1])
		new_w = gs[0]/factor #Divides the width by the factor which the height changes so the aspect ratio remians the same.
		game_scaled = (new_w,ss[1])
	else:
		game_scaled = ss
	return (int(game_scaled[0]),int(game_scaled[1]))
def gaussian_blur(*args):
	pass
def smooth_polygon_edges(coordinates,radius): #Rounds a list of polygon coordinates with a given radius.
	new_coordinates = []
	for x in xrange(len(coordinates)):
		b = coordinates[x]
		if x == 0:
			a = coordinates[len(coordinates) - 1]
			c = coordinates[x+1]
		else:
			a = coordinates[x - 1]
			if x == len(coordinates) - 1:
				c = coordinates[0]
			else:
				c = coordinates[x+1]
		ba_angle = find_bearing(a[0]-b[0],a[1]-b[1])
		bc_angle =  find_bearing(c[0]-b[0],c[1]-b[1])
		angle = bc_angle - ba_angle #Angle between the two angles
		if abs(angle) > 3.141592653589793:
			angle = 6.2831853072 - angle
			changed = True
		else:
			changed = False
		d = radius/maths.tan(angle/2.) #Work out distance for tangents
		if ba_angle > bc_angle:
			d = -d
		h = (radius**2 + d**2)**0.5 #hypotenuse for the radius/tangent right angled triangle
		b1 =  (b[0] + maths.sin(ba_angle)*d,b[1] - maths.cos(ba_angle)*d)
		b2 = (b[0] + maths.sin(bc_angle)*d,b[1] - maths.cos(bc_angle)*d)
		centre_angle = (ba_angle + bc_angle)/2
		if changed:
			centre_angle += 3.141592653589793
		centre = (b[0]+maths.sin(centre_angle)*h,b[1]-maths.cos(centre_angle)*h)
		angle1 = find_bearing(b1[0] - centre[0],b1[1] - centre[1])
		angle2 = find_bearing(b2[0] - centre[0],b2[1] - centre[1])
		new_coordinates += draw_corner_arc(angle1,angle2,centre,radius)
	return new_coordinates
def draw_corner_arc(angle1,angle2,centre,radius):
	new_coordinates = []
	if angle1 > angle2:
		if angle1 - angle2 > 3.141592653589793:
			return draw_corner_arc(-6.2831853072 + angle1,angle2,centre,radius)
		while angle1 > angle2:
			new_coordinates.append((centre[0] + maths.sin(angle1) * radius,centre[1] - maths.cos(angle1) * radius))
			angle1 -= 0.01
	else:
		while angle1 < angle2:
			if angle2 - angle1 > 3.141592653589793:
				return draw_corner_arc(angle1,-6.2831853072 + angle2,centre,radius)
			new_coordinates.append((centre[0] + maths.sin(angle1) * radius,centre[1] - maths.cos(angle1) * radius))
			angle1 += 0.01
	return new_coordinates
def create_texture(surface):
	surface.texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, surface.texture) #Binds the current 2D texture to the texture to be drawn
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.surface_size[0], surface.surface_size[1], 0, GL_RGBA,GL_UNSIGNED_BYTE, surface.data) #Put surface pixel data into texture
	if surface.data is None:
		setup_framebuffer(surface)
		c = [float(sc)/255.0 for sc in surface.colour] #Divide colours by 255 because OpenGL uses 0-1
		if surface.background_alpha != None:
			c[3] = float(surface.background_alpha)/255.0
		glClearColor(*c)
		glClear(GL_COLOR_BUFFER_BIT)
		end_framebuffer()
	Surface.texture_ready.append(surface)
def load_image_texture(path):
	tex = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, tex)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	img = image_load(path)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0, GL_RGBA,GL_UNSIGNED_BYTE, image_to_string(img, "RGBA")) 
	return [tex,img.get_width(),img.get_height()]
def open_image(path):
	tex_data = load_image_texture(path)
	surf = Surface((tex_data[1],tex_data[2]))
	surf.texture = tex_data[0]
	return surf
def save_image(surf,path):
	setup_framebuffer(surf)
	pygame_save(pygame_fromstring(glReadPixels(0,0,surf.get_width(),surf.get_height(),GL_RGBA,GL_UNSIGNED_BYTE), surf.get_size(), "RGBA"),path)
	end_framebuffer()
def add_line(surface,c,a,b,w = 1,antialias = False):
	if (a[0] > 0 and a[1] >0) or (b[0] > 0 and b[1] > 0):
		if surface.__class__ != GameClass: #Only use a frame buffer if the line isn't being drawn to the screen.
			setup_framebuffer(surface)
		glDisable(GL_TEXTURE_2D)
		if antialias:
			glEnable(GL_LINE_SMOOTH) #Enable line smoothing.
		c = [float(sc)/255.0 for sc in c] #Divide colours by 255 because OpenGL uses 0-1
		if len(c) != 4:
			c.append(1) #Add a value for aplha transparency if needed
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity() #Loads model matrix
		glColor4f(*c)
		glLineWidth(w)
		a = list(a)
		b = list(b)
		glBegin(GL_LINES)
		glVertex2f(*a)
		glVertex2f(*b)
		glEnd()
		if antialias:
			glDisable(GL_LINE_SMOOTH) #Disable line smoothing.
		glEnable(GL_TEXTURE_2D)
		if surface.__class__ != GameClass:
			end_framebuffer()
def setup_framebuffer(surface,flip=False):
	#Create texture if not done already
	if surface.texture is None:
		create_texture(surface)
	#Render child to parent
	if surface.frame_buffer is None:
		surface.frame_buffer = int(glGenFramebuffersEXT(1))
	cscalelib.setup_framebuffer(flip,surface.frame_buffer,surface.texture,int(surface._scale[0]),int(surface._scale[1]))
def end_framebuffer():
	cscalelib.end_framebuffer()
def add_lines(surface,c,coordinates,w =1,antialias = True):
	if surface.__class__ == Surface: #Only use a frame buffer if the line isn't being drawn to the screen.
		setup_framebuffer(surface)
	last = None
	glDisable(GL_TEXTURE_2D)
	if antialias:
		glEnable(GL_LINE_SMOOTH) #Enable line smoothing.
	c = [float(sc)/255.0 for sc in c] #Divide colours by 255 because OpenGL uses 0-1
	if len(c) != 4:
		c.append(1) #Add a value for aplha transparency if needed
	glColor4f(*c)
	glLineWidth(w)
	glBegin(GL_LINE_STRIP)
	for coordinate in coordinates: #Loop though the coordinates and draw the lines
		glVertex2f(*coordinate)
	glEnd()
	if antialias:
		glDisable(GL_LINE_SMOOTH) #Disable line smoothing.
	glEnable(GL_TEXTURE_2D)
	if surface.__class__ == Surface: #Only use a frame buffer if the line isn't being drawn to the screen.
		end_framebuffer()
def rotate_coordinate(coordinate,centre,angle):
	dx = coordinate[0] - centre[0] #Remove centre point ordinates so the rotation only applies from this center.
	dy = - coordinate[1] + centre[1] #Remember that the y-axis is flipped with Open GL top low to bottom high
	return (centre[0] + dx*maths.cos(angle) + dy*maths.sin(angle),centre[1] - dy*maths.cos(angle) + dx*maths.sin(angle)) #Rotation trigonometry with the centre point added
def draw_texture(texture,offset,size,a,rounded,sides,angle,point):
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
	start = time.time()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity() #Loads model matrix
	glColor4f(1,1,1,float(a)/255.0)
	glBindTexture(GL_TEXTURE_2D, texture)
	if rounded == 0:
		if angle == 0:
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex2f(*offset) #Top Left
			glTexCoord2f(0.0, 1.0)
			glVertex2f(offset[0],offset[1] + size[1]) #Bottom Left
			glTexCoord2f(1.0, 1.0)
			glVertex2f(offset[0] + size[0],offset[1] + size[1]) #Bottom, Right
			glTexCoord2f(1.0, 0.0)
			glVertex2f(offset[0] + size[0],offset[1]) #Top, Right
			glEnd()
		else:
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex2f(*rotate_coordinate(offset,point,angle)) #Top Left
			glTexCoord2f(0.0, 1.0)
			glVertex2f(*rotate_coordinate((offset[0],offset[1] + size[1]),point,angle)) #Bottom Left
			glTexCoord2f(1.0, 1.0)
			glVertex2f(*rotate_coordinate((offset[0] + size[0],offset[1] + size[1]),point,angle)) #Bottom, Right
			glTexCoord2f(1.0, 0.0)
			glVertex2f(*rotate_coordinate((offset[0] + size[0],offset[1]),point,angle)) #Top, Right
			glEnd()
	else:
		global arc_factors
		arc = [[o*rounded for o in c] for c in arc_factors]
		glBegin(GL_POLYGON)
		if sides & 1:
			for c in arc:
				coordinates = (offset[0] + rounded - c[0],offset[1] + rounded - c[1])
				glTexCoord2f((coordinates[0]-offset[0])/size[0],(coordinates[1]-offset[1])/size[1])
				glVertex2f(*coordinates)
		else:
			glTexCoord2f(0.0, 0.0)
			glVertex2f(*rotate_coordinate(offset,point,angle)) #Top Left
		if sides & 2:
			for c in arc[::-1]:
				coordinates = (offset[0] + size[0] - rounded + c[0],offset[1] + rounded - c[1])
				glTexCoord2f((coordinates[0]-offset[0])/size[0],(coordinates[1]-offset[1])/size[1])
				glVertex2f(*coordinates)
		else:
			glTexCoord2f(1.0, 0.0)
			glVertex2f(*rotate_coordinate((offset[0] + size[0],offset[1]),point,angle)) #Top, Right
		if sides & 4:
			for c in arc:
				coordinates = (offset[0] + size[0] - rounded + c[0],offset[1] + size[1] - rounded + c[1])
				glTexCoord2f((coordinates[0]-offset[0])/size[0],(coordinates[1]-offset[1])/size[1])
				glVertex2f(*coordinates)
		else:
			glTexCoord2f(1.0, 1.0)
			glVertex2f(*rotate_coordinate((offset[0] + size[0],offset[1] + size[1]),point,angle)) #Bottom, Right
		if sides & 8:
			for c in arc[::-1]:
				coordinates = (offset[0] + rounded - c[0],offset[1] + size[1] - rounded + c[1])
				glTexCoord2f((coordinates[0]-offset[0])/size[0],(coordinates[1]-offset[1])/size[1])
				glVertex2f(*coordinates)
		else:
			glTexCoord2f(0.0, 1.0)
			glVertex2f(*rotate_coordinate((offset[0],offset[1] + size[1]),point,angle)) #Bottom Left
		glEnd()
def texture_to_texture(target,surface,offset,rounded,rotation,point):
	if target.__class__ == LargeImg:
		if surface.texture is None:
			create_texture(surface)
		c1 = offset[0]
		r1 = offset[1]
		c2 = offset[0] + surface.get_width()
		r2 = offset[1] + surface.get_height()
		sides = [(c1,r1),(c1,r2),(c2,r2),(c2,r1)]
		done_cr = []
		for side in sides:
			c = side[0] / 1000
			r = side[1] / 1000
			if (c,r) not in done_cr: #Texture not done yet and a side is in it.
				cscalelib.setup_framebuffer(False,target.fb_array[c][r],target.img_array[c1][r1],target._scale[0],target._scale[1])
				draw_texture(surface.texture,(side[0] % 1000,side[1] % 1000),surface._scale,surface.colour[3],rounded,surface.rounded_sides,rotation,point)
				end_framebuffer()
				done_cr.append((c,r))
	elif surface.__class__ == LargeImg:
		print "drawing LargeImg to surface target"
		setup_framebuffer(target)
		zoom = float(surface._scale[0]) / surface.surface_size[0]
		for c in xrange(surface.w_num):
			if c + 1 == surface.w_num:
				width = surface.w_end
			else:
				width = 1000
			for r in xrange(surface.h_num):
				if r + 1 == surface.h_num:
					height = surface.h_end
				else:
					height = 1000
				draw_texture(surface.img_array[c][r],(offset[0] + c * 999 * zoom,offset[1] + r * 999 * zoom),(width*zoom,height*zoom),surface.colour[3],0,False,rotation,point)
		end_framebuffer()
	else:
		#Create texture if not done already
		if surface.texture is None:
			create_texture(surface)
		#Render child to parent
		setup_framebuffer(target)
		draw_texture(surface.texture,offset,surface._scale,surface.colour[3],rounded,surface.rounded_sides,rotation,point)
		end_framebuffer()
def texture_to_screen(surface,offset,rotation,point):
	if surface.__class__ == LargeImg:
		zoom = float(surface._scale[0]) / surface.surface_size[0]
		for c in xrange(surface.w_num):
			if c + 1 == surface.w_num:
				width = surface.w_end
			else:
				width = 1000
			for r in xrange(surface.h_num):
				if r + 1 == surface.h_num:
					height = surface.h_end
				else:
					height = 1000
				draw_texture(surface.img_array[c][r],(offset[0] + c * 999 * zoom,offset[1] + r * 999 * zoom),(width*zoom,height*zoom),surface.colour[3],0,False,rotation,point)
	else:
		if surface.texture is None:
			create_texture(surface)
		draw_texture(surface.texture,offset,surface._scale,surface.colour[3],surface.rounded,surface.rounded_sides,rotation,point)
def fix_colour(colour):
	if len(colour) < 4:
		colour = list(colour)
		colour.append(255)
	return colour
class Particles():
	def __init__(self,coordinates,size,colour,surface=None):
		glDisable(GL_TEXTURE_2D)
		colour = [float(c)/255. for c in fix_colour(colour)]
		if surface != None:
			setup_framebuffer(surface)
		glColor4f(*colour)
		if size < 60:
			glPointSize(size)
			glBegin(GL_POINTS)
			for position in coordinates:
				glVertex2f(*position)
			glEnd()
		else:
			size /= 2.
			for position in coordinates:
				glBegin(GL_POLYGON)
				for point in arc_factors:
					glVertex2f(position[0] + point[0] * size,position[1] + point[1] * size)
				for point in arc_factors:
					glVertex2f(position[0] - point[1] * size,position[1] + point[0] * size)
				for point in arc_factors:
					glVertex2f(position[0] - point[0] * size,position[1] - point[1] * size)
				for point in arc_factors: 
					glVertex2f(position[0] + point[1] * size,position[1] - point[0] * size)
				glEnd()
		if surface != None:
			end_framebuffer()
		glEnable(GL_TEXTURE_2D)
def Polygon(coordinates,colour,surface=None):
	if surface.__class__ == LargeImg:
		width_height_lists = zip(*coordinates)
		large_img = surface
		min_wh = (min(width_height_lists[0]),min(width_height_lists[1]))
		surface = Surface((max(width_height_lists[0])-min_wh[0],max(width_height_lists[1])-min_wh[1]))
		surface.set_background_alpha(0)
	glDisable(GL_TEXTURE_2D)
	colour = [float(c)/255. for c in fix_colour(colour)]
	if surface != None:
		setup_framebuffer(surface)
	glColor4f(*colour)
	glBegin(GL_POLYGON)
	for position in coordinates:
		glVertex2f(*position)
	glEnd()
	if surface != None:
		end_framebuffer()
	glEnable(GL_TEXTURE_2D)
	if surface.__class__ == LargeImg:
		surface.blit(surface,min_wh)
def create_callback(function):
	callback = Section.alloc().init().set_section(function)
	callback.retain() #Don't delete callback
	return callback
drawable_3d_items = []
def draw_3d_items():
	for drawable_3d_item in drawable_3d_items:
		drawable_3d_item.draw()
def draw_rectangle(vertices,colour):
	cscalelib.draw_rectangle(c_coordinates(vertices,c_3dcoordinate),c_colour(*colour))
class Rectangle():
	def __init__(self,vertices,texture,tex_w,tex_h,colour = (1,1,1,1)):
		self.texture = texture
		self.display_list = cscalelib.make_rectangle(c_coordinates(vertices,c_3dcoordinate),c_double(tex_w),c_double(tex_h),c_colour(*colour))
		drawable_3d_items.append(self)
	def draw(self):
		cscalelib.draw_list(self.display_list,self.texture)
'''
May be used in the future
class Circle():
	def __init__(centre,radius,texture,texture_radius,colour = (1,1,1,1)):
		self.texture = load_image_texture(texture)[0]
		self.display_list = cscalelib.make_circle(c_3dcoordinate(centre),c_double(radius),c_double(texture_radius),c_colour(*colour))
		drawable_3d_items.append(self)
	def draw(self):
		cscalelib.draw_list(self.display_list,self.texture)'''
class Surface():
	texture_ready = []
	def __init__(self,size,extra = None):
		self._offset = (0,0)
		self.children = []
		self.blitted = False
		self.last_offset = [0,0]
		self.surface_size = list(size)
		self.colour = [0,0,0,255]
		self.data = None
		self.rounded = 0
		self.parent = None
		self.parent_offset = (0,0)
		self.texture = None
		self.frame_buffer = None
		self._scale = size
		self.background_alpha = None
		self.rounded_sides = 0
	def blit(self,surface,offset,rotation = 0,point = (0,0)):
		texture_to_texture(self,surface,offset,surface.rounded,rotation,point)
		if surface not in self.children:
			self.children.append(surface)
		if surface.parent_offset != offset or not surface.blitted:
			surface.parent_offset = offset
			surface._offset = [offset[0] + self._offset[0],offset[1] + self._offset[1]]
			surface.recursive_offset_change() #Add to the children's offsets
			surface.blitted = True
	def set_background_alpha(self,alpha):
		self.background_alpha = float(alpha)/255.0
	def recursive_offset_change(self):
		for child in self.children:
			child._offset = (self._offset[0] + child.parent_offset[0],self._offset[1] + child.parent_offset[1])
			child.recursive_offset_change()
	def get_offset(self):
		return self._offset
	def fill(self,colour):
		colour = fix_colour(colour)
		self.children = []
		self.textures = []
		self.colour = colour
		if self.texture != None:
			glDeleteTextures([self.texture])
			self.data = None
			create_texture(self)
	def get_size(self):
		return self.surface_size
	def get_width(self):
		return self.surface_size[0]
	def get_height(self):
		return self.surface_size[1]
	def round_corners(self,r,sides = 15):
		self.rounded = r
		self.rounded_sides = sides
	def get_rect(self):
		return Rect(self._offset,self.surface_size)
	def scale(self,scale):
		self._scale = scale
		return self
	def __del__(self):
		if self.texture != None:
			glDeleteTextures([self.texture])
		if self.frame_buffer != None:
			glDeleteFramebuffersEXT(1, [int(self.frame_buffer)])
class LargeImg(Surface):
	def __init__(self,image):
		self.parent_offset = (None,None)
		self.blitted = True
		self.rounded = 0
		self.colour = [0,0,0,255]
		self._offset = (0,0)
		self.children = []
		self.blitted = False
		self.last_offset = [0,0]
		img = image_load(image)
		self.surface_size = img.get_size()
		self._scale = self.surface_size
		self.w_num = (self.surface_size[0] + 99)/1000
		self.h_num = (self.surface_size[1] + 99)/1000
		self.w_end = self.surface_size[0] % 1000
		if self.w_end == 0:
			self.w_end = 1000
		self.h_end = self.surface_size[1] % 1000
		if self.h_end == 0:
			self.h_end = 1000
		self.img_array = []
		self.fb_array = []
		for x in xrange(self.w_num):
			height_array = []
			fb_height_array = []
			if x+1 == self.w_num:
				width = self.w_end
			else:
				width = 1000
			for y in xrange(self.h_num):
				if y+1 == self.h_num:
					height = self.h_end
				else:
					height = 1000
				texture = glGenTextures(1)
				height_array.append(texture)
				fb_height_array.append(glGenFramebuffersEXT(1))
				glBindTexture(GL_TEXTURE_2D, texture) #Binds the current 2D texture to the texture to be drawn
				glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
				glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) #Required to be set for maping the pixel data
				glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) #Similar as above
				glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,GL_UNSIGNED_BYTE,image_to_string(img.subsurface(Rect(x*1000, y*1000,width,height)), "RGBA")) #Put pixel data into texture
			self.img_array.append(height_array)
			self.fb_array.append(fb_height_array)
	def fill(self,c):
		pass
	def round_corners(self,r,s=None):
		pass
	def set_background_alpha(self,a):
		pass
	def __del__(self):
		for c in self.img_array:
			glDeleteTextures(c)
		for c in self.fb_array:
			for fb in c:
				glDeleteFramebuffersEXT(1, [int(fb)])
class Font():
	def __init__(self,font,size):
		self.size = size
		self.font = PygameFont(os.path.dirname(sys.argv[0]) + "/fonts/" + font + ".ttf",size)
	def return_surface(self,label):
		surface = Surface(label.get_size())
		surface.data = image_to_string(label, "RGBA")
		return surface
	def render(self,text,colour):
		colour = fix_colour(colour)
		label = self.font.render(text, True, colour)
		return self.return_surface(label)
	def render_wordwrap(self,text,width,colour,alignment):
		label = render_textrect(text, self.font, width, colour, alignment)
		return self.return_surface(label)
from Foundation import *
class HTTPRequestThread(httplib2.Http):
	def __init__(self,url,data,timeout):
		httplib2.Http.__init__(self,None,timeout)
		self.url = url
		self.data = data
		self.response_number = 0
		self.details = ""
		self.t = Thread(self.run)
	def run(self):
		for key, string in self.data.items():
			self.data[key] = string.encode('utf-8')
		encoded_data = urllib.urlencode(self.data)
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		self.details, self.content = self.request(self.url,"POST",headers=headers,body=encoded_data)
		self.response_number = self.details['status']
	def isAlive(self):
		return self.t.alive
class ObjCThread(PyCocoaThread):
	def init(self,func,args,time):
		self = super(PyCocoaThread, self).init()
		self.time = time
		self.func = func
		self.args = args
		self.alive = False
		print "Thread init"
		self.start()
		return self
	def run(self):
		print "Thread run"
		time.sleep(self.time)
		self.alive = True
		self.func(*self.args)
		self.alive = False
		print "Thread end"
	def isAlive(self):
		return self.alive
def Thread(func,args = (),time = 0):
	return ObjCThread.alloc().init(func,args,time)
class Section(NSObject):
	def set_section(self,python_object): #Python initialisation of class, add the callback function and arguments
		self.section = python_object
		return self
	@signature("v@:")
	def initialise(self):
		self.section.init()
	@signature("v@:")
	def loop(self): #Used by Objective-C to call python function
		self.section.loop()
	def transfer(self,args):
		self.section.transfer(*args)
	def __del__(self):
		self.release()
class GameClass(ObjCGame):
	#Python interface to Cocoa
	homedir = os.path.expanduser("~")
	instance = None
	def minimise(self,bool):
		self.minimise_(bool)
	@signature("@@:")
	def getExecDir(self):
		return os.path.dirname(sys.argv[0]) 
	@signature("v@:")
	def setInstance(self):
		GameClass.instance = self
	@signature("i@:")
	def pyGetVol(self):
		if len(sys.argv) > 1:
			if sys.argv[1] == "-m":
				return 0
		return self.options[OPTION_SOUND_VOLUME]
	def play_sound(self,file):
		if len(sys.argv) > 1:
			if sys.argv[1] == "-m":
				return
		self.playSound_Volume_(os.path.dirname(sys.argv[0]) + file,self.options[OPTION_SOUND_VOLUME])
	def get_fps(self):
		return self.getFPS()
	def enter_fullscreen(self):
		self.enterFullScreen()
	def set_section(self,section):
		self.setSection_(section)
	def get_section(self,x):
		return self.getSection_(x)
	def get_fade(self):
		return self.getFade()
	def add_section(self,section_object):
		self.addSection_(create_callback(section_object))
	def set_music_volume(self,volume):
		self.setVolume_(volume)
	@signature("v@:@")
	def pyPlayMusic_(self,section):
		if len(sys.argv) > 1:
			if sys.argv[1] == "-m":
				return
		self.playMusic_Volume_(os.path.dirname(sys.argv[0]) + section.section.music,self.options[OPTION_MUSIC_VOLUME])
	def transfer_section(self,section,args=()):
		self.args = args
		self.transferSetup_(section)
	@signature("v@:")
	def transfer(self):
		self.getCurrentSection().transfer(self.args)
	def track_mouse(self,track = True):
		self.trackMouse_(track)
	def get_latest_key(self):
		return self.getLatestKey()
	def get_width(self):
		return self.getWidth()
	def get_height(self):
		return self.getHeight()
	def fade_screen(self):
		return self.getFadeScreen()
	def set_fade_screen(self,boolean):
		self.setFadeScreen_(boolean)
	def unfade(self):
		self.getUnFade()
	def key(self,key):
		return self.key_(key)
	def is_fullscreen(self):
		return self.isFullScreen()
	def mouse_pos(self):
		return (self.getMousePosX(),self.getMousePosY())
	def game_scaled(self):
		return (self.getGameScaledX(),self.getGameScaledY())
	def enable_mouse(self):
		self.enableMouse()
	def show_cursor(self,show = True):
		self.showCursor_(show)
	def disable_mouse(self):
		self.disableMouse()
	def engage_2d(self):
		self.engage2d()
	def engage_3d(self,angle,near,far):
		self.engage3dViewingAngle_Near_Far_(angle,near,far)
	def set_icon_folder_file(self,target,icon):
		NSWorkspace.sharedWorkspace().setIcon_forFile_options_(NSImage.alloc().initWithContentsOfFile_(icon),target,0)
	def modify_background_colour(self,r,g,b,a):
		self.modifyClearColourR_G_B_A_(r,g,b,a)
	@signature("v@:@")
	def exception_(self,trace):
		traceback.print_tb(trace)
		NSApplication.sharedApplication().terminate_(None) #Accept no errors
	@signature("v@:@")
	def pyEventKeyDown_(self,characters):
		self.events.append((KEYDOWN,characters))
	@signature("v@:i")
	def pyMouseUp_(self,side):
		pos = self.mouse_pos()
		self.events.append((MOUSEUP,side,pos[0],pos[1]))
	@signature("v@:i")
	def pyMouseDown_(self,side):
		pos = self.mouse_pos()
		self.events.append((MOUSEDOWN,side,pos[0],pos[1]))
	@signature("v@:ii")
	def pyMouseMoveX_Y_(self,dx,dy):
		for event in self.events:
			if event[0] == MOUSEMOTION:
				event[1] += dx
				event[2] -= dy
				break
		else:
			self.events.append([MOUSEMOTION,dx,-dy])
	@signature("v@:")
	def removeEvents(self):
		self.events = []
	def blit(self,surface,offset,rotation = 0,point = (0,0)):
		if surface.get_offset() != offset or not surface.blitted:
			surface._offset = offset
			surface.recursive_offset_change() #Add to the children's offsets
		surface.blitted = True
		texture_to_screen(surface,offset,rotation,point)
def Game(title,size):
	return GameClass.alloc().initWithTitle_Width_Height_(title,size[0],size[1])
import traceback