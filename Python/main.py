#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#
#  main.py
#
#  Created by Matthew Mitchell on 15/09/2009.
#  Copyright © 2009 Matthew Mitchell. All rights reserved.
#  Do not, under any circumstances, send requests to the urls listed in this program without using this program in it's unmodified form or without permission from the author.
#
TSPVERSION = [0,0,5] #Version 0.0.5 Pre-Alpha 5
#Import modules
from scalelib import *
import os,random,sys,getpass,time,webbrowser,copy,zlib
from menulib import *
from cStringIO import StringIO
import math as maths
import cPickle as pickle
from PIL import Image
cmain = CDLL(os.path.dirname(sys.argv[0]) + "/C++ Extensions/cmain.dylib") #Load C++ library
#Constants
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_FORWARD = 4
ACTION_BACKWARD = 8
ACTION_LEFT_SIDE = 16
ACTION_RIGHT_SIDE = 32
ACTION_FIRE = 64
ACTION_RELOAD = 128
ACTION_SWITCH = 256
DECISION_LEFT = 0
DECISION_RIGHT = 1
DECISION_FORWARD = 2
DECISION_BACKWARD = 3
DECISION_LEFT_SIDE = 4
DECISION_RIGHT_SIDE = 5
DECISION_FIRE = 6
DECISION_RELOAD = 7
DECISION_SWITCH = 8
ITEM_ID = 0
ITEM_POS = 1
ITEM_DATA = 2
ITEM_IMG = 3
ITEM_FLOOR = 4
MMS_NO_IMG = 0
MMS_NEW_IMG = 1
MMS_NAV = 2
MMS_DRAG = 3
MMS_WALL = 4
MMS_ITEMS = 5
MMS_FLOOR_TOOLS = 6
MMS_STAIRS = 7
MMS_STAIRS_PARALLEL = 8
MMS_HOLE = 9
MMS_TRANSPARENT = 10
MMS_OPTIONS = 11
MMS_OPEN = 12
MMS_SAVE = 13
MMS_PREVIEW = 14
EXPLOSION_POS = 0
EXPLOSION_TIME = 1
EXPLOSION_FLOOR = 2
ALONG_LINE = 0
FROM_LINE = 1
LINE_INTERSECT = 2
POINT_LINE_VECTOR = 3
GOING_UP = 0
GOING_DOWN = 1
FALL_HOLE = 0
FALL_STAGE = 1
FALL_ALTITUDE = 2
FALL_SPEED = 3
HOLE_SLIDE = 0
FREEFALL = 1
MODE_PREVIEW = 0
MODE_DEATHMATCH = 1
MODE_ELIMINATION = 2
ELIM_LIVES = 0
DEATHMATCH_SUICIDES = 0
DEATHMATCH_DEATHS = 1
DEATHMATCH_TIME = 2
DEATHMATCH_SCORE = 3
CONTROLS_TURNING_MODE = 0
MOUSE_TURNING = 0
KEYBOARD_TURNING = 1
CONTROLS_ROTATION_MODE = 1
LEVEL_ROTATION = 0
PLAYER_ROTATION = 1
CONTROLS_KEYBOARD_FORWARD = 2
CONTROLS_KEYBOARD_BACKWARD = 3
CONTROLS_KEYBOARD_STRAFE_LEFT = 4
CONTROLS_KEYBOARD_STRAFE_RIGHT = 5
CONTROLS_KEYBOARD_TURN_LEFT = 6
CONTROLS_KEYBOARD_TURN_RIGHT = 7
CONTROLS_KEYBOARD_FIRE = 8
CONTROLS_KEYBOARD_SWITCH = 9
CONTROLS_KEYBOARD_RELOAD = 10
CONTROLS_KEYBOARD_PAUSE = 11
CONTROLS_MOUSE_FORWARD = 12
CONTROLS_MOUSE_BACKWARD = 13
CONTROLS_MOUSE_STRAFE_LEFT = 14
CONTROLS_MOUSE_STRAFE_RIGHT = 15
CONTROLS_MOUSE_SWITCH = 16
CONTROLS_MOUSE_RELOAD = 17
CONTROLS_MOUSE_PAUSE = 18
ORDER_MAPS_NAME = 0
ORDER_MAPS_ESTABLISH = 1
ORDER_MAPS_LAST_EDIT = 2
ORDER_MAPS_PLAYS = 3
ORDER_MAPS_LAST_PLAY = 4
CURLING_DIRECTION = 0
CURLING_POWER = 1
CURLING_SPIN = 2
CURLING_MOVE = 3
CURLING_SCORE = 4
CURLING_GAME_OVER = 5
MONKEY_X = 0
MONKEY_Z = 1
MONKEY_SPEED = 2
MONKEY_DIRECTION = 3
#Menu events
OPTTOG = 0
CONTROLS = 1
BLOG = 2
LOGOUT = 3
ANDREW = 4
ANDREWFFF = 5
RESUME = 6
END_GAME = 7
NAMEMAPS = 8
DATENEWMAPS = 9
DATEOLDMAPS = 10
EDITNEWMAPS = 11
EDITOLDMAPS = 12
PLAYSMOSTMAPS = 13
PLAYSLEASTMAPS = 14
LASTPLAYRECENTMAPS = 15
LASTPLAYLONGESTMAPS = 16
L = 17
MAPRETURN = 18
DEATHMATCH = 19
TEAMDEATHMATCH = 20
ELIMINATION = 21
TEAMELIMINATION = 22
DONEGAMEOPTS = 23
def point_collide(pos,surface):
	return surface.get_rect().collidepoint((pos[0],pos[1]))
def get_mouse_pos(pos):
	game_scaled = game.game_scaled()
	return (pos[0] * (1280.0/float(game_scaled[0])),pos[1] * (720.0/float(game_scaled[1])))
def website(address):
	if game.is_fullscreen():
		game.exit_fullscreen = True
	game.minimise(True)
	webbrowser.open_new_tab(address)
def update_options():
	options_file = open(game.homedir + "/.timesplitters_platinum/options.sav","wb")
	pickle.dump(game.options,options_file,2)
	options_file.close()
def update_controls():
	controls_file = open(game.homedir + "/.timesplitters_platinum/controls.sav","wb")
	pickle.dump(game.controls,controls_file,2)
	controls_file.close()
def exit_game():
	game.section.exit()
	sys.exit()
def xintersect(a,b,x):
	if intersect(a,b,x,[x[0]+20,x[1]+20]) or intersect(a,b,[x[0]+20,x[1]],[x[0],x[1]+20]):
		return True
	return False
def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def intersect_point(a,b,c,d): #This somehow returns the point of intersect for the lines ab and dc.
	dx_ab = round(a[0] - b[0],2)
	dx_cd = round(c[0] - d[0],2)
	if dx_ab != 0:
		ab_grad = float(a[1] - b[1])/float(dx_ab)
		ab_c = a[1] - (a[0] * ab_grad)
	if dx_cd != 0:
		cd_grad = float(c[1] - d[1])/float(dx_cd)
		cd_c = c[1] - (c[0] * cd_grad)
	if dx_ab == 0:
		if dx_cd == 0:
			return None
		else:
			return (a[0],cd_grad*a[0] + cd_c)
	else:
		if dx_cd == 0:
			return (c[0],ab_grad*c[0] + ab_c)
		elif (ab_grad-cd_grad) != 0:
			x = (cd_c-ab_c)/(ab_grad-cd_grad)
			return (x,ab_grad*x + ab_c)
		else:
			return None
def vector_intersection(v1,v2,d1,d2):
	'''
	v1 and v2 - Vector points
	d1 and d2 - Direction vectors
	returns the intersection point for the two vector line equations.
	'''
	if d1[0] == 0 and d2[0] != 0 or d1[1] == 0 and d2[1] != 0:
		if d1[0] == 0 and d2[0] != 0:
			mu = float(v1[0] - v2[0])/d2[0]
		elif d1[1] == 0 and d2[1] != 0:
			mu = float(v1[1] - v2[1])/d2[1]
		return (v2[0] + mu* d2[0],v2[1] + mu * d2[1])
	else:
		if d1[0] != 0 and d1[1] != 0 and d2[0] != 0 and d2[1] != 0:
			if d1[1]*d2[0] - d1[0]*d2[1] == 0:
				raise ValueError('Direction vectors are invalid. (Parallel)')
			lmbda = float(v1[0]*d2[1] - v1[1]*d2[0] - v2[0]*d2[1] + v2[1]*d2[0])/(d1[1]*d2[0] - d1[0]*d2[1])
		elif d2[0] == 0 and d1[0] != 0:
			lmbda = float(v2[0] - v1[0])/d1[0]
		elif d2[1] == 0 and d1[1] != 0:
			lmbda = float(v2[1] - v1[1])/d1[1]
		else:
			raise ValueError('Direction vectors are invalid.')
		return (v1[0] + lmbda* d1[0],v1[1] + lmbda * d1[1])
#######################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                          MAY BE REDUNDANT                                                           #
#                                                                                                                                                     #
#                                                                                                                                                     #
#######################################################################################
def line_point_distances(a,b,p):
	direction_vector = (a[0] - b[0],a[1] - b[1]) #Direction vector last to wall_point
	#This is all vector maths which has been rearanged into fewer expressions
	#t is the factor for the direction vector at which the perpendicular meets the wall from the point
	t = ((-p[0]+b[0])*-direction_vector[0] + (-p[1]+b[1])*-direction_vector[1])/(direction_vector[0]**2 + direction_vector[1]**2)
	perpendicular_intersect = (b[0] + t * direction_vector[0],b[1] + t * direction_vector[1])
	point_intersect_vector = (-p[0]+perpendicular_intersect[0],-p[1]+perpendicular_intersect[1])
	if t < 0: #Closest to last but not perpendicular to line bounds
		d = ((p[0] - b[0])**2+(p[1] - b[1])**2)**0.5
	elif t > 1: #Closest to wall_point but not perpendicular to line bounds
		d = ((p[0] - a[0])**2+(p[1] - a[1])**2)**0.5
	else: #Perpendicular to line bounds, find distance to line using vector maths.
		d = (point_intersect_vector[0]**2 + point_intersect_vector[1]**2)**0.5
	return (t,d,perpendicular_intersect,point_intersect_vector) #Returns distance along and from wall, perpendicular intersect point and point-intersect vector.
#######################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                          END                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
#######################################################################################
def in_square(square,point):
	pos_range = [square[0][0],square[2][0]]
	if pos_range[0] > pos_range[1]:
		temp = pos_range[0]
		pos_range[0] = pos_range[1]
		pos_range[1] = temp
	if point[0] > pos_range[0] and point[0] < pos_range[1]:
		pos_range = [square[0][1],square[2][1]]
		if pos_range[0] > pos_range[1]:
			temp = pos_range[0]
			pos_range[0] = pos_range[1]
			pos_range[1] = temp
		if point[1] > pos_range[0] and point[1] < pos_range[1]:
				return True
	return False
#Classes
class Minigun():
	max_ammo = 400
	mag_size = 0
	goodness = 0.7
	def __init__(self,player,game_session):
		self.stop_fire = False
		self.reloading = False
		self.left = True
		self.is_firing = False
		self.ammo = [400,0]
		self.player = player
		self.game_session = game_session
	def trigger_on(self):
		if not self.is_firing:
			self.stop_fire = False
			Thread(self.fire_func)
	def trigger_off(self):
		self.stop_fire = True
	def reload(self):
		pass
	def fire_func(self):
		self.is_firing = True
		current_weapon = self.player.get_current_weapon()
		while not self.stop_fire and current_weapon[1] == self:
			if self.ammo[0] != 0:
				self.ammo[0] -= 1
				self.game_session.ammochange = True
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/4/fire.ogg")
				if self.left:
					self.game_session.bullet_queue.append(((self.player.character_data.weapon_pos[0]-4,self.player.character_data.weapon_pos[1]),self.player,15,10,5,0))
					self.left = False
				else:
					self.game_session.bullet_queue.append(((self.player.character_data.weapon_pos[0]+4,self.player.character_data.weapon_pos[1]),self.player,15,10,5,0))
					self.left = True
				time.sleep(0.1)
			else:
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/dry.ogg")
				time.sleep(0.1)
		self.is_firing = False
class Shotgun():
	max_ammo = 40
	mag_size = 2
	goodness = 0.7
	def __init__(self,player,game_session):
		self.stop_fire = False
		self.reloading = False
		self.is_firing = False
		self.ammo = [38,2]
		self.player = player
		self.game_session = game_session
	def trigger_on(self):
		if not self.is_firing:
			self.stop_fire = False
			Thread(self.fire_func)
	def trigger_off(self):
		self.stop_fire = True
	def reload(self):
		Thread(self.reload_func)
	def reload_func(self):
		time.sleep(0.3)
		current_weapon = self.player.get_current_weapon()
		if not self.reloading and current_weapon[1] == self and self.ammo[0] != 0:
			self.reloading = True
			if self.player is self.game_session.control_player:
				game.play_sound("/weapons/3/reload.ogg")
			time.sleep(2)
			if current_weapon[1] == self:
				self.ammo[0] -= 2
				self.ammo[1] = 2
				self.game_session.ammochange = True
			self.reloading = False
	def fire_func(self):
		self.is_firing = True
		current_weapon = self.player.get_current_weapon()
		while not self.stop_fire and current_weapon[1] == self:
			if self.ammo[1] != 0:
				self.ammo[1] = 0
				self.game_session.ammochange = True
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/3/fire.ogg")
				self.game_session.bullet_queue.append(((self.player.character_data.weapon_pos[0]-4,self.player.character_data.weapon_pos[1]),self.player,50,45,35,0))
				self.game_session.bullet_queue.append(((self.player.character_data.weapon_pos[0]+4,self.player.character_data.weapon_pos[1]),self.player,50,45,35,0))
				time.sleep(0.2)
				self.reload_func()
			elif self.ammo[0] == 0:
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/dry.ogg")
				time.sleep(0.2)
		self.is_firing = False
class Revolver():
	max_ammo = 78
	mag_size = 6
	goodness = 0.5
	def __init__(self,player,game_session):
		self.stop_fire = False
		self.reloading = False
		self.ammo_list = [6,6,6,6,6,6,6,6,6,6,6,6,6]
		self.current_mag = 0
		self.firing = False
		self.ammo = [72,6]
		self.player = player
		self.game_session = game_session
	def trigger_on(self):
		if not self.firing:
			self.stop_fire = False
			Thread(self.fire_func)
	def trigger_off(self):
		self.stop_fire = True
	def reload(self):
		Thread(self.reload_func)
	def reload_func(self):
		time.sleep(0.3)
		current_weapon = self.player.get_current_weapon()
		if self.ammo_list != [0,0,0,0,0,0,0,0,0,0,0,0,0] and not self.reloading and current_weapon[1] == self:
			self.reloading = True
			if self.player is self.game_session.control_player:
				game.play_sound("/weapons/2/reload.ogg")
			time.sleep(2)
			if current_weapon[1] == self:
				reload_flag = False
				max = 0
				for mag in range(len(self.ammo_list)):
					if self.ammo_list[mag] > max:
						max = self.ammo_list[mag]
						max_mag = mag
				if self.ammo_list[max_mag] > self.ammo_list[self.current_mag]:
					difference = self.ammo_list[max_mag] - self.ammo_list[self.current_mag]
					self.current_mag = max_mag
					reload_flag = True
				if reload_flag:
					self.ammo[1] = self.ammo_list[self.current_mag]
					self.ammo[0] -= difference
					self.game_session.ammochange = True
			self.reloading = False
	def fire_func(self):
		self.firing = True
		current_weapon = self.player.get_current_weapon()
		while not self.stop_fire and current_weapon[1] == self:
			if self.ammo[0] != 0 and self.ammo[1] != 0:
				self.ammo[1] -= 1
				self.ammo_list[self.current_mag] -= 1
				self.game_session.ammochange = True
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/2/fire.ogg")
				self.game_session.bullet_queue.append((self.player.character_data.weapon_pos,self.player,50,45,35,1))
				time.sleep(0.2)
				if self.ammo[1] == 0:
					self.reload_func()
			elif self.ammo[0] == 0:
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/dry.ogg")
				time.sleep(0.2)
			else:
				self.reload_func()
		self.firing = False
class AK47():
	max_ammo = 150
	mag_size = 30
	goodness = 0.5
	def __init__(self,player,game_session):
		self.stop_fire = False
		self.reloading = False
		self.ammo_list = [30,30,30,30,30]
		self.current_mag = 0
		self.is_firing = False
		self.ammo = [120,30]
		self.player = player
		self.game_session = game_session
	def trigger_on(self):
		if not self.is_firing:
			self.stop_fire = False
			Thread(self.fire_func)
	def trigger_off(self):
		self.stop_fire = True
	def reload(self):
		Thread(self.reload_func)
	def reload_func(self):
		time.sleep(0.6)
		current_weapon = self.player.get_current_weapon()
		if self.ammo_list != [0,0,0,0,0] and not self.reloading and current_weapon[1] == self:
			self.reloading = True
			if self.player is self.game_session.control_player:
				game.play_sound("/weapons/1/reload.ogg")
			time.sleep(1.4)
			if current_weapon[1] == self:
				reload_flag = False
				max = 0
				for mag in range(len(self.ammo_list)):
					if self.ammo_list[mag] > max:
						max = self.ammo_list[mag]
						max_mag = mag
				if self.ammo_list[max_mag] > self.ammo_list[self.current_mag]:
					difference = self.ammo_list[max_mag] - self.ammo_list[self.current_mag]
					self.current_mag = max_mag
					reload_flag = True
				if reload_flag:
					self.ammo[1] = self.ammo_list[self.current_mag]
					self.ammo[0] -= difference
					self.game_session.ammochange = True
			self.reloading = False
	def fire_func(self):
		self.is_firing = True
		current_weapon = self.player.get_current_weapon()
		while not self.stop_fire and current_weapon[1] == self:
			if self.ammo[1] != 0:
				self.ammo[1] -= 1
				self.ammo_list[self.current_mag] -= 1
				self.game_session.ammochange = True
				if self.player is self.game_session.control_player:
					game.play_sound("/weapons/1/fire.ogg")
				self.game_session.bullet_queue.append((self.player.character_data.weapon_pos,self.player,20,15,5,0))
				time.sleep(0.1)
			elif not self.reloading:
				if self.ammo[0] != 0:
					self.reload_func()
				else:
					if self.player is self.game_session.control_player:
						game.play_sound("/weapons/dry.ogg")
					time.sleep(0.1)
			else:
				time.sleep(0.1)
		self.is_firing = False
class Unarmed():
	ammo = (0,0)
	def __init__(self,foo,bar):
		'''foobar not used as the whole class is a dummy one'''
		pass
	def trigger_on(self):
		pass
	def trigger_off(self):
		pass
	def reload(self):
		pass
class Monkey():
	weapon_pos = (105, 10)
	armed_collision_coordinates = [(10,59),(21,58),(22,62),(21,65),(34,63),(59,63),(59,60),(67,59),(73,54),(77,54),(82,59),(88,59),(89,62),(92,64),(115,64),(111,55),(111,49),(109,46),(108,37),(101,34),(97,28),(97,20),(95,12),(98,4),(108,3),(114,3),(116,11),(129,18),(135,27),(135,38),(143,46),(146,63),(143,73),(141,82),(136,88),(125,89),(123,91),(97,91),(85,99),(70,99),(65,96),(56,96),(51,92),(45,95),(17,95),(12,92),(10,87),(10,81),(8,78),(8,72),(9,68),(9,61),(10,59)]
	unarmed_collision_coordinates = [(0,0)]
class Player():
	#Players for the game
	spawn_points = []
	available_spawn_points = []
	def __init__(self,player_character,game_session):
		self.character_image_stationed_unarmed = open_image(os.path.dirname(sys.argv[0]) + "/characters/" + str(player_character) + "/stationed_unarmed.png")
		self.character_image_stationed_armed = open_image(os.path.dirname(sys.argv[0]) + "/characters/" + str(player_character) + "/stationed_armed.png")
		self.character_data = character_classes[player_character]()
		self.killed = {}
		self.kills = {}
		self.suicides = 0
		self.game_session = game_session
		self.floor = None
		if game_session.mode == MODE_ELIMINATION:
			self.score = game_session.mode_options[ELIM_LIVES]
		elif game_session.mode == MODE_DEATHMATCH:
			self.score = 0
	def spawn(self):
		self.inventory = [(0,Unarmed(self,self.game_session),None)]
		if len(self.available_spawn_points) == 0:
			self.available_spawn_points = self.spawn_points[:]
		spawn_point = random.randrange(len(self.available_spawn_points))
		self.pos = self.available_spawn_points[spawn_point][ITEM_POS]
		self.floor = self.available_spawn_points[spawn_point][ITEM_FLOOR]
		self.face_angle = 3.141592653589793 - self.available_spawn_points[spawn_point][ITEM_DATA]
		del self.available_spawn_points[spawn_point]
		self.health = 100
		self.armour = 0
		if self == self.game_session.control_player:
			self.game_session.make_health_bar()
			self.game_session.make_armour_bar()
		self.forward_speed = 0
		self.side_speed = 0
		self.collect_weapon(self.game_session.weapon_list[0])
		self.falling = [None,None,0,0]
		self.floor_transition = None
		self.slide_speed = [0,0]
		game.play_sound("/sounds/respawn.mp3")
	def movement_attempt(self,new_pos,goes = 5):
		walls = self.game_session.walls
		if self.falling[FALL_STAGE] != HOLE_SLIDE:
			for wall in walls[self.floor]:
				last = None
				for wall_point in wall:
					if last is not None:
						direction_vector = (wall_point[0] - last[0],wall_point[1] - last[1]) #Direction vector last to wall_point
						#This is all vector maths which has been rearanged into fewer expressions
						#t is the factor for the direction vector at which the perpendicular meets the wall from the point
						t = ((-new_pos[0]+last[0])*-direction_vector[0] + (-new_pos[1]+last[1])*-direction_vector[1])/(direction_vector[0]**2 + direction_vector[1]**2)
						if t < 0: #Closest to last but not perpendicular to line bounds
							vector_to_last = (-new_pos[0] + last[0],-new_pos[1] + last[1])
							d = (vector_to_last[0]**2 + vector_to_last[1]**2)**0.5
							if d < 100:
								self.game_session.particles.append(self.game_session.map_level_to_screen(last))
							p = 0
						elif t > 1: #Closest to wall_point but not perpendicular to line bounds
							vector_to_last = (-new_pos[0] + wall_point[0],-new_pos[1] + wall_point[1])
							d = (vector_to_last[0]**2 + vector_to_last[1]**2)**0.5
							if d < 100:
								self.game_session.particles.append(self.game_session.map_level_to_screen(wall_point))
							p = 1
						else: #Perpendicular to line bounds, find distance to line using vector maths.
							perpendicular_intersect = (last[0] + t * direction_vector[0],last[1] + t * direction_vector[1])
							point_intersect_vector = (-new_pos[0]+perpendicular_intersect[0],-new_pos[1]+perpendicular_intersect[1])
							d = (point_intersect_vector[0]**2 + point_intersect_vector[1]**2)**0.5
							p =  2 #Slide along wall
						if d < 60:
							if goes != 0:
								t = -61/d
								if p == 0:
									self.movement_attempt([last[0] + vector_to_last[0]*t,last[1] + vector_to_last[1]*t],goes - 1)
								elif p == 1:
									self.movement_attempt([wall_point[0] + vector_to_last[0]*t,wall_point[1] + vector_to_last[1]*t],goes - 1)
								elif p == 2:
									self.movement_attempt([perpendicular_intersect[0] + t*point_intersect_vector[0],perpendicular_intersect[1] + t*point_intersect_vector[1]],goes - 1)
							return
					last = wall_point
			back_up = False
		if self.falling[FALL_STAGE] is None:
			for stairs_slope in self.game_session.level.floors[self.floor].connectors:
				if intersect(stairs_slope[0],stairs_slope[1],new_pos,self.pos):
					#Bottom of slope/stairs crossed
					if self.floor_transition is None:
						self.floor_transition = stairs_slope
					else:
						self.floor_transition = None
				if intersect(stairs_slope[2],stairs_slope[3],new_pos,self.pos):
					back_up = True
					self.floor += 1
					self.floor_transition = None
			if not back_up:
				for stairs_slope in self.game_session.level.floors[self.floor - 1].connectors:
					if intersect(stairs_slope[2],stairs_slope[3],new_pos,self.pos):
						#Top of stairs crossed
						self.floor -= 1
						self.floor_transition = stairs_slope
			for hole in self.game_session.level.floors[self.floor].holes:
				for x in xrange(4):
					if intersect(hole[x],hole[0 if x == 3 else x + 1],new_pos,self.pos):
						self.falling = [hole,HOLE_SLIDE,1,0]
						self.slide_speed = [0,0]
						break
		self.pos = new_pos
		if self.falling[FALL_STAGE] == HOLE_SLIDE:
			clear = True
			y_deccelerate = True
			x_deccelerate = True
			for x in xrange(4):
				distances = line_point_distances(self.falling[FALL_HOLE][x],self.falling[FALL_HOLE][0 if x == 3 else x + 1],new_pos)
				if distances[FROM_LINE] < 60:
					#Not clear of line so continue accelerating away from it.
					clear = False
					if distances[POINT_LINE_VECTOR][0] != 0:
						#X difference
						if distances[POINT_LINE_VECTOR][0] > 0:
							self.slide_speed[0] -= 5./game.get_fps()
						else:
							self.slide_speed[0] += 5./game.get_fps()
						x_deccelerate = False
					else:
						#Y difference
						if distances[POINT_LINE_VECTOR][1] > 0:
							self.slide_speed[1] -= 5./game.get_fps()
						else:
							self.slide_speed[1] += 5./game.get_fps()
						y_deccelerate = False
			if clear:
				self.falling[FALL_STAGE] = FREEFALL
				self.floor -= 1
			self.slide_movement(y_deccelerate,x_deccelerate)
	def slide_movement(self,y_deccelerate,x_deccelerate):
		if y_deccelerate:
			if self.slide_speed[1] > 0:
				self.slide_speed[1] -= 8./game.get_fps()
			elif self.slide_speed[1] < 0:
				self.slide_speed[1] += 8./game.get_fps()
			if abs(self.slide_speed[1]) < 0.5:
				self.slide_speed[1] = 0
		if x_deccelerate:
			if self.slide_speed[0] > 0:
				self.slide_speed[0] -= 8./game.get_fps()
			elif self.slide_speed[0] < 0:
				self.slide_speed[0] += 8./game.get_fps()
			if abs(self.slide_speed[0]) < 0.5:
				self.slide_speed[0] = 0
		self.pos[0] += self.slide_speed[0]
		self.pos[1] += self.slide_speed[1]
	def change_weapon(self,pos):
		if self.inventory[pos][0] == 0:
			self.current_weapon = 0
			self.current_upper = self.character_image_stationed_unarmed
			self.current_collision_coordinates = self.character_data.unarmed_collision_coordinates
		else:
			self.current_weapon = pos
			self.current_upper = Surface((self.character_image_stationed_armed.get_width(),self.character_image_stationed_armed.get_height()+self.inventory[pos][2].get_height() - self.character_data.weapon_pos[1]))
			self.current_upper.set_background_alpha(0)
			self.current_upper.blit(self.character_image_stationed_armed,(0,self.inventory[pos][2].get_height() - self.character_data.weapon_pos[1]))
			self.current_upper.blit(self.inventory[pos][2],(self.character_data.weapon_pos[0] - self.inventory[pos][2].get_width()/2,0))
			self.current_collision_coordinates = self.character_data.armed_collision_coordinates
			if self.inventory[pos][1].ammo[1] == 0:
				self.inventory[pos][1].reload()
	def collect_weapon(self,weapon):
		if weapon != 0:
			found = False
			pos = 0
			for weapon_data in self.inventory:
				if weapon_data[0] == weapon:
					found = True
					weapon_data[1] = weapon_classes[weapon - 1](self,self.game_session)
					self.change_weapon(pos)
					break
				pos += 1
			if not found:
				self.inventory.append([weapon,weapon_classes[weapon - 1](self,self.game_session),open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(weapon) + "/wait.png")])
				self.change_weapon(len(self.inventory) - 1)
		else:
			self.change_weapon(0)
	def check_items(self,items): #Checks pickups for weapons and ammo
		for item in items:
			if item[ITEM_DATA] == False and item[ITEM_FLOOR] == self.floor: #item enabled
				if Rect(item[ITEM_POS],item[ITEM_IMG].get_size()).colliderect(Rect((self.pos[0]-50,self.pos[1]-50),(100,100))): #Test is player is over a item by testing if the two rectangles overlap.
					change = True
					if self == self.game_session.control_player:
						if item[ITEM_ID] < 13:
							game.play_sound("/sounds/gun_pickup.mp3")
						else:
							game.play_sound("/sounds/gun_pickup.mp3")
					if item[ITEM_ID] < 8:
						self.collect_weapon(self.game_session.weapon_list[item[ITEM_ID]-3]) #Weapon pickup items start at 3, weapon list starts at 1. Use - 3 to map the two.
					elif item[ITEM_ID] < 13:
						if self.game_session.weapon_list[item[ITEM_ID]-8] in zip(*self.inventory)[0]: #First elements in inventory lists, are the weapon ids.
							self.collect_weapon(self.game_session.weapon_list[weapon[0]-8]) #Ammo pickup items start at 9, weapon list starts at 1. Use - 8 to map the two.
						else:
							change = False #No pickup for ammo as the player doesn't have the weapon
					elif item[ITEM_ID] == 13: #Health Low
						self.health += 50
						if self.health > 100:
							self.health = 100
						if self is self.game_session.control_player:
							self.game_session.make_health_bar()
					elif item[ITEM_ID] == 14: #Health High
						self.health += 99
						if self.health > 100:
							self.health = 100
						if self is self.game_session.control_player:
							self.game_session.make_health_bar()
					elif item[ITEM_ID] == 15: #Armour Low
						self.armour += 50
						if self.armour > 100:
							self.armour = 100
						if self is self.game_session.control_player:
							self.game_session.make_armour_bar()
					elif item[ITEM_ID] == 16: #Armour High
						self.armour += 100
						if self.armour > 100:
							self.armour = 100
						if self is self.game_session.control_player:
							self.game_session.make_armour_bar()
					if change:
						item[ITEM_DATA] = True #Weapon disabled for 30 seconds. Disabling with True is counter intuitive, yes. I can't be bothered to change it.
						Thread(self.enable_pickup,(item,),30)
						self.game_session.ammochange = True
	def damage(self,damage,inflicter):
		pre_armour_change = self.armour
		self.armour -= damage
		if self.armour < 0:
			self.health += self.armour
			self.armour = 0
			if self is self.game_session.control_player:
				self.game_session.make_health_bar()
		if self is self.game_session.control_player and pre_armour_change != self.armour:
			self.game_session.make_armour_bar()
		if self.health <= 0:
			if self.game_session.mode == MODE_ELIMINATION:
				self.score -= 1
				if self.game_session.team_mode:
					self.game_session.team_scores[self.team] -= 1
			elif self.game_session.mode == MODE_DEATHMATCH:
				if self is inflicter:
					if self.game_session.mode_options[DEATHMATCH_SUICIDES]:
						self.score -= 1
						if self.game_session.team_mode:
							self.game_session.team_scores[self.team] -= 1
				else:
					if self.game_session.mode_options[DEATHMATCH_DEATHS]:
						self.score -= 1
						if self.game_session.team_mode:
							self.game_session.team_scores[self.team] -= 1
					if self.game_session.team_mode:
						if self.team != inflicter.team: #Only give points for killing opposite team members
							inflicter.score += 1
							self.game_session.team_scores[inflicter.team] += 1
					else:
						inflicter.score += 1
			if self is inflicter:
				self.suicides += 1
			else:
				if inflicter in self.killed.keys():
					self.killed[inflicter] += 1
				else:
					self.killed[inflicter] = 1
				if self in inflicter.kills.keys():
					inflicter.kills[self] += 1
				else:
					inflicter.kills[self] = 1
			self.inventory[self.current_weapon][1].trigger_off()
			self.spawn()
	def do_actions(self,actions,mouse = False):
		if self.falling[FALL_STAGE] == FREEFALL:
			self.falling[FALL_SPEED] += 3.9/game.get_fps() #Acceleration roughly equivilent to g = 9.8m/s with floor height at 2.5 metres. This acceleration is the rate of floors falling per second. It should take just over a 1.43 seconds to fall from floor 5 to floor 1.
			self.falling[FALL_ALTITUDE] -= self.falling[FALL_SPEED]/game.get_fps()
			if self.falling[FALL_ALTITUDE] < 0:
				#Fall has ended
				falling = False
				for hole in self.game_session.level.floors[self.floor].holes:
					if in_square(hole,self.pos):
						self.falling[FALL_HOLE] = hole
						self.falling[FALL_STAGE] = HOLE_SLIDE
						self.falling[FALL_ALTITUDE] = 1
						falling = True
						break
				if not falling:
					self.falling = [None,None,0,0]
				#Check to see if player has fell onto stairs
				for stairs in self.game_session.level.floors[self.floor].connectors:
					if in_square(stairs,self.pos):
						self.floor_transition = stairs
		if mouse:
			if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION:
				amount = 0
				for event in game.events:
					if event[0] == MOUSEMOTION:
						amount = event[1]/3.
						if amount > 4:
							amount = 4
						elif amount < -4:
							amount = -4
						self.face_angle = (self.face_angle + amount/game.get_fps()) % 6.2831853071795862
						break
				speed = 1 - abs(amount)/4
			else:
				for event in game.events:
					if event[0] == MOUSEMOTION:
						self.game_session.mouse_position[0] += event[1]
						self.game_session.mouse_position[1] += event[2]
						if self.game_session.mouse_position[0] > 1280:
							self.game_session.mouse_position[0] = 1280
						if self.game_session.mouse_position[1] > 720:
							self.game_session.mouse_position[1] = 720
						if self.game_session.mouse_position[0] < 0:
							self.game_session.mouse_position[0] = 0
						if self.game_session.mouse_position[1] < 0:
							self.game_session.mouse_position[1] = 0
				self.face_angle = find_bearing(self.game_session.mouse_position[0] - 640,self.game_session.mouse_position[1] - 360)
				speed = 0.9		
		else:
			if actions & ACTION_LEFT ^ actions & ACTION_RIGHT:
				#2.09439510239 is 2 degrees in radians times 60. Hence it should turn 120 degrees in a second.
				if actions & ACTION_LEFT:
					self.face_angle = (self.face_angle - 2.4/game.get_fps()) % 6.2831853071795862
				if actions & ACTION_RIGHT:
					self.face_angle = (self.face_angle + 2.4/game.get_fps()) % 6.2831853071795862
				speed = 0.4
			else:
				speed = 1
		if actions & ACTION_FORWARD and self.forward_speed >= 0 and self.falling[FALL_STAGE] is None:
			self.forward_speed += 12.0/game.get_fps()
			if self.forward_speed > 6 * speed:
				self.forward_speed -= 12.0/game.get_fps()
		elif actions & ACTION_BACKWARD and self.forward_speed <= 0 and self.falling[FALL_STAGE] is None:
			self.forward_speed -= 12.0/game.get_fps()
			if self.forward_speed < -5 * speed:
				self.forward_speed += 12.0/game.get_fps()
		else:
			if self.forward_speed > 0:
				self.forward_speed -= 11.0/game.get_fps()
				if self.forward_speed < 0:
					self.forward_speed = 0
			elif self.forward_speed < 0:
				self.forward_speed += 11.0/game.get_fps()
				if self.forward_speed > 0:
					self.forward_speed = 0
		if actions & ACTION_LEFT_SIDE and self.side_speed >= 0 and self.falling[FALL_STAGE] is None:
			self.side_speed += 11.0/game.get_fps()
			if self.side_speed > 5 * speed:
				self.side_speed -= 11.0/game.get_fps()
		elif actions & ACTION_RIGHT_SIDE and self.side_speed <= 0 and self.falling[FALL_STAGE] is None:
			self.side_speed -= 11.0/game.get_fps()
			if self.side_speed < -5 * speed:
				self.side_speed += 11.0/game.get_fps()
		else:
			if self.side_speed > 0:
				self.side_speed -= 10.0/game.get_fps()
				if self.side_speed < 0:
					self.side_speed = 0
			elif self.side_speed < 0:
				self.side_speed += 10.0/game.get_fps()
				if self.side_speed > 0:
					self.side_speed = 0
		if actions & ACTION_SWITCH:
			self.get_current_weapon()[1].trigger_off()
			if self.current_weapon == len(self.inventory) - 1:
				self.change_weapon(0)
			else:
				self.change_weapon(self.current_weapon + 1)
				self.game_session.ammochange = True
		if actions & ACTION_FIRE:
			self.get_current_weapon()[1].trigger_on()
		else:
			self.get_current_weapon()[1].trigger_off()
		if actions & ACTION_RELOAD:
			self.get_current_weapon()[1].reload()
		request_position = (self.pos[0] + maths.sin(self.face_angle)*self.forward_speed * 60.0/game.get_fps(),self.pos[1] - maths.cos(self.face_angle)*self.forward_speed * 60.0/game.get_fps())
		request_position = [request_position[0] + maths.sin(self.face_angle - 1.57079633)*self.side_speed * 60.0/game.get_fps(),request_position[1] - maths.cos(self.face_angle - 1.57079633)*self.side_speed * 60.0/game.get_fps()]
		if self.side_speed != 0 or self.forward_speed != 0 or self.falling[FALL_STAGE] == HOLE_SLIDE:
			self.movement_attempt(request_position)
		if self.falling[FALL_STAGE] != HOLE_SLIDE and self.slide_speed != [0,0]:
			self.slide_movement(True,True) #Deccelerate sliding motion when not sliding and not still
		self.check_items([item for item in self.game_session.items if item[ITEM_ID] > 2 and item[ITEM_ID] < 17]) #3 - 8 are the ids for the 5 weapon pickups, 9-14 is the ammo
	def enable_pickup(self,weapon):
		weapon[2] = False
	def get_current_weapon(self):
		return self.inventory[self.current_weapon]
class ComputerPlayer(Player):
	#AI players
	def __init__(self,character,game_session):
		Player.__init__(self,character,game_session)
		self.decision_chances = [0,0,0,0,0,0,0,0,0]
		self.turn_around = 0
	def check_side_view_item_collisions(self,pos,end_of_scan_line,last,coordinate):
		if intersect(pos,end_of_scan_line,last,coordinate):
			point = intersect_point(pos,end_of_scan_line,last,coordinate)
			return ((point[0] - pos[0])**2 + (point[1] - pos[1])**2)**0.5
		else:
			return 721 #Maximum distance, so will not replace anything
	def loop(self):
		actions = 0
		scan_angle = self.face_angle - 1
		scan_part = 0
		max_scan_distance = 0
		vision_proximity = False
		pos1 = (self.pos[0] + maths.sin(self.face_angle - 1.5707963268) * 60,self.pos[1] - maths.cos(self.face_angle - 1.5707963268) * 60) #Left side
		pos2 = (self.pos[0] + maths.sin(self.face_angle + 1.5707963268) * 60,self.pos[1] - maths.cos(self.face_angle + 1.5707963268) * 60) #Right side
		#Particles([pos1,pos2],3,(250,100,150),self.game_session.level.image)
		player_scan_part = None
		closest_player = 721
		health_scan_part = None
		closest_health = 721
		armour_scan_part = None
		closest_armour = 721
		gun_scan_part = None
		closest_gun = 721
		while scan_angle < self.face_angle + 1:
			scan_x_addition = maths.sin(scan_angle) * 1000
			scan_y_addition =  - maths.cos(scan_angle) * 1000
			end_of_scan_line1 = (pos1[0] + scan_x_addition,pos1[1] + scan_y_addition)
			end_of_scan_line2 = (pos2[0] + scan_x_addition,pos2[1] + scan_y_addition)
			end_of_centre_scan_line = (self.pos[0] + scan_x_addition,self.pos[1] + scan_y_addition)
			#Wall scan
			wall_distance1 = 721
			wall_distance2 = 721
			for wall in self.game_session.walls[self.floor]:
				last = None
				for coordinate in wall:
					if last is not None:
						wall_distance_temp = self.check_side_view_item_collisions(pos1,end_of_scan_line1,last,coordinate) #Check left side of player
						if wall_distance_temp < wall_distance1:
							wall_distance1 = wall_distance_temp #Only interested in the distance to nearest wall
						wall_distance_temp = self.check_side_view_item_collisions(pos2,end_of_scan_line2,last,coordinate) #Check right side of player
						if wall_distance_temp < wall_distance2:
							wall_distance2 = wall_distance_temp
					last = coordinate
			if wall_distance1 < wall_distance2: #Get the smallest distance to nearest wall so the AI accounts for each side.
				wall_distance = wall_distance1
			else:
				wall_distance = wall_distance2
			if wall_distance != 721:
				vision_proximity = True
				if wall_distance > max_scan_distance:
					max_scan_distance = wall_distance
					longest_scan_part = scan_part
			#Player scan
			player_distance = 721
			for player in self.game_session.players:
				if player is not self and player.floor == self.floor:
					last = None
					for coordinate in player.current_collision_coordinates:
						level_coordinate = rotate_coordinate((player.pos[0] - player.current_upper.get_width()/2 + coordinate[0],player.pos[1] - player.current_upper.get_height() + 80 + coordinate[1]),player.pos,player.face_angle)
						if last is not None:
							distance = self.check_side_view_item_collisions(self.pos,end_of_centre_scan_line,last,level_coordinate)
							if distance < player_distance:
								if distance < wall_distance:
									player_distance = distance
									break
						last = level_coordinate
			if player_distance < closest_player:
				closest_player = player_distance
				player_scan_part = scan_part
			#Health, armour, ammo and gun scan
			health_min_distance = 721
			armour_min_distance = 721
			gun_min_distance = 721
			for item in self.game_session.items:
				if item[ITEM_DATA] == False and item[ITEM_ID] > 2 and item[ITEM_ID] < 17 and item[ITEM_FLOOR] == self.floor: #Item enabled, on the same floor and significant
					if intersect(self.pos,end_of_centre_scan_line,item[ITEM_POS],(item[ITEM_POS][0] + 20,item[ITEM_POS][1] + 20)) or intersect(self.pos,end_of_centre_scan_line,(item[ITEM_POS][0] + 20,item[ITEM_POS][1]),(item[ITEM_POS][0],item[ITEM_POS][1] + 20)):
						if item[ITEM_ID] == 13 or item[ITEM_ID] == 14: #Health low
							distance = ((item[ITEM_POS][0] - self.pos[0])**2+(item[ITEM_POS][1] - self.pos[1])**2)**0.5
							if distance < health_min_distance:
								health_min_distance = distance
						elif item[ITEM_ID] == 15 or item[ITEM_ID] == 16: #Health low
							distance = ((item[ITEM_POS][0] - self.pos[0])**2+(item[ITEM_POS][1] - self.pos[1])**2)**0.5
							if distance < armour_min_distance:
								armour_min_distance = distance
						elif item[ITEM_ID] > 2:
							#Ammo or weapon.Check inventory for weapon
							id = item[ITEM_ID] - 3 % 5
							found = False
							get_weapon = False
							for weapon in self.inventory:
								if weapon[0] == id:
									#Is ammo low?
									if weapon[1].ammo[0] < weapon[1].ammo[0]*0.4:
										#Better get the weapon then.
										get_weapon = True
									found = True
									break
							if not found:		
								if item[ITEM_ID] < 8:
									#Weapons
									if weapon_classes[id].goodness > self.inventory[self.current_weapon][1].goodness + random.random() - 0.5:
										get_weapon = True
							if get_weapon:
								distance = ((item[ITEM_POS][0] - self.pos[0])**2+(item[ITEM_POS][1] - self.pos[1])**2)**0.5
								if distance < gun_min_distance:
									gun_min_distance = distance
			if health_min_distance < closest_health:
				health_scan_part = scan_part
				closest_health = health_min_distance
			if armour_min_distance < closest_armour:
				armour_scan_part = scan_part
				closest_armour = armour_min_distance
			if gun_min_distance < closest_gun:
				gun_scan_part = scan_part
				closest_gun = gun_min_distance
			scan_angle += 0.1
			scan_part += 1
		if not vision_proximity:
			longest_scan_part = 10
			max_scan_distance = 1000
		if health_scan_part is not None and armour_scan_part is not None:
			if self.health < self.armour:
				armour_scan_part = None
			else:
				health_scan_part = None
		if gun_scan_part is not None:
			longest_scan_part = gun_scan_part
		self.decision_chances[DECISION_FIRE] = 0
		self.decision_chances[DECISION_BACKWARD] = 0
		if max_scan_distance < self.current_upper.get_width() + 200: #Close to wall, cosider movement
			self.decision_chances[DECISION_BACKWARD] = 1
			left = self.decision_chances[DECISION_LEFT]
			right = self.decision_chances[DECISION_RIGHT]
			self.decision_chances[DECISION_BACKWARD] = 1
			self.decision_chances[DECISION_FORWARD] = 0
			if left > right:
				self.decision_chances[DECISION_LEFT] = 1
				self.decision_chances[DECISION_RIGHT] = 0
			elif right >= left:
				self.decision_chances[DECISION_RIGHT] = 1
				self.decision_chances[DECISION_LEFT] = 0
		elif player_scan_part is not None: #Player found, attack when no proximity to wall.
			if player_scan_part > 11 + random.randint(0,2):
				self.decision_chances[DECISION_RIGHT] = 0.95
				self.decision_chances[DECISION_LEFT] = 0
				self.decision_chances[DECISION_LEFT_SIDE] = 0
				self.decision_chances[DECISION_RIGHT_SIDE] = 0.3
			elif player_scan_part < 9 - random.randint(0,2):
				self.decision_chances[DECISION_LEFT] = 0.95
				self.decision_chances[DECISION_RIGHT] = 0
				self.decision_chances[DECISION_RIGHT_SIDE] = 0
				self.decision_chances[DECISION_LEFT_SIDE] = 0.3
			else:
				if random.random() > 0.5: #Slide left
					self.decision_chances[DECISION_RIGHT] = 0.8
					self.decision_chances[DECISION_LEFT_SIDE] = 1
				else: #Slide right
					self.decision_chances[DECISION_LEFT] = 0.8
					self.decision_chances[DECISION_RIGHT_SIDE] = 1
				self.decision_chances[DECISION_FIRE] = 1
				if closest_player < 300:
					self.decision_chances[DECISION_FORWARD] = 0
					self.decision_chances[DECISION_BACKWARD] = 1
				elif closest_player > 500:	
					self.decision_chances[DECISION_FORWARD] = 1
					self.decision_chances[DECISION_BACKWARD] = 0
				else:
					self.decision_chances[DECISION_BACKWARD] = 0
					self.decision_chances[DECISION_FORWARD] = 0
		elif self.turn_around > 0:
			self.turn_around -= 60/game.get_fps()
			self.decision_chances[DECISION_LEFT] = 1
			self.decision_chances[DECISION_RIGHT] = 0
			self.decision_chances[DECISION_FORWARD] = 0.1
		else:
			if armour_scan_part is not None:
				if random.random() > self.armour/100.:
					longest_scan_part = armour_scan_part
			elif health_scan_part is not None:
				if random.random() > self.health/100.:
					longest_scan_part = health_scan_part
			if longest_scan_part < 9:
				self.decision_chances[DECISION_FORWARD] = 0.5
				self.decision_chances[DECISION_LEFT] = 1
				self.decision_chances[DECISION_RIGHT] = 0
				self.decision_chances[DECISION_RIGHT_SIDE] = 0
				self.decision_chances[DECISION_LEFT_SIDE] = 0.1
			elif longest_scan_part > 11:
				self.decision_chances[DECISION_FORWARD] = 0.5
				self.decision_chances[DECISION_RIGHT] = 1
				self.decision_chances[DECISION_LEFT] = 0
				self.decision_chances[DECISION_LEFT_SIDE] = 0
				self.decision_chances[DECISION_RIGHT_SIDE] = 0.1
			else:
				self.decision_chances[DECISION_FORWARD] = 1
				self.decision_chances[DECISION_LEFT] = 0.05
				self.decision_chances[DECISION_RIGHT] = 0.05
		current_weapon = self.get_current_weapon()[1]
		if current_weapon.mag_size != 0:
			if float(current_weapon.ammo[1])/float(current_weapon.mag_size) < 0.4:
				if player_scan_part is None:
					self.decision_chances[DECISION_RELOAD] = 0.01
		action_bit = 1
		for decision in self.decision_chances:
			if decision > random.random():
				actions += action_bit
			action_bit *= 2
		if actions & ACTION_FORWARD and actions & ACTION_BACKWARD:
			if self.decision_chances[DECISION_FORWARD] >= self.decision_chances[DECISION_BACKWARD]:
				actions -= ACTION_BACKWARD
			else:
				actions -= ACTION_FORWARD
		if actions & ACTION_LEFT and actions & ACTION_RIGHT:
			if self.decision_chances[DECISION_LEFT] > self.decision_chances[DECISION_RIGHT]:
				actions -= ACTION_RIGHT
			else:
				actions -= ACTION_LEFT
		self.do_actions(actions)
	def damage(self,damage,inflicter):
		self.turn_around = 60
		Player.damage(self,damage,inflicter)
class GameSession():
	#The game which is the main part of the entire program
	barrel_circle_coordinates = [(40.0, 140.0), (49.983341664682811, 139.50041652780257), (59.866933079506111, 138.00665778412417), (69.552020666133956, 135.53364891256058), (78.941834230865055, 132.10609940028854), (87.942553860420304, 127.75825618903727), (96.464247339503544, 122.53356149096781), (104.42176872376912, 116.48421872844885), (111.73560908995228, 109.67067093471655), (118.33269096274833, 102.16099682706648), (124.14709848078964, 94.030230586813985), (129.12073600614352, 85.359612142557751), (133.20390859672261, 76.235775447667351), (136.35581854171932, 66.749882862458747), (138.54497299884602, 56.996714290024073), (139.74949866040546, 47.073720166770272), (139.95736030415054, 37.080047769871101), (139.16648104524685, 27.115550570447482), (137.38476308781946, 17.279790530691244), (134.63000876874145, 7.671043313649605), (130.92974268256813, -1.614683654714284), (126.32093666488736, -10.484610459985788), (120.84964038195899, -18.850111725534617), (114.57052121767198, -26.62760212798247), (107.54631805511505, -33.739371554124602), (99.847214410395566, -40.114361554693417), (91.550137182146329, -45.688875336894768), (82.737988023382897, -50.407214201706154), (73.498815015590381, -54.222234066865852), (63.92493292139811, -57.095816514959083), (54.112000805986597, -58.999249660044555), (44.158066243328911, -59.913515027327946), (34.162585657241863, -59.829477579475295), (24.225430585675003, -58.747976990886457), (14.445889797316703, -56.67981925794605), (4.9216772310378474, -53.645668729079574), (-4.2520443294854076, -49.67584163341462), (-12.983614090849485, -44.810003171040705), (-21.185789094272067, -39.096771191441547), (-28.776615918397525, -32.593230420013867), (-35.680249530792935, -25.364362086361055), (-41.827711106441129, -17.482394653326772), (-47.157577241358865, -9.0260821340698669), (-51.61659367494552, -0.079917207997453943), (-55.160207388951619, 9.2667130021580668), (-57.753011766509701, 18.920420056922023), (-59.369100363346448, 28.784747306494509), (-59.992325756410082, 38.761133653710843), (-59.616460883584082, 48.749898343944551), (-58.245261262433274, 58.651236942257405), (-55.892427466313904, 68.366218546322443), (-52.581468232773304, 77.797774271297868), (-48.345465572015456, 86.85166713003747), (-43.226744222390266, 95.437433617915843), (-37.276448755598935, 103.46928759426319), (-30.554032557039449, 110.86697742912577), (-23.126663787232431, 117.55658785102472), (-15.068554259764127, 123.47127848391573), (-6.4602179413761291, 128.55195169413173), (2.6123335169759088, 132.74784307440339), (12.058450180106899, 136.01702866503643), (21.783749572789883, 138.32684384425835), (31.691059718249743, 139.65420970232171)]
	def init(self):
		self.pause_menu = [False] * 2
		self.end_menu = [False] * 3
		self.hud_corner_top_left = Surface((200,100))
		self.hud_corner_top_left.round_corners(20,BOTTOM_RIGHT)
		self.hud_corner_top_right = Surface((200,100))
		self.hud_corner_top_right.round_corners(20,BOTTOM_LEFT)
		self.hud_corner_bottom_left = Surface((200,100))
		self.hud_corner_bottom_left.round_corners(20,TOP_RIGHT)
		self.hud_corner_bottom_right = Surface((200,100))
		self.hud_corner_bottom_right.round_corners(20,TOP_LEFT)
		self.time_font = Font("NEUROPOL",70)
		self.ammo_font = Font("NEUROPOL",40)
		self.crosshairs = Surface((50,50))
		self.crosshairs.set_background_alpha(0)
		add_line(self.crosshairs,menu_theme.selected_colour,(25,0),(25,50),2)
		add_line(self.crosshairs,menu_theme.selected_colour,(0,25),(50,25),2)
		add_line(self.crosshairs,menu_theme.selected_colour,(25,15),(35,25),2,True)
		add_line(self.crosshairs,menu_theme.selected_colour,(35,25),(25,35),2,True)
		add_line(self.crosshairs,menu_theme.selected_colour,(25,35),(15,25),2,True)
		add_line(self.crosshairs,menu_theme.selected_colour,(15,25),(25,15),2,True)
		self.particles = []
	def transfer(self,*options):
		game.show_cursor(False)
		self.music,self.level,self.level_name,self.mode,self.radar,self.one_shot_kill,bot_list,self.weapon_list,self.player_character,self.friendly_fire,self.friendly_fire_penalty,self.team_mode,self.mode_options = options
		#Update level play information
		f = open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + self.level_name + "/information.dat", 'rb')
		level_information = pickle.loads(f.read())
		level_information.plays += 1
		level_information.last_played = time.time()
		f.close()
		f = open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + self.level_name + "/information.dat", 'wb')
		f.write(pickle.dumps(level_information, 2))
		f.close()
		#Track the mouse and lock movement when using it for controls
		if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING:
			game.track_mouse()
		file = os.listdir(os.path.dirname(sys.argv[0]) + "/music/game/")[self.music]
		if file[-4:] == ".ogg":
			self.music = "/music/game/" + file
		else:
			self.music = ""
		#Transparency
#######################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                          MAY BE REDUNDANT                                                           #
#                                             RETENTION FOR FUTURE POSSIBLE USE                                          #
#                                                                                                                                                     #
#######################################################################################
		'''self.floor_under_show = [[],[],[],[]]
		for x in xrange(1,len(self.level.floors)):
			first_indices = []
			for box_coordinates in self.level.floors[x].connectors + self.level.floors[x].transparent_boxes + self.level.floors[x].holes:
				x_range = [box_coordinates[0][0]/1000,box_coordinates[2][0]/1000]
				if x_range[0] > x_range[1]:
					temp = x_range[0]
					x_range[0] = x_range[1]
					x_range[1] = temp
				y_range = [box_coordinates[0][1]/1000,box_coordinates[2][1]/1000]
				if y_range[0] > y_range[1]:
					temp = y_range[0]
					y_range[0] = y_range[1]
					y_range[1] = temp
				for y in xrange(x_range[0] - 1,x_range[1]):
					for z in xrange(y_range[0] - 1,y_range[1]):
						if (y,z) not in self.floor_under_show[x - 1]:
							first_indices.append((y,z)) #Adds index for a required texture underneath
			if x != 1:
				for prior_indices in self.floor_under_show[x-2]:
					indices = []
					for index in prior_indices:
						if index in first_indices:
							indices.append(index)
					self.floor_under_show[x - 1].append(indices)
			self.floor_under_show[x - 1].append(first_indices)'''
#######################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                      END                                                                        #
#                                                                                                                                                     #
#                                                                                                                                                     #
#######################################################################################
		#Transparency end
		x = 0
		for floor in self.level.floors:
			Player.spawn_points += [i + [x] for i in floor.items if i[ITEM_ID] == 0]
			x += 1
		Player.available_spawn_points = Player.spawn_points[:]
		self.bots = []
		if self.team_mode:
			self.teams = [[],[]]
			for bot in bot_list:
				self.bots.append(ComputerPlayer(bot[0],self))
				self.bots[-1].team = bot[1]
				self.teams[bot[1]].append(self.bots[-1])
			self.control_player = Player(self.player_character[0],self)
			self.control_player.team = self.player_character[1]
			self.teams[self.player_character[1]].append(self.control_player)
			if self.mode == MODE_DEATHMATCH:
				self.team_scores = [0,0]
			elif self.mode == MODE_ELIMINATION:
				self.team_scores = [len(self.teams[0]) * self.mode_options[ELIM_LIVES],len(self.teams[1]) * self.mode_options[ELIM_LIVES]]
		else:
			for bot in bot_list:
				self.bots.append(ComputerPlayer(bot,self))
			self.control_player = Player(self.player_character,self)
		self.players = [self.control_player] + self.bots
		self.hud_corner_bottom_right.fill(list(menu_theme.selected_colour) + [230])
		self.hud_corner_bottom_left.fill(list(menu_theme.selected_colour) + [230])
		self.hud_corner_top_right.fill(list(menu_theme.selected_colour) + [230])
		self.hud_corner_top_left.fill(list(menu_theme.selected_colour) + [230])
		self.start_time = time.time()
		self.paused = False
		pause_menu = [None]
		pause_menu[0] = Menu("Paused")
		pause_menu[0].add_button("Resume",RESUME,True)
		pause_menu[0].add_button("Options",OPTTOG,True)
		pause_menu[0].add_button("Controls",CONTROLS,True)
		pause_menu[0].add_button("End Preview" if self.mode == MODE_PREVIEW else "End Game",END_GAME,True)
		pause_menu[0].create()
		self.pause_menu = MenuSet(pause_menu,game)
		self.options_menu_active = self.pause_menu
		self.p_key = False
		self.down_key = False
		self.r_key = False
		self.pause_start_time = 0
		self.health_bar = open_image(os.path.dirname(sys.argv[0]) + "/images/misc/health_bar.png")
		self.health_back = Surface((280,600))
		self.health_back.fill((0,0,0,100))
		self.health_back.set_background_alpha(0)
		self.health_back.blit(self.health_bar,(0,0))
		self.armour_bar = open_image(os.path.dirname(sys.argv[0]) + "/images/misc/armour_bar.png")
		self.armour_back = Surface((280,600))
		self.armour_back.set_background_alpha(0)
		self.armour_back.fill((0,0,0,100))
		self.armour_back.blit(self.armour_bar,(0,0))
		self.health_armour_start = 0
		self.ammochange = True
		self.bullet_queue = []
		self.items = []
		x = 0
		for floor in self.level.floors:
			self.items += [[item[ITEM_ID],item[ITEM_POS],False,None,x] for item in floor.items if item[ITEM_DATA] == None] #Item data is none when not a spawn point
			x += 1
		self.barrels = []
		for item in self.items:
			if item[ITEM_ID] > 2 and item[ITEM_ID] < 13:
				if item[ITEM_ID] < 8: #Weapon pickup
					item[ITEM_IMG] = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.weapon_list[item[ITEM_ID] - 3]) + "/pickup.png")
				else: #Ammo pickup
					item[ITEM_IMG] = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.weapon_list[item[ITEM_ID] - 8]) + "/ammo.png")
			else: #Static item
				item[ITEM_IMG] = open_image(os.path.dirname(sys.argv[0]) + "/images/items/" + str(item[ITEM_ID]) + ".png")
				if item[ITEM_ID] == 17:
					self.barrels.append([item,[(coordinate[0] + item[ITEM_POS][0],coordinate[1] + item[ITEM_POS][1]) for coordinate in self.barrel_circle_coordinates]])
		self.barrel_coordinates = [barrel[ITEM_POS] for barrel in self.barrels]
		self.explosions = []
		self.walls = [[[(0,0),(0,floor.image.get_height()),(floor.image.get_width(),floor.image.get_height()),(floor.image.get_width(),0)]] + [barrel[1] for barrel in self.barrels if self.level.floors[barrel[0][ITEM_FLOOR]] == floor] + floor.walls for floor in self.level.floors if floor.image is not None]
		self.control_player.spawn()
		for bot in self.bots:
			bot.spawn()
		self.mouse_position = [640,200]
		self.position = ""
		self.mouse_fire = False
	def map_level_to_screen(self,position):
		if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION:
			return rotate_coordinate((640 + position[0] - self.control_player.pos[0],600 + position[1] - self.control_player.pos[1]),(640,600),-self.control_player.face_angle)
		else:
			return (position[0] + 640  - self.control_player.pos[0],position[1] + 360 - self.control_player.pos[1])
	def bullet_line(self,bullet_origin,shooter,head,body,side,ricochets,angle,is_ricochet,alpha):
		wall_bearing = None
		#Find wall collsions
		bullet_extension = (bullet_origin[0] +  maths.sin(angle) * 12727, bullet_origin[1] -  maths.cos(angle) * 12727) #12727 is close to the maximum diagonal length of a level
		collide_point = bullet_extension
		contender_distance = 12727
		bullet_bearing = find_bearing(bullet_origin[0] - bullet_extension[0],bullet_origin[1] - bullet_extension[1])
		for wall in self.walls[shooter.floor]:
			last = None
			for coordinate in wall:
				if last is not None:
					if intersect((bullet_origin[0] +  maths.sin(angle) * 1, bullet_origin[1] -  maths.cos(angle) * 1),bullet_extension,last,coordinate): #Move along one to prevent intersecting with the rebounding wall
						#Find intersects
						contender = intersect_point(bullet_origin,bullet_extension,last,coordinate)
						if contender == None:
							continue
						distance = ((bullet_origin[0] - contender[0])**2 + (bullet_origin[1] - contender[1])**2)**0.5
						if distance < contender_distance:
							contender_distance = distance
							collide_point = contender
							if ricochets != 0:
								wall_bearing = find_bearing(last[0] - coordinate[0],last[1] - coordinate[1])
				last = coordinate
		#Test collision with barrels
		for barrel in self.barrels:
			if not barrel[0][2] and barrel[0][ITEM_FLOOR] == shooter.floor:
				last = None
				for coordinate in barrel[1]:
					if last is not None:
						if intersect(bullet_origin,bullet_extension,last,coordinate):
							#initiate explosion with the barrel.
							barrel[0][2] = True
							barrel[0][3] = open_image(os.path.dirname(sys.argv[0]) + "/images/items/17 burnt.png")
							for player in self.players:
								if player.floor == shooter.floor:
									if self.team_mode:
										if not self.friendly_fire:
											if shooter.team == player.team:
												continue
									distance = ((player.pos[0] - barrel[0][1][0])**2 + (player.pos[1] - barrel[0][1][1])**2)**0.5
									if distance < 401:
										player.damage(int(200-float(distance)/2.),shooter)
										if distance < 250:
											angle = find_bearing(player.pos[0] - barrel[0][1][0],player.pos[1] - barrel[0][1][1])
											for x in xrange(int(distance/25)):
												self.blood(player.pos,angle - 1 + random.random()*2,random.random() * 20 + 40,player.floor)
							self.explosions.append([(barrel[0][1][0] + 40,barrel[0][1][1] + 40),5,shooter.floor])
							game.play_sound("/sounds/explosion.mp3")
							break
					last = coordinate
		#Test for bullet collisions with players
		for player in self.players:
			if self.team_mode:
				if not self.friendly_fire:
					if shooter.team == player.team:
						continue
			if player.floor == shooter.floor:
				if not is_ricochet and player is shooter: #Shooter can't kill self unless it is a ricochet
					continue
				last = None
				length = None
				for coordinate in player.current_collision_coordinates:
					new_coordinate = rotate_coordinate((player.pos[0] - player.current_upper.get_width()/2 + coordinate[0],player.pos[1] - player.current_upper.get_height() + 80 + coordinate[1]),player.pos,player.face_angle)
					if last is not None:
						if intersect(new_coordinate,last,bullet_origin,collide_point):
							point = intersect_point(new_coordinate,last,bullet_origin,collide_point)
							if length == None:
								length = abs(point[0] - bullet_origin[0])
								last_point = point
							else:
								if length > abs(point[0] - bullet_origin[0]):
									point = last_point
					last = new_coordinate
				if length is not None:
					for x in xrange(3):
						self.blood(point,bullet_bearing - 1 + random.random()*2,random.random() * 20 + 10,player.floor)
					point = rotate_coordinate(point,player.pos,6.2831853071795862 - player.face_angle)
					x_point = point[0] - player.pos[0] + player.current_upper.get_width()/2
					x_point  = x_point / float(player.current_upper.get_width())
					if x_point < 0.2 or x_point > 0.8:
						player.damage(side,shooter)
					elif x_point > 0.4 and x_point < 0.6:
						player.damage(head,shooter)
					else:
						player.damage(body,shooter)
		#Draw the line
		if shooter.floor == self.control_player.floor:
			add_line(game,(240,230,50,alpha),self.map_level_to_screen(bullet_origin),self.map_level_to_screen(collide_point),2)
		#Do ricochets
		if ricochets != 0 and wall_bearing is not None:
			normal = wall_bearing - 1.5707963267948966
			new_angle = normal*2 - bullet_bearing
			self.bullet_line(collide_point,player,head/2,body/2,side/2,ricochets - 1,new_angle,True,alpha)
	def bullet_player(self,position,player,head,body,side,ricochets,alpha):
		#The code for bullets
		self.bullet_line(rotate_coordinate((player.pos[0] - player.current_upper.get_width()/2 + position[0],player.pos[1] - player.current_upper.get_height() +50 + position[1]),player.pos,player.face_angle),player,head,body,side,ricochets,player.face_angle,False,alpha)
	def blood(self,origin,angle,distance,floor):
		coordinates = []
		origin = (origin[0] + maths.sin(angle) * distance,origin[1] + maths.cos(angle) * distance)
		for x in xrange(15):
			angle = float(x)/2.3873241464
			d = random.random()*15 + 1
			coordinates.append((origin[0] + maths.sin(angle) * d,origin[1] + maths.cos(angle) * d))
		Polygon(smooth_polygon_edges(coordinates,2),(145,5,3,230),self.level.floors[floor].image)
	def make_health_bar(self):
		self.health = Surface((280,600))
		self.health.set_background_alpha(0)
		self.health.blit(self.health_back,(0,0))
		if self.control_player.health > 0:
			health_front = Surface((280,6 * self.control_player.health))
			health_front.fill((0,0,0,200))
			health_front.set_background_alpha(0)
			health_front.blit(self.health_bar,(0,-600+6*self.control_player.health))
			self.health.blit(health_front,(0,600 - 6*self.control_player.health))
		self.health_armour_start = time.time()
	def make_armour_bar(self):
		self.armour = Surface((280,600))
		self.armour.set_background_alpha(0)
		self.armour.blit(self.armour_back,(0,0))
		if self.control_player.armour > 0:
			armour_front = Surface((280,6 * self.control_player.armour))
			armour_front.fill((0,0,0,200))
			armour_front.set_background_alpha(0)
			armour_front.blit(self.armour_bar,(0,-600+6*self.control_player.armour))
			gaussian_blur(armour_front.texture,10,armour_front.get_width(),armour_front.get_height())
			self.armour.blit(armour_front,(0,600 - 6*self.control_player.armour))
		self.health_armour_start = time.time()
	def loop(self):
		if game.key(key.P):
			self.p_key = True
		else:
			if self.p_key == True:
				if self.paused:
					self.start_time += time.time() - self.pause_start_time
				else:
					self.pause_start_time = time.time()
					game.play_sound("/sounds/pause.mp3")
				self.paused = not self.paused
			self.p_key = False
		#Level
		if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION:
			rotate = self.control_player.face_angle
		else:
			rotate = 0
		if not self.paused:
			actions = 0
			if game.controls[CONTROLS_TURNING_MODE] == KEYBOARD_TURNING:
				if game.key(game.controls[CONTROLS_KEYBOARD_TURN_LEFT]):
					actions += ACTION_LEFT
				if game.key(game.controls[CONTROLS_KEYBOARD_TURN_RIGHT]):
					actions += ACTION_RIGHT
			if game.key(game.controls[CONTROLS_MOUSE_FORWARD] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_FORWARD]):
				actions += ACTION_FORWARD
			if game.key(game.controls[CONTROLS_MOUSE_BACKWARD] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_BACKWARD]):
				actions += ACTION_BACKWARD
			if game.key(game.controls[CONTROLS_MOUSE_STRAFE_LEFT] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_STRAFE_LEFT]):
				actions += ACTION_LEFT_SIDE
			if game.key(game.controls[CONTROLS_MOUSE_STRAFE_RIGHT] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_STRAFE_RIGHT]):
				actions += ACTION_RIGHT_SIDE
			if game.key(game.controls[CONTROLS_MOUSE_SWITCH] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_SWITCH]):
				if not self.down_key:
					self.down_key = True
					actions += ACTION_SWITCH
			else:
				self.down_key = False
			if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING:
				for event in game.events:
					if event[0] == MOUSEDOWN:
						if event[1] == LEFT_MOUSE_BUTTON:
							self.mouse_fire = True
							break
					elif event[0] == MOUSEUP:
						if event[1] == LEFT_MOUSE_BUTTON:
							self.mouse_fire = False
							break
				if self.mouse_fire:
					actions += ACTION_FIRE
			else:
				if game.key(game.controls[CONTROLS_KEYBOARD_FIRE]):
					actions += ACTION_FIRE
			if game.key(game.controls[CONTROLS_MOUSE_RELOAD] if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING else game.controls[CONTROLS_KEYBOARD_RELOAD]):
				if not self.r_key:
					self.r_key = True
					actions += ACTION_RELOAD
			else:
				self.r_key = False
			self.control_player.do_actions(actions,game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING)
			for bot in self.bots:
				bot.loop()
			#Rendering
			x = 0
			#Next floor
			if self.control_player.floor_transition is not None or self.control_player.falling[FALL_STAGE] == FREEFALL:
				a = 2
			else:
				a = 1
			for floor in self.level.floors[:self.control_player.floor + a]:
				alpha = 255
				if x == self.control_player.floor + 1:
					if self.control_player.floor_transition is not None:
						distance = line_point_distances(self.control_player.floor_transition[3],self.control_player.floor_transition[0],self.control_player.pos)
						alpha = 255 * distance[ALONG_LINE]
					else:
						alpha = 255 * self.control_player.falling[FALL_ALTITUDE]
				#Level Image
				floor.image.colour[3] = alpha
				if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION:
					game.blit(floor.image,(- self.control_player.pos[0] + 640,-self.control_player.pos[1] + 600),-rotate,(640,600))
				else:
					game.blit(floor.image,self.map_level_to_screen((0,0)))
				#Computer Players
				for bot in self.bots:
					if bot.floor == x or (bot.floor == x - 1 and bot.floor_transition is not None):
						pos = self.map_level_to_screen(bot.pos)
						bot.current_upper.colour[3] = alpha
						game.blit(bot.current_upper,(pos[0] - bot.current_upper.get_width()/2,pos[1] - bot.current_upper.get_height()/2),(-self.control_player.face_angle if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION else 0) + bot.face_angle,pos)
				#Bullets
				for bullet_args in self.bullet_queue:
					self.bullet_player(*bullet_args + (alpha,))
				self.bullet_queue = []
				#Items
				for item in self.items:
					if (not item[ITEM_DATA] or item[ITEM_ID] == 17) and  self.level.floors[item[ITEM_FLOOR]] == floor: #When False, item is available or always show if an explosive barrel
						item[ITEM_IMG].colour[3] = alpha
						game.blit(item[ITEM_IMG],self.map_level_to_screen(item[ITEM_POS])) #Element 3 is the item image. Element 1 is the item coordinates
				#Explosions
				for explosion in self.explosions:
					if  self.level.floors[explosion[EXPLOSION_FLOOR]] == floor:
						coordinates1 = []
						coordinates2 = []
						for x in xrange(20):
							angle = float(x)/3.1830988618
							d1 = random.random()*20 - 32*(explosion[1]-2.5)**2 + 201
							d2 = random.random()*20 - 16*(explosion[1]-2.5)**2 + 101
							coordinates1.append(self.map_level_to_screen((explosion[EXPLOSION_POS][0] + maths.sin(angle) * d1,explosion[EXPLOSION_POS][1] + maths.cos(angle) * d1)))
							coordinates2.append(self.map_level_to_screen((explosion[EXPLOSION_POS][0] + maths.sin(angle) * d2,explosion[EXPLOSION_POS][1] + maths.cos(angle) * d2)))
						Polygon(smooth_polygon_edges(coordinates1,-16*(explosion[EXPLOSION_TIME]-2.5)**2+101),(220,120,100,alpha/2.))
						Polygon(smooth_polygon_edges(coordinates2,-8*(explosion[EXPLOSION_TIME]-2.5)**2+51),(240,220,170,alpha/2.5))
						explosion[EXPLOSION_TIME] -= 30./game.get_fps()
				self.explosions = [explosion for explosion in self.explosions if explosion[EXPLOSION_TIME] > 0]
				x += 1
		#Player
		if game.controls[CONTROLS_ROTATION_MODE] == LEVEL_ROTATION:
			game.blit(self.control_player.current_upper,((1280-self.control_player.current_upper.get_width())/2,650-self.control_player.current_upper.get_height()))
		else:
			game.blit(self.control_player.current_upper,((1280-self.control_player.current_upper.get_width())/2,(720-self.control_player.current_upper.get_width())/2),self.control_player.face_angle,(640,360))
		#Crosshairs if used by control system
		if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING:
			if game.controls[CONTROLS_ROTATION_MODE] == PLAYER_ROTATION :
				game.blit(self.crosshairs,(self.mouse_position[0] - 25,self.mouse_position[1] - 25))
		#HUD
		if self.mode > MODE_PREVIEW:
			if self.team_mode:
				if self.mode == MODE_DEATHMATCH:
					position = "1st" if self.team_scores[self.control_player.team] > self.team_scores[1 if self.control_player.team == 0 else 0] else "2nd"
				else:
					position = str(self.team_scores)
			else:
				if self.mode == MODE_DEATHMATCH:
					x = 1
					e = False
					for bot in self.bots:
						if bot.score > self.control_player.score:
							x += 1
						elif bot.score == self.control_player.score:
							e = True
					position = str(x) + ("st" if x == 1 else ("nd" if x == 2 else ("rd" if x == 3 else "th"))) + (" =" if e else "")
				else:
					position = str(self.control_player.score)
			if position != self.position:
				self.position = position
				self.hud_corner_top_left.fill(list(menu_theme.selected_colour) + [230])
				text = self.time_font.render(position,menu_theme.text_colour)
				self.hud_corner_top_left.blit(text,((200 - text.get_width())/2,(100 - text.get_height())/2))
			game.blit(self.hud_corner_top_left,(0,0))
		if self.mode == MODE_DEATHMATCH:
			if self.mode_options[DEATHMATCH_TIME] > 0:
				if not self.paused:
					self.hud_corner_top_right.fill(list(menu_theme.selected_colour) + [230])
					seconds_left = self.mode_options[DEATHMATCH_TIME] - int(time.time() - self.start_time)
					seconds = seconds_left % 60
					text = self.time_font.render(str(seconds_left / 60) + ":" + ("0" if seconds < 10 else "") + str(seconds),menu_theme.text_colour)
					self.hud_corner_top_right.blit(text,((200 - text.get_width())/2,(100 - text.get_height())/2))
				game.blit(self.hud_corner_top_right,(1080,0))
		if self.control_player.current_weapon != 0: #Not unarmed
			if self.ammochange:
				self.ammochange = False
				current_weapon = self.control_player.get_current_weapon()[1]
				self.hud_corner_bottom_left.fill(list(menu_theme.selected_colour) + [230])
				if current_weapon.mag_size == 0:
					text = str(current_weapon.ammo[0])
				else:
					text = str(current_weapon.ammo[0]) + "    " + str(current_weapon.ammo[1])
				text = self.ammo_font.render(text,menu_theme.text_colour)
				self.hud_corner_bottom_left.blit(text,((200 - text.get_width())/2,(100 - text.get_height())/2))
			game.blit(self.hud_corner_bottom_left,(0,620))
		game.blit(self.hud_corner_bottom_right,(1080,620))
		if time.time() - self.health_armour_start < 1 or self.paused:
			game.blit(self.health,(50,60))
			game.blit(self.armour,(950,60))
		#If paused
		if self.paused:
			if self.options_menu_active != self.pause_menu:
				event = self.options_menu_active.loop(self.pause_menu,True)
			else:
				event = self.options_menu_active.loop(game.events)
			if event == RESUME:
				self.paused = False
			elif event == END_GAME:
				if game.controls[CONTROLS_TURNING_MODE] == MOUSE_TURNING:
					game.track_mouse(False)
				game.transfer_section(2,(None,True))
			elif event == OPTTOG: #Toggle options menu
				game.play_sound("/sounds/menu3/change.ogg")
				if self.options_menu_active == options_menu:
					self.options_menu_active = self.pause_menu
				else:
					self.options_menu_active = options_menu
					options_menu.enter = True
					options_menu.return_key = True
			elif event == CONTROLS:
				game.play_sound("/sounds/menu3/change.ogg")
				if self.options_menu_active == controls_menu:
					self.options_menu_active = self.pause_menu
				else:
					self.options_menu_active = controls_menu
					controls_menu.enter = True
					controls_menu.return_key = True
		Particles(self.particles,20,(0,100,200))
		self.particles = []
	def exit(self):
		pass
class LevelInformation():
	def __init__(self):
		self.established = time.time()
		self.description = ""
		self.plays = 0
		self.last_played = 0
		self.format = 0 #Format 0. Used for future identification of the level format for future proofing.
class Level():
	def __init__(self):
		self.weapons = [1,2,3,4,5]
		self.floors = [Floor(),Floor(),Floor(),Floor(),Floor()]
		self.recomended_muisc = 0
class Floor():
	def __init__(self):
		self.walls = []
		self.items = []
		self.image = None
		self.connectors = []
		self.holes = []
		self.transparent_boxes = []
		self.imgfile = None
		self.thumb = None
		self.done_thumb = False
	def add_connector(self,connector_coordinates):
		self.connectors.append(connector_coordinates)
	def add_item(self,item_id,pos,data):
		self.items.append([item_id,pos,data,None])
	def add_blue_spawn_point(self,spawn_point_object,a,b):
		self.blue_spawn_points.append([spawn_point_object,a,b])
	def add_wall(self,wall):
		self.walls.append(wall)
	def add_image(self,image):
		self.image = LargeImg(image)
		self.imgfile = image
		#Make thumbnail - Images showing each floor, for previews.
		aspect = float(self.image.get_width())/self.image.get_height()
		self.thumb = Surface((100,100))
		self.thumb.set_background_alpha(0)
		if aspect > 1:
			self.image.scale((100,100/aspect))
			self.thumb.blit(self.image,(0,50 - 50/aspect))
		else:
			self.image.scale((100*aspect,100))
			self.thumb.blit(self.image,(50 - 50*aspect,100))
		self.image.scale(self.image.get_size())
		self.done_thumb = True
	def add_box(self,box,section):
		if section == MMS_HOLE:
			self.holes.append(box)
		elif section == MMS_TRANSPARENT:
			self.transparent_boxes.append(box)
class MapmakerButton(Surface):
	text_font = Font("Geneva",10)
	end_offset = 0
	def __init__(self,text,title,surface):
		self.surface = surface
		self.pos = MapmakerButton.end_offset 
		self.text = self.text_font.render(text,menu_theme.text_colour)
		Surface.__init__(self,(self.text.get_width() + 20, 25))
		MapmakerButton.end_offset += self.get_width()
		self.title = title
	def render(self,selected):
		if not selected or self.title:
			self.fill(menu_theme.not_selected_colour)
		else:
			self.fill(menu_theme.selected_colour)
		self.blit(self.text,(10,5))
		self.surface.blit(self,(self.pos,0))
class Scrollbar(Surface):
	handle = Surface((16,16))
	handle.round_corners(8)
	def __init__(self,size,offset,surface,side=0,pos=0):
		if side == 0:
			Surface.__init__(self,(19,size))
		else:
			Surface.__init__(self,(size,19))
		self.set_background_alpha(0)
		self.side = side
		self.size = size
		self.offset = offset
		self.surface = surface
		self.handle.fill(menu_theme.text_colour)
		self.pos = pos
		self.drag = False
		self.render()
	def render(self):
		self.fill([255,255,255])
		if self.side == 0:
			add_line(self,menu_theme.text_colour,(9,0), (9,self.size),2)
			self.blit(self.handle,(3,self.pos))
		else:
			add_line(self, menu_theme.text_colour,(0,9), (self.size,9),2)
			self.blit(self.handle,(self.pos,3))
		self.surface.blit(self,(self.offset))
	def mouse(self,pos,type):
		if self.side == 0:
			xpos = pos[1] - self.get_offset()[1]
		else:
			xpos = pos[0] - self.get_offset()[0]
		change_pos = False
		if type == MOUSEDOWN and point_collide(pos,self.handle):
			self.drag = True
		elif type == MOUSEUP and self.drag:
			self.drag = False
		elif self.drag:
			change_pos = True
		elif type == MOUSEDOWN and point_collide(pos,self):
			change_pos = True
			self.drag = True
		if change_pos:
			self.pos = (xpos - 8 if xpos > 8 else 0) if xpos <= self.size - 8 else self.size - 16
		self.render()
		return change_pos
	def get_pos(self):
		return float(self.pos)/float(self.size-16)
class Frame():
	def __init__(self,size,pos,surface,view_port_size = None):
		if view_port_size == None:
			view_port_size = size
		self.surface = surface
		self.pos = pos
		self.border = Surface((size[0] + 10,size[1] + 10))
		self.border.fill(menu_theme.text_colour)
		self.border.round_corners(30)
		self.inner = Surface(size)
		self.inner.fill(menu_theme.not_selected_colour)
		self.inner.round_corners(25)
		self.viewport = Surface(view_port_size)
		self.viewport.fill(menu_theme.not_selected_colour)
		self.contents = Surface((1,1))
	def render(self):
		self.viewport.fill(menu_theme.not_selected_colour)
		self.viewport.fill(menu_theme.not_selected_colour)
		self.viewport.blit(self.contents,(0,0))
		self.inner.blit(self.viewport,(0,0))
		self.border.blit(self.inner,(5,5))
		self.surface.blit(self.border,self.pos)
	def add_to_frame(self,surface):
		self.contents = surface
class ViewPoint(Frame):
	def __init__(self,size,title,pos,surface):
		Frame.__init__(self,size,pos,surface,(size[0] - 30,size[1] - 30))
		self.title = Font("Geneva",15).render(title,menu_theme.text_colour)
		self.inner.blit(self.title,(20,10))
		self.scrollbar = Scrollbar(size[1] - 45,(size[0] - 30,30),self.inner)
	def render(self,pos=0):
		self.viewport.fill(menu_theme.not_selected_colour)
		self.viewport.fill(menu_theme.not_selected_colour)
		length = -self.contents.get_height() + self.viewport.get_height()
		if length > 0:
			length = 0
		self.viewport.blit(self.contents,(0,length*pos))
		self.inner.blit(self.viewport,(0,30))
		self.inner.blit(self.title,(20,10))
		self.border.blit(self.inner,(5,5))
		self.surface.blit(self.border,self.pos)
		self.xpos = pos
	def mouse(self,pos,event):
		if event[0] == MOUSEUP:
			if point_collide(pos,self.viewport):
				if (event[1] == 4 or event[1] == 5):
					if event[1] == 4:
						xpos = self.scrollbar.pos - 10000 * (60/game.get_fps()) * 1/(self.contents.get_height() - self.viewport.get_height())
					elif event[1] == 5:
						xpos = self.scrollbar.pos + 10000 * (60/game.get_fps()) * 1/(self.contents.get_height() - self.viewport.get_height())
					self.scrollbar.pos = (xpos if xpos > 8 else 0) if xpos <= self.scrollbar.size - 8 else self.scrollbar.size - 16
					self.scrollbar.render()
					self.render(self.scrollbar.get_pos())
		self.inner.fill(menu_theme.not_selected_colour)
		self.scrollbar.mouse(pos,event[0])
		self.render(self.scrollbar.get_pos())
	def add_to_view_point(self,surface):
		Frame.add_to_frame(self,surface)
class MapmakerRoundButton(Surface):
	def __init__(self,offset,size,text,parent):
		Surface.__init__(self,size,SRCALPHA)
		self.fill(menu_theme.text_colour)
		self.round_corners(10)
		self.inner = Surface((size[0] - 10,size[1] - 10),SRCALPHA)
		self.inner.fill(menu_theme.not_selected_colour)
		self.inner.round_corners(5)
		self.title = Font("Geneva",15).render(text,menu_theme.text_colour)
		self.blit(self.inner,(5,5))
		self.blit(self.title,(30,(size[1] - self.title.get_height())/2))
		parent.blit(self,offset)
		self.parent = parent
		self.inner_selected = False
	def mouse(self,mouse_pos,event):
		changed = False
		if point_collide(mouse_pos,self):
			if event[0] == MOUSEMOTION:
				self.inner_selected = True
				self.inner.fill(menu_theme.selected_colour)
				self.inner.fill(menu_theme.selected_colour)
				changed = True
			else:
				return True
		elif self.inner_selected:
			if event[0] == MOUSEMOTION:
				self.inner_selected = False
				self.inner.fill(menu_theme.not_selected_colour)
				self.inner.fill(menu_theme.not_selected_colour)
				changed = True
		if changed:
			self.blit(self.inner,(5,5))
			self.blit(self.title,(30,(self.get_height() - self.title.get_height())/2))
			self.parent.blit(self,self.parent_offset)
class SelectableList(Surface):
	def __init__(self,width,items,type,viewpoint):
		Surface.__init__(self,(width,30*len(items)))
		self.items = []
		for item in items:
			surface = IDSurface(item,(width,30))
			surface.fill(menu_theme.not_selected_colour)
			surface.blit(Font("Geneva",15).render(item,menu_theme.text_colour),(10,10))
			self.blit(surface,(0,30*len(self.items)))
			self.items.append(surface)
		self.type = type
		self.viewpoint = viewpoint
		self.last_selected_x = None
	def loop(self,mouse_pos,event):
		for x in range(len(self.items)):
			if self.type == 1:
				if self.items[x].id == "No acceptable images in this folder":
					break
			elif self.type == 2:
				if self.items[x].id == "No maps":
					break
			if self.items[x].get_offset()[1] + 30 > self.viewpoint.viewport.get_offset()[1] and self.items[x].get_offset()[1] < self.viewpoint.viewport.get_offset()[1] + self.viewpoint.viewport.get_height():
				select_end = True
				if self.type in [1,2] and self.last_selected_x is not None:
					if self.items[self.last_selected_x] == self.items[x]:
						select_end = False
				if point_collide(mouse_pos,self.items[x]):
					if event[0] == MOUSEUP and event[1] == LEFT_MOUSE_BUTTON:
						if self.type in [1,2] and self.last_selected_x != x:
							if self.last_selected_x is not None:
								self.items[self.last_selected_x].fill(menu_theme.not_selected_colour)
								self.items[self.last_selected_x].blit(Font("Geneva",15).render(self.items[self.last_selected_x].id,menu_theme.text_colour),(10,10))
								self.viewpoint.contents.blit(self.items[self.last_selected_x],(0,30*self.last_selected_x))
								self.items[self.last_selected_x].selected = False
							self.last_selected_x = x
						if self.type != 2:
							return x
						else:
							return self.items[x].id
						break
					elif event[0] == MOUSEMOTION and self.items[x].selected == False:
						self.items[x].fill(menu_theme.selected_colour)
						self.items[x].blit(Font("Geneva",15).render(self.items[x].id,menu_theme.text_colour),(10,10))
						self.viewpoint.contents.blit(self.items[x],(0,30*x))
						self.items[x].selected = True
				elif self.items[x].selected == True and select_end:
					self.items[x].fill(menu_theme.not_selected_colour)
					self.items[x].blit(Font("Geneva",15).render(self.items[x].id,menu_theme.text_colour),(10,10))
					self.viewpoint.contents.blit(self.items[x],(0,30*x))
					self.items[x].selected = False
class FileBrowser(Surface):
	def __init__(self):
		#File browser
		Surface.__init__(self,(1000,600))
		self.fill(list(menu_theme.not_selected_colour) + [200])
		self.round_corners(30)
		title = Font("Geneva",20).render("Select a background image (2000x2000px - 9000x9000px)",menu_theme.text_colour)
		self.blit(title,((self.get_width() - title.get_width())/2,15))
		#Folders
		self.folder_viewpoint = ViewPoint((370,520),"Folders",(20,50),self)
		#Files
		self.file_viewpoint = ViewPoint((560,460),"Files",(420,50),self)
		#Cancel Button
		self.cancel_button = MapmakerRoundButton((420,530),(270,50),"Cancel",self)
		#Select Button
		self.select_button = MapmakerRoundButton((710,530),(270,50),"Select",self)
		self.list_directory(game.homedir)
	def loop(self,mouse_pos,event):
		self.folder_viewpoint.mouse(mouse_pos,event)
		self.file_viewpoint.mouse(mouse_pos,event)
		if self.cancel_button.mouse(mouse_pos,event):
			return "CANCEL"
		if self.select_button.mouse(mouse_pos,event) and self.files_surface.last_selected_x is not None:
			return self.current_dir + "/" + self.files_surface.items[self.files_surface.last_selected_x].id
		x = self.folders_surface.loop(mouse_pos,event)
		if x is not None:
			if self.folders_surface.items[x].id == "../":
				self.list_directory(os.path.dirname(self.current_dir[:-1]))
			else:
				self.list_directory(self.current_dir + "/" + self.folders_surface.items[x].id)
		self.files_surface.loop(mouse_pos,event)
	def list_directory(self,dir):
		self.folder_viewpoint.scrollbar.pos = 0
		self.folder_viewpoint.scrollbar.render()
		self.current_dir = dir
		files = []
		for file in os.listdir(dir):
			if file[-4:] in [".png",".jpg","jpeg"]:
				image_size = Image.open(dir + "/" + file).size
				if image_size[0] >= 2000 and image_size[1] >= 2000 and image_size[0] <= 9000 and image_size[1] <= 9000:
					files.append(file)
		if len(files) == 0:
			files.append("No acceptable images in this folder")
		folders = (["../"] if dir != "/" else []) + [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f)) and f[0] != "."]
		self.folders_surface = SelectableList(340,folders,0,self.folder_viewpoint)
		self.files_surface =  SelectableList(540,files,1,self.file_viewpoint)
		self.folder_viewpoint.add_to_view_point(self.folders_surface)
		self.folder_viewpoint.render()
		self.file_viewpoint.add_to_view_point(self.files_surface)
		self.file_viewpoint.render()
class MapmakerInput(Surface):
	objects = []
	font = Font("Geneva",15)
	def __init__(self,size,max,surface,offset):
		self.objects.append(self)
		Surface.__init__(self,(size,40))
		self.fill(menu_theme.text_colour)
		self.round_corners(20)
		self.inner = Surface((size - 10,30))
		self.inner.fill(menu_theme.not_selected_colour)
		self.inner.round_corners(15)
		self.text_surface =  Surface((size - 30,21))
		self.text = ""
		self.surface = surface
		self.max = max
		self.offset = offset
		self.do_render = True
		self.selected = False
		self.cursor_show = False
		self.in_cursor_loop = False
	def cursor(self):
		self.in_cursor_loop = True
		self.cursor_show = False #Show cursor to begin with (Will invert directly after)
		while 1:
			self.do_render = True #Render on next call to render function because of cursor change
			if self.selected:
				self.cursor_show = not self.cursor_show #Invert variable so cursor will change on the next render
				time.sleep(0.6) #Wait 0.6 seconds until next iteration
			else:
				self.cursor_show = False
				break #End cursor blinking
		self.in_cursor_loop = False
	def render(self):
		if self.do_render:
			chars = []
			offset = 0
			full = False
			for char in ''.join(list((self.text + "|") if self.cursor_show else self.text)[::-1]):
				chars.append(self.font.render(char,menu_theme.text_colour))
				if char != "|":
					offset += chars[-1].get_width()
				if offset > self.text_surface.get_width():
					full = True
					break
			offset = 10 if self.cursor_show and full else 14
			self.text_surface.fill(menu_theme.not_selected_colour)
			if full:
				for char in chars:
					offset += char.get_width()
					self.text_surface.blit(char,(self.text_surface.get_width() - offset,0))
			else:
				for char in chars[::-1]:
					self.text_surface.blit(char,(offset,0))
					offset += char.get_width()
			self.inner.blit(self.text_surface,(10,7))
			self.blit(self.inner,(5,5))
			self.surface.blit(self,self.offset)
			self.do_render = False
	def loop(self,mouse_pos,event):
		return_val = False
		if event[0] == MOUSEUP:
			if event[1] == LEFT_MOUSE_BUTTON:
				if point_collide(mouse_pos,self):
					self.selected = True
					if not self.in_cursor_loop:
						Thread(self.cursor)
				else:
					self.selected = False
		if self.selected:
			if event[0] == KEYDOWN:
				letter = ""
				if ord(event[1]) != KEY_BACKSPACE:
					letter = event[1]
				elif self.text:
					self.text = self.text[:-1]
				if len(self.text) < self.max and len(letter) == 1 and not ord(event[1]) in  [63272,63236,63237,63238,63239,63240,63242,63232,63233,63234,63235,127] and ord(event[1]) > 31: #Those keys are control characters
					self.text += letter
				return_val = True
				self.do_render = True
		return return_val
class MapBrowser(Surface):
	def __init__(self,save):
		Surface.__init__(self,(500,600))
		self.fill(list(menu_theme.not_selected_colour) + [200])
		self.round_corners(30)
		title = (Font("Geneva",20).render("Save" if save else "Load",menu_theme.text_colour))
		self.blit(title,((self.get_width() - title.get_width())/2,15))
		if save:
			#Name
			self.blit(Font("Geneva",15).render("Name",menu_theme.text_colour),(25,60))
			self.map_name = MapmakerInput(370,30,self,(110,50))
		#Maps
		self.maps_viewpoint = ViewPoint((450,350 if save else 400),"Saved Maps",(20,100 if save else 50),self)
		#Select Button
		self.select_button = MapmakerRoundButton((20,470),(460,50),"Select",self)
		#Cancel Button
		self.cancel_button = MapmakerRoundButton((20,530),(460,50),"Cancel",self)
		maps = []
		for map in os.listdir(game.homedir + "/TimeSplitters Platinum Custom Maps"):
			if os.path.isdir(game.homedir + "/TimeSplitters Platinum Custom Maps/" + map): #Only allow folders which will be the maps
				maps.append(map)
		if not maps:
			maps.append("No maps")
		self.maps_surface = SelectableList(450,maps,2,self.maps_viewpoint)
		self.maps_viewpoint.add_to_view_point(self.maps_surface)
		self.maps_viewpoint.render()
		self.save = save
	def loop(self,mouse_pos,event):
		self.maps_viewpoint.mouse(mouse_pos,event)
		if self.select_button.mouse(mouse_pos,event):
			if self.save:
				return self.map_name.text
			elif self.maps_surface.last_selected_x is not None:
				return self.maps_surface.items[self.maps_surface.last_selected_x].id
		if self.cancel_button.mouse(mouse_pos,event):
			return "CANCEL"
		map = self.maps_surface.loop(mouse_pos,event)
		if self.save:
			if map is not None and len(map) < 41:
				self.map_name.text = map
				self.map_name.render()
			self.map_name.loop(mouse_pos,event)
class DropDownBox():
	current_open = None
	def __init__(self,position,size,items,parent,drop_down_pos,default = 0):
		#List surface
		self.items = Surface((size[0],610))
		self.items.fill(list(menu_theme.not_selected_colour) + [200])
		self.items.round_corners(40)
		self.items_viewpoint = ViewPoint((size[0] - 30,580),"Select an option...",(10,10),self.items)
		self.items_list = SelectableList(580,items,3,self.items_viewpoint)
		self.items_viewpoint.add_to_view_point(self.items_list)
		self.items_viewpoint.render()
		#Closed surface
		self.box_button = MapmakerRoundButton(position,size,items[default],parent)
		self.closed = True
		self.parent = parent
		self.position = position
		self.default = default
		self.size = size
		self.item_list = items
		self.drop_down_pos = drop_down_pos
	def loop(self,mouse_pos,event):
		if self.closed:
			if self.box_button.mouse(mouse_pos,event):
				if DropDownBox.current_open is not None:
					DropDownBox.current_open.closed = True
				DropDownBox.current_open = self
				self.closed = False
		else:
			self.items_viewpoint.mouse(mouse_pos,event)
			item = self.items_list.loop(mouse_pos,event)
			if item is not None:
				self.closed = True
				self.box_button = MapmakerRoundButton(self.position,self.size,self.item_list[item],self.parent)
				return item
	def render(self):
		if not self.closed:
			game.blit(self.items,self.drop_down_pos)
class Options(Surface):
	def __init__(self):
		Surface.__init__(self,(500,370))
		self.fill(list(menu_theme.not_selected_colour) + [200])
		self.round_corners(30)
		title = (Font("Geneva",20).render("Options",menu_theme.text_colour))
		self.blit(title,((self.get_width() - title.get_width())/2,15))
		option_font = Font("Geneva",15)
		self.blit(option_font.render("Music",menu_theme.text_colour),(20,60))
		self.blit(option_font.render("Weapon 1",menu_theme.text_colour),(20,100))
		self.blit(option_font.render("Weapon 2",menu_theme.text_colour),(20,140))
		self.blit(option_font.render("Weapon 3",menu_theme.text_colour),(20,180))
		self.blit(option_font.render("Weapon 4",menu_theme.text_colour),(20,220))
		self.blit(option_font.render("Weapon 5",menu_theme.text_colour),(20,260))
		self.blit(option_font.render("Description (200 chars)",menu_theme.text_colour),(20,320))
		self.description_input = MapmakerInput(280,200,self,(200,310))
		self.music = [file[:-4] for file in os.listdir(os.path.dirname(sys.argv[0]) + "/music/game/") if file[-4:] == ".ogg"]
		self.make_boxes()
	def make_boxes(self):
		self.muisc_box = DropDownBox((150,55),(330,35),self.music,self,(920,60))
		self.weapon_boxes = [None,None,None,None,None]
		self.weapon_boxes[0] = DropDownBox((150,95),(330,35),weapon_list,self,(920,60))
		self.weapon_boxes[1] = DropDownBox((150,135),(330,35),weapon_list,self,(920,60),1)
		self.weapon_boxes[2] = DropDownBox((150,175),(330,35),weapon_list,self,(920,60),2)
		self.weapon_boxes[3] = DropDownBox((150,215),(330,35),weapon_list,self,(920,60),3)
		self.weapon_boxes[4] = DropDownBox((150,255),(330,35),weapon_list,self,(920,60),4)
	def change_level(self,level,level_information):
		self.level = level
		level.recomended_muisc = 0
		for x in xrange(5):
			level.weapons[x] = x + 1
		self.make_boxes()
		self.description_input.text = level_information.description
		self.description_input.do_render = True
	def render(self):
		result = self.muisc_box.render()
		for x in xrange(5):
			result = self.weapon_boxes[x].render()
	def loop(self,mouse_pos,event,mapmaker):
		result = self.muisc_box.loop(mouse_pos,event)
		if result is not None:
			self.level.recomended_muisc = result
		for x in xrange(5):
			result = self.weapon_boxes[x].loop(mouse_pos,event)
			if result is not None:
				self.level.weapons[x] = result + 1
				mapmaker.game_items[3 + x] = weapon_list[result]
				mapmaker.game_items[8 + x] = weapon_list[result] + " Ammo"
				mapmaker.items_list = SelectableList(580,mapmaker.game_items,3,mapmaker.items_viewpoint)
				mapmaker.items_viewpoint.add_to_view_point(mapmaker.items_list)
				mapmaker.items_viewpoint.render(mapmaker.items_viewpoint.scrollbar.get_pos())
				mapmaker.item_img[3+x] = 0
				mapmaker.item_img[8+x] = 0
		if self.description_input.loop(mouse_pos,event):
			mapmaker.level_information.description = self.description_input.text
		self.description_input.render()
		print "end loop opt"
class IDSurface(Surface):
	def __init__(self,id,*args):
		Surface.__init__(self,*args)
		self.id = id
		self.selected = False
#Section classes. __init__ on first initilistation, transfer when section changes, loop per frame and exit when games quits during section
class Mapmaker():
	#Creates levels with a GUI
	music = ""
	story_lines = [(50, 40), (50, 140), (50, 40), (24.019237880568905, 25), (50, 40), (84.64101615924146, 20), (50, 60), (24.019237880568905, 45), (50, 60), (84.64101615924146, 40), (50, 80), (24.019237880568905, 65), (50, 80), (84.64101615924146, 60), (50, 100), (24.019237880568905, 85), (50, 100), (84.64101615924146, 80), (50, 120), (24.019237880568905, 105), (50, 120), (84.64101615924146, 100), (50, 140), (24.019237880568905, 125), (50, 140), (84.64101615924146, 120), (84.64101615924146, 20), (58.660254039810368, 5), (24.019237880568905, 25), (58.660254039810368, 5), (84.64101615924146, 20), (84.64101615924146, 120), (24.019237880568905, 25), (24.019237880568905, 125)]
	story_edges = [(58.660254039810368,5),(24.019237880568905, 25),(24.019237880568905, 125),(50,140),(84.64101615924146, 120),(84.64101615924146, 20)]
	single_story_edges = [(50,40),(24.019237880568905, 25),(24.019237880568905, 45),(50,60),(84.64101615924146, 40),(84.64101615924146, 20)]
	story_indicator = Surface((100,150))
	story_indicator.set_background_alpha(0)
	def init(self):
		start_notice_text = Font("Geneva",15).render_wordwrap('Welcome to the Mapmaker!\n\n This mapmaker allows you to create your own maps, either for your own pleasure or to share to whoever you like.\n\nBefore you can use this mapmaker you will need to have created some background images for the stories. You can have up to 5 stories, 9000 by 9000 pixels each. The screen resolution is 1280x720 pixels and the characters are roughly 100 pixels wide. \n\n If this is the first time making a level, maybe you will want to figure how to make maps for yourself. In that case, just press "New" over at the top-left. It is likely you will need to press the help button if you become clueless.',630, menu_theme.text_colour,1)
		self.start_notice = Surface((650,start_notice_text.get_height() + 20))
		self.start_notice.fill(list(menu_theme.not_selected_colour) + [200])
		self.start_notice.blit(start_notice_text,(10,10))
		self.start_notice.round_corners(30)
		image_notice_text = Font("Geneva",15).render_wordwrap('This story has no background image. To add one, press the "New Image" button.',240, menu_theme.text_colour,1)
		self.image_notice = Surface((260,image_notice_text.get_height() + 20))
		self.image_notice.fill(list(menu_theme.not_selected_colour) + [200])
		self.image_notice.blit(image_notice_text,(10,10))
		self.image_notice.round_corners(30)
	def make_button(self,name,title = False):
		button = MapmakerButton(name,title,self.bar)
		self.buttons.append(button)
		return button
	def transfer(self,level=None,preview = False):
		if preview:
			self.section = MMS_NAV
			self.nav_button.render(True)
			self.preview_button.render(False)
			for floor in self.level.floors:
				floor.add_image(floor.imgfile)
			game.window.set_exclusive_mouse(False)
		else:
			game.enable_mouse()
			game.show_cursor()
			self.focus = True
			self.buttons = []
			MapmakerButton.end_offset = 0
			self.bar = Surface((1280,25))
			self.background = Surface((1280,720))
			self.background.fill([float(c)/4.0 for c in menu_theme.not_selected_colour])
			for x in xrange(19,1280,20):
				for y in [-1,+1]:
					add_line(self.background, menu_theme.not_selected_colour, (x+y,0), (x+y,720))
			for x in xrange(19,720,20):
				for y in [-1,+1]:
					add_line(self.background, menu_theme.not_selected_colour, (0,x+y), (1280,x+y))
			for x in xrange(19,1280,20):
				add_line(self.background, menu_theme.selected_colour, (x,0), (x,720))
			for x in xrange(19,720,20):
				add_line(self.background, menu_theme.selected_colour, (0,x), (1280,x))
			self.bar.fill((255,255,255,240))
			self.edit_area = Surface((1280,695))
			self.edit_area.set_background_alpha(0)
			self.make_button("  Mapmaker   ",True)
			self.new_button = self.make_button("New")
			self.open_button = self.make_button("Open")
			self.save_button = self.make_button("Save")
			self.image_button = self.make_button("New Image")
			self.nav_button = self.make_button("Navigation Hand")
			self.drag_button = self.make_button("Select Hand")
			self.wall_button = self.make_button("Wall Tool")
			self.stairs_button = self.make_button("Floor Tools")
			self.items_button = self.make_button("Items")
			self.options_button = self.make_button("Options")
			self.preview_button = self.make_button("Preview")
			self.exit_button = self.make_button("Exit")
			self.bar.set_background_alpha(0)
			self.colour_bar = Surface((383,25))
			zoom_img = open_image(os.path.dirname(sys.argv[0]) + "/images/mapmaker_images/magnify.png")
			self.colour_bar.fill(list(menu_theme.not_selected_colour) + [255])
			self.colour_bar.blit(zoom_img,(154,3))
			self.bar.blit(self.colour_bar,(896,0))
			self.selected_button = None
			for button in self.buttons:
				button.render(False)
			self.section = MMS_NO_IMG
			self.level = False
			self.file_browser = FileBrowser()
			self.enter = False
			#Zoom scrollbar
			self.zoom_scrollbar = Scrollbar(191,(1084,2),self.bar,1,75)
			self.new_wall = []
			self.new_wall_end = 0
			self.nav_move = 4
			#Open
			self.open_browser = MapBrowser(False)
			#Save
			self.save_browser = MapBrowser(True)
			#Items
			self.items = Surface((410,610))
			self.items.fill(list(menu_theme.not_selected_colour) + [200])
			self.items.round_corners(40)
			self.items_viewpoint = ViewPoint((380,580),"Items",(10,10),self.items)
			self.game_items = ["Spawn Point","Red Spawn Point","Blue Spawn Point","AK-47","Garrett Revolver","Shotgun","Minigun","None","AK-47 Ammo","Garrett Revolver Ammo","Shotgun Ammo","Minigun Ammo","None Ammo","Health Low","Health High","Armour Low","Armour High","Explosive Barrel"]
			self.items_list = SelectableList(380,self.game_items,3,self.items_viewpoint)
			self.items_viewpoint.add_to_view_point(self.items_list)
			self.items_viewpoint.render()
			self.item_img = [0] * 18
			#Options
			self.options_menu = Options()
			#Floor tools
			self.floor_tools = Surface((410,130))
			self.floor_tools.fill(list(menu_theme.not_selected_colour) + [200])
			self.floor_tools.round_corners(40)
			self.floor_tools_frame = Frame((380,100),(10,10),self.floor_tools)
			self.floor_tools_list = SelectableList(380,["Stairs/slope","Stairs/Slope (Parallel)","Hole","Transparency"],3,self.floor_tools_frame)
			self.floor_tools_frame.add_to_frame(self.floor_tools_list)
			self.floor_tools_frame.render()
			#Stairs/Slope tool
			self.current_connector_coordinates = [False,False,False,False]
			self.next_floor_connector_point = (0,0)
			self.selected_connector_coordinates = None
			#Hole and Transparency
			self.current_box = [False,False,False,False]
			self.selected_box = None
			#Others
			self.up_key_down = False
			self.down_key_down = False
			self.current_zoom = 1
	def loop(self):
		game.blit(self.background,(0,0))
		for object in MapmakerInput.objects:
			object.render() #Constant call to render function for cursor blinking. Required on main thread for some reason.
		if not self.level:
			game.blit(self.start_notice,((game.get_width() - self.start_notice.get_width())/2,(game.get_height() - self.start_notice.get_height())/2))
		else:
			if self.current_floor.image is not None:
				game.blit(self.current_floor.image,self.pos)
			if self.section == MMS_NO_IMG:
				game.blit(self.image_notice,((game.get_width() - self.image_notice.get_width())/2,(game.get_height() - self.image_notice.get_height())/2))
			if not self.section in [MMS_NEW_IMG,MMS_STAIRS,MMS_FLOOR_TOOLS]:
				if game.key(KEY_UP):
					if self.story != 4 and not self.up_key_down:
						self.story += 1
						self.change_floor()
						self.up_key_down = True
				else:
					self.up_key_down = False
				if game.key(KEY_DOWN):
					if self.story != 0 and not self.down_key_down:
						self.story -= 1
						self.change_floor()
						self.down_key_down = True
				else:
					self.down_key_down = False
		game.blit(self.bar,(0,0))
		self.bar.blit(self.colour_bar,(896,0))
		self.zoom_scrollbar.render()
		self.edit_area.fill((0,0,0))
		if self.section == MMS_NEW_IMG:
			game.blit(self.file_browser,(140,60))
		elif self.section in [MMS_WALL,MMS_DRAG]:
			for pos in self.new_wall:
				#Add points
				pos = self.get_edit_position(pos)
				Particles([pos],16,(0,0,255),self.edit_area)
			for level_pos in xrange(len(self.new_wall) -1):
				add_line(self.edit_area, (0,0,255),self.get_edit_position(self.new_wall[level_pos]), self.get_edit_position(self.new_wall[level_pos+ 1]),4)
			if self.new_wall and self.new_wall_end != 0:
				add_line(self.edit_area, (0,0,255),self.get_edit_position(self.new_wall[-1]), self.get_edit_position(self.new_wall_end),4)
			for wall in self.current_floor.walls:
				for pos in wall:
					#Add points
					pos = self.get_edit_position(pos)
					Particles([pos],16,(255,0,0),self.edit_area)
				for level_pos in xrange(len(wall) -1):
					add_line(self.edit_area, (255,0,0),self.get_edit_position(wall[level_pos]), self.get_edit_position(wall[level_pos+ 1]),4)
		if self.section in [MMS_ITEMS,MMS_DRAG]:
			for item in self.current_floor.items:
				if not self.item_img[item[ITEM_ID]]:
					if item[ITEM_ID] < 3 or item[ITEM_ID] > 12:
						self.item_img[item[ITEM_ID]] = open_image(os.path.dirname(sys.argv[0]) + "/images/items/" + str(item[ITEM_ID]) + ".png")
					elif item[ITEM_ID] < 8:
						self.item_img[item[ITEM_ID]] = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.level.weapons[item[ITEM_ID] - 3]) + "/pickup.png")
					else:
						self.item_img[item[ITEM_ID]] = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.level.weapons[item[ITEM_ID] - 8]) + "/ammo.png")
				item_pos = self.get_edit_position((item[ITEM_POS][0] - self.item_img[item[ITEM_ID]].get_width()/2,item[ITEM_POS][1] - self.item_img[item[ITEM_ID]].get_height()/2))
				self.edit_area.blit(self.item_img[item[ITEM_ID]],item_pos)
				if item[ITEM_IMG] is not None:
					self.arrow(item[ITEM_POS],item[ITEM_IMG],(255,0,0))
				if self.item_selected == item:
					add_line(self.edit_area, (0,0,255),item_pos,(item_pos[0],item_pos[1] + self.item_img[item[ITEM_ID]].get_height()),3)
					add_line(self.edit_area, (0,0,255),item_pos,(item_pos[0] + self.item_img[item[ITEM_ID]].get_width(),item_pos[1]),3)
					add_line(self.edit_area, (0,0,255),(item_pos[0],item_pos[1] + self.item_img[item[ITEM_ID]].get_height()),(item_pos[0] + self.item_img[item[ITEM_ID]].get_width(),item_pos[1] + self.item_img[item[ITEM_ID]].get_height()),3)
					add_line(self.edit_area, (0,0,255),(item_pos[0] + self.item_img[item[ITEM_ID]].get_width(),item_pos[1]),(item_pos[0] + self.item_img[item[ITEM_ID]].get_width(),item_pos[1] + self.item_img[item[ITEM_ID]].get_height()),3)
			if self.item_drag is not None and self.section != MMS_DRAG:
				self.edit_area.blit(self.item_image,self.get_edit_position((self.item_pos[0] - self.item_image.get_width()/2,self.item_pos[1] - self.item_image.get_height()/2)))
				if self.item_down and self.item_angle is not None:
					self.arrow(self.item_pos,self.item_angle,(0,0,255))
		if not self.section in [MMS_NO_IMG,MMS_NEW_IMG,MMS_NAV,MMS_OPEN,MMS_FLOOR_TOOLS,MMS_OPTIONS]:
			move = True
			if self.nav_move == 0:
				self.pos[0] += self.nav_move_amount
			elif self.nav_move == 1:
				self.pos[1] += self.nav_move_amount
			elif self.nav_move == 2:
				self.pos[0] += self.nav_move_amount
			elif self.nav_move == 3:
				self.pos[1] += self.nav_move_amount
			else:
				move = False
			if move:
				self.reposition()
		if self.section in [MMS_STAIRS,MMS_DRAG]:
			if self.current_connector_coordinates[0]:
				#Show first
				coordinates = [self.get_edit_position(self.current_connector_coordinates[0])]
				if self.current_connector_coordinates[1]:
					#Show second
					coordinates.append(self.get_edit_position(self.current_connector_coordinates[1]))
					add_line(self.edit_area, (0,0,255),coordinates[0],coordinates[1],3)
					if self.current_connector_coordinates[2]:
						#Show third
						coordinates.append(self.get_edit_position(self.current_connector_coordinates[2]))
						add_line(self.edit_area,(0,0,255),coordinates[2],self.get_edit_position(self.next_floor_connector_point),3)
				else:
					add_line(self.edit_area, (0,0,255),coordinates[0],self.get_edit_position(self.next_floor_connector_point),3)
				Particles(coordinates,16,(0,0,255),self.edit_area)
			x = 0
			for connector_coordinates in self.current_floor.connectors + self.level.floors[self.story - 1].connectors:
				if self.selected_connector_coordinates == x:
					colour = (0,0,255)
				else:
					colour = (255,0,0)
				add_line(self.edit_area, colour,self.get_edit_position(connector_coordinates[0]),self.get_edit_position(connector_coordinates[1]),3)
				add_line(self.edit_area, colour,self.get_edit_position(connector_coordinates[2]),self.get_edit_position(connector_coordinates[3]),3)
				Particles([self.get_edit_position(coordinate) for coordinate in connector_coordinates],16, colour,self.edit_area)
				middle1 = ((connector_coordinates[0][0] + connector_coordinates[1][0])/2,(connector_coordinates[0][1] + connector_coordinates[1][1])/2)
				middle2 = ((connector_coordinates[2][0] + connector_coordinates[3][0])/2,(connector_coordinates[2][1] + connector_coordinates[3][1])/2)
				direction_vector = ((middle2[0] - middle1[0])/10,(middle2[1] - middle1[1])/10)
				start = ((connector_coordinates[0][0] + connector_coordinates[1][0])/2 + direction_vector[0],(connector_coordinates[0][1] + connector_coordinates[1][1])/2 + direction_vector[1])
				direction_vector = (direction_vector[0]*8,direction_vector[1]*8)
				end = (start[0] + direction_vector[0],start[1] + direction_vector[1])
				add_line(self.edit_area, colour,self.get_edit_position(start),self.get_edit_position(end),3)
				direction_vector = (direction_vector[0]/8,direction_vector[1]/8)
				arrow_back = (end[0] - direction_vector[0],end[1] - direction_vector[1])
				direction_vector = (direction_vector[0]/2,direction_vector[1]/2)
				p1 = (arrow_back[0] + direction_vector[1],arrow_back[1] - direction_vector[0])
				p2 = (arrow_back[0] - direction_vector[1],arrow_back[1] + direction_vector[0])
				add_line(self.edit_area, colour,self.get_edit_position(end),self.get_edit_position(p1),3)
				add_line(self.edit_area, colour,self.get_edit_position(end),self.get_edit_position(p2),3)
				x += 1
		if self.section in [MMS_HOLE,MMS_TRANSPARENT,MMS_DRAG]:
			if self.current_box[0]:
				self.current_box[1] = [self.next_floor_connector_point[0],self.current_box[0][1]]
				self.current_box[2] = self.next_floor_connector_point
				self.current_box[3] = [self.current_box[0][0],self.next_floor_connector_point[1]]
				points = [self.get_edit_position(x) for x in self.current_box]
				points.append(points[0])
				add_lines(self.edit_area, (0,0,255),points,3)
				Particles(points[:-1],16,(0,0,255),self.edit_area)
			if self.section == MMS_HOLE:
				boxes = self.current_floor.holes
			elif self.section == MMS_TRANSPARENT:
				boxes = self.current_floor.transparent_boxes
			else:
				boxes =  self.current_floor.holes + self.current_floor.transparent_boxes
			x = len(self.current_floor.connectors) + len(self.level.floors[self.story - 1].connectors)
			for box_coordinates in boxes:
				if x == self.selected_connector_coordinates:
					colour = (0,0,255)
				else:
					colour = (255,0,0)
				box_coordinates = [self.get_edit_position(c) for c in box_coordinates]
				box_coordinates.append(box_coordinates[0])
				add_lines(self.edit_area,colour,box_coordinates,3)
				Particles(box_coordinates[:-1],16,colour,self.edit_area)
				x += 1
		if game.events:
			mouse_pos = get_mouse_pos(game.mouse_pos())
			if not self.section in [MMS_NO_IMG,MMS_NEW_IMG,MMS_OPEN,MMS_FLOOR_TOOLS]:
				if self.current_zoom != 0:
					level_cursor_position = self.get_level_position(mouse_pos)
		for event in game.events:
			if (event[0] == MOUSEMOTION or event[0] == MOUSEUP or event[0] == MOUSEDOWN):
				if self.zoom_scrollbar.mouse(mouse_pos,event[0]) and self.section not in [MMS_NO_IMG,MMS_NEW_IMG,MMS_OPEN]:
					self.reposition()
				self.stop_bar = True
				if self.section == MMS_NEW_IMG: #New Image
					result = self.file_browser.loop(mouse_pos,event)
					if result is not None:
						self.focus = True
						if result == "CANCEL":
							self.section = self.last_section
							self.new_button.render(False)
						else:
							self.section = MMS_NAV
							self.drag_hand = False
							self.current_floor.add_image(result)
							self.new_button.render(False)
							self.selected_button = self.nav_button
							self.nav_button.render(True)
							self.current_zoom = 1
							self.start_wall = 0
							self.reposition()
				elif self.section == MMS_NAV: #Navigation
					if not self.drag_hand:
						self.focus = True
					if point_collide(mouse_pos,self.edit_area) and event[0] == MOUSEDOWN:
						if event[1] == LEFT_MOUSE_BUTTON:
							self.drag_hand = True
							self.focus = False
					elif self.drag_hand:
						if event[0] == MOUSEUP:
							self.drag_hand = False
						else:
							self.pos[0] += event[1] * 2
							self.pos[1] += event[2] * 2
							self.reposition()
				elif self.section == MMS_DRAG: #Select hand
					if self.enter:
						self.drag_wall_point = None
						self.new_wall_end = 0
						self.wall_selected = False
						self.enter = False
					done = False
					if event[0] == MOUSEUP:
						if self.drag_wall_point is not None:
							self.drag_wall_point = None
							self.current_floor.add_wall(self.new_wall)
							self.new_wall = []
						if self.item_drag is not None:
							self.item_selected = self.item_drag
							self.item_drag = None
						elif self.item_selected is not None:
							self.item_selected = None
					elif event[0] == MOUSEMOTION:
						if self.drag_wall_point is not None:
							self.new_wall[self.drag_wall_point] = level_cursor_position
							self.stop_bar = False
						elif self.item_drag is not None:
							self.item_drag = level_cursor_position
					if event[0] == MOUSEDOWN:
						was_selected = self.wall_selected
						self.wall_selected = False
						if event[1] == LEFT_MOUSE_BUTTON:
							#Walls
							for w in xrange(len(self.current_floor.walls)):
								prior_pos = False
								for x in xrange(len(self.current_floor.walls[w])):
									#Add points
									pos = self.get_screeen_position(self.current_floor.walls[w][x])
									if pygame.Rect((pos[0] - 8,pos[1] -8),(16,16)).collidepoint(mouse_pos):
										self.edit_wall(w)
										self.drag_wall_point = x
										done = True
										break
									if prior_pos:
										if intersect(pos,prior_pos,(mouse_pos[0] + 3,mouse_pos[1]),(mouse_pos[0] - 3,mouse_pos[1])) or  intersect(pos,prior_pos,(mouse_pos[0],mouse_pos[1]- 22),(mouse_pos[0],mouse_pos[1]-28)):
											self.edit_wall(w)
											self.wall_selected = True
											done = True
											break
									prior_pos = pos
								if done == True:
									break
							#Stairs/slope connector
							x = 0
							found = False
							for connector_coordinates in self.current_floor.connectors + self.level.floors[self.story - 1].connectors + self.current_floor.holes + self.current_floor.transparent_boxes:
								prior_pos = False
								for coordinate in connector_coordinates:
									pos = self.get_screeen_position(coordinate)
									if pygame.Rect((pos[0] - 8,pos[1] -8),(16,16)).collidepoint(mouse_pos):
										found = True
									elif prior_pos:
										if intersect(pos,prior_pos,(mouse_pos[0] + 3,mouse_pos[1]),(mouse_pos[0] - 3,mouse_pos[1])) or  intersect(pos,prior_pos,(mouse_pos[0],mouse_pos[1]- 22),(mouse_pos[0],mouse_pos[1]-28)):
											found = True
									if found:
										self.selected_connector_coordinates = x
										break
									prior_pos = pos
								x += 1
								if found:
									break
							if not found:
								self.selected_connector_coordinates = None
							#Items
							if not self.wall_selected: #Don't do both at the same time
								for item in xrange(len(self.current_floor.items)):
									pos = self.get_screeen_position(self.current_floor.items[item][ITEM_POS])
									if Rect((pos[0]-25,pos[1] - 25),(50,50)).collidepoint(mouse_pos):
										self.item_drag = self.current_floor.items[item]
										self.item_no = item
						if was_selected and not self.wall_selected:
							self.current_floor.add_wall(self.new_wall)
							self.new_wall = []									
				elif self.section == MMS_WALL: #Wall tool
					if self.new_wall:
						self.stop_bar = False
					if event[0] == MOUSEUP and not point_collide(mouse_pos,self.bar):
						if event[1] == LEFT_MOUSE_BUTTON:
							if self.new_wall:
								if self.new_wall[-1] != level_cursor_position:
									self.new_wall.append(level_cursor_position)
								else:
									self.current_floor.add_wall(self.new_wall)
									self.new_wall = []
									self.nav_move = 4
							else:
								self.new_wall = [level_cursor_position]
					elif event[0] == MOUSEMOTION:
						self.new_wall_end = level_cursor_position
				elif self.section == MMS_FLOOR_TOOLS: #Selection for floor tools
					self.floor_tools_frame.render()
					item = self.floor_tools_list.loop(mouse_pos,event)
					if item is not None:
						if item in (0,1): #Stairs/Slope
							if self.story != 4 and self.level.floors[self.story + 1].image is not None:
								if item == 0:
									self.section = MMS_STAIRS
								else:
									self.section = MMS_STAIRS_PARALLEL
								self.current_connector_coordinates = [False,False,False,False]
						elif self.level.floors[self.story - 1].image is not None:
							if item == 2: #Hole
								self.section = MMS_HOLE
							else: #Transparency
								self.section = MMS_TRANSPARENT
				elif self.section in (MMS_STAIRS,MMS_STAIRS_PARALLEL): #Stairs/slope connector tool
					if event[0] == MOUSEUP and not point_collide(mouse_pos,self.bar):
						if event[1] == LEFT_MOUSE_BUTTON:
							if not self.current_connector_coordinates[0]:
								self.current_connector_coordinates[0] = self.next_floor_connector_point
							elif not self.current_connector_coordinates[1]:
								self.current_connector_coordinates[1] = self.next_floor_connector_point
								self.story += 1
								self.change_floor()
							elif not self.current_connector_coordinates[2]:
								self.current_connector_coordinates[2] = self.next_floor_connector_point
							else:
								self.current_connector_coordinates[3] = self.next_floor_connector_point
								self.story -= 1
								self.change_floor()
								self.current_floor.add_connector(self.current_connector_coordinates)
								self.current_connector_coordinates = [False,False,False,False]
					elif event[0] == MOUSEMOTION:
						if self.current_connector_coordinates[2] and self.section == MMS_STAIRS_PARALLEL:
							direction_vector = (self.current_connector_coordinates[0][0]-self.current_connector_coordinates[1][0],self.current_connector_coordinates[0][1]-self.current_connector_coordinates[1][1]) #This vector multiplied by a number gives the intersection
							perpendicular = (-direction_vector[1],direction_vector[0]) #With the perpendicular towards the mouse position
							self.next_floor_connector_point = vector_intersection(self.current_connector_coordinates[2],level_cursor_position,direction_vector,perpendicular)
						else:
							self.next_floor_connector_point = level_cursor_position
				elif self.section in [MMS_HOLE,MMS_TRANSPARENT]:
					if event[0] == MOUSEUP and not point_collide(mouse_pos,self.bar):
						if event[1] == LEFT_MOUSE_BUTTON:
							if not self.current_box[0]:
								self.current_box[0] = self.next_floor_connector_point
							else:
								self.current_box[2] = self.next_floor_connector_point
								self.current_floor.add_box(self.current_box,self.section)
								self.current_box= [False,False,False,False]
					elif event[0] == MOUSEMOTION:
						self.next_floor_connector_point = level_cursor_position
				elif self.section == MMS_ITEMS: #Items  
					if self.item_drag == None:
						self.items_viewpoint.mouse(mouse_pos,event)
						item = self.items_list.loop(mouse_pos,event)
						if item is not None:
							self.item_down = False
							self.item_drag = item
							if item < 3 or item > 12:
								self.item_image = open_image(os.path.dirname(sys.argv[0]) + "/images/items/" + str(item) + ".png")
							elif item < 8:
								self.item_image = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.level.weapons[item - 3]) + "/pickup.png")
							else:
								self.item_image = open_image(os.path.dirname(sys.argv[0]) +  "/weapons/" + str(self.level.weapons[item - 8]) + "/ammo.png")
							self.item_pos = level_cursor_position
					else:
						if event[0] == MOUSEDOWN and not point_collide(mouse_pos,self.bar):
							if event[1] == LEFT_MOUSE_BUTTON:
								self.item_down = True
								if self.item_drag in [0,1,2]: #All the items which can have an angle to them
									self.item_angle = 0
								else: #All items with no need for an angle
									self.item_angle = None
						if self.item_down:
							if event[0] == MOUSEUP:
								if event[1] == LEFT_MOUSE_BUTTON:
									self.current_floor.add_item(self.item_drag,self.item_pos,self.item_angle)
									self.item_drag = None
									self.item_down = False
						if event[0] == MOUSEMOTION:
							if self.item_down:
								pos = self.get_screeen_position(self.item_pos)
								if not Rect((pos[0] - self.item_image.get_width()/2,pos[1] - self.item_image.get_height()/2),self.item_image.get_size()).collidepoint(mouse_pos):
									self.item_angle = find_bearing(self.item_pos[0] - level_cursor_position[0],self.item_pos[1] - level_cursor_position[1])
									self.item_angle = 2*maths.pi - self.item_angle
							else:
								if level_cursor_position[0] > 0 and level_cursor_position[1] > 0 and level_cursor_position[0] < self.current_floor.image.get_width() - self.item_image.get_width() and level_cursor_position[1] < self.current_floor.image.get_height() - self.item_image.get_height():
									self.item_pos = level_cursor_position
				elif self.section == MMS_PREVIEW: #Preview
					fail = False
					if self.current_floor.items:
						if 0 in zip(*self.current_floor.items)[0]:
							for floor in self.level.floors:
								if floor.image is not None:
									floor.image.scale(floor.image.get_size())
							game.transfer_section(3,(self.level.recomended_muisc,self.level,MODE_DEATHMATCH,False,[0],self.level.weapons,0,False,False,[False,False,0,10]))
							#self.music,self.level,self.mode,self.radar,bot_list,self.weapon_list,self.player_character,self.friendly_fire,self.team_mode,self.mode_options
						else:
							fail = True
					else:
						fail = True
					if fail:
						self.section = self.last_section
				if event[0] == MOUSEMOTION and self.section > MMS_NEW_IMG:
					if mouse_pos[0] < 40:
						self.nav_move = 0
						self.nav_move_amount = 40 - mouse_pos[0]
					elif mouse_pos[1] < 40:
						self.nav_move = 1
						self.nav_move_amount = 40 - mouse_pos[1]
					elif mouse_pos[0] > 1240:
						self.nav_move = 2
						self.nav_move_amount = 1240 - mouse_pos[0]
					elif mouse_pos[1] > 680:
						self.nav_move = 3
						self.nav_move_amount = 680 - mouse_pos[1]
					else:
						self.nav_move = 4
					if point_collide(mouse_pos,self.bar) and (1 if self.stop_bar else mouse_pos[0] > 1050):
						self.nav_move = 4
			if self.section == MMS_WALL: #Wall tool
				if event[0] == KEYDOWN and len(self.new_wall) > 0:
					if event[1] == key.BACKSPACE: #Backspace
						del self.new_wall[-1]
					elif event[1] == key.DELETE:
						self.new_wall = []
			elif self.section == MMS_STAIRS: #Stairs/slope tool
				if event[0] == KEYDOWN:
					if event[1] == 8 or event[1] == key.DELETE:
						if self.current_connector_coordinates[1]:
							self.story -= 1
							self.change_floor()
						self.current_connector_coordinates = [False,False,False,False]
			elif self.section == MMS_DRAG: #Select Hand
				if event[0] == KEYDOWN:
					if event[1] == key.DELETE or event[1] == key.BACKSPACE:
						if self.wall_selected:
							self.new_wall = []
							self.wall_selected = False
						elif self.item_selected is not None:
							del self.current_floor.items[self.item_no]
							self.item_selected = None
						elif self.selected_connector_coordinates is not None:
							if self.selected_connector_coordinates < len(self.current_floor.connectors):
								del self.current_floor.connectors[self.selected_connector_coordinates]
							elif self.selected_connector_coordinates < len(self.current_floor.connectors) + len(self.level.floors[self.story - 1].connectors):
								del self.level.floors[self.story - 1].connectors[self.selected_connector_coordinates - len(self.current_floor.connectors)]
							elif self.selected_connector_coordinates < len(self.current_floor.connectors) + len(self.level.floors[self.story - 1].connectors) + len(self.current_floor.holes):
								del self.current_floor.holes[self.selected_connector_coordinates - len(self.current_floor.connectors) - len(self.level.floors[self.story - 1].connectors)]
							else:
								del self.current_floor.transparent_boxes[self.selected_connector_coordinates - len(self.current_floor.connectors) - len(self.level.floors[self.story - 1].connectors) - len(self.current_floor.holes)]
							self.selected_connector_coordinates = None
			elif self.section == MMS_OPEN: #Open
				result = self.open_browser.loop(mouse_pos,event)
				if result == "CANCEL":
					self.section = self.last_section
					self.focus = True
					self.open_button.render(False)
				elif result is not None:
					f = open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/level.dat", 'rb')
					self.level = pickle.loads(zlib.decompress(f.read()))
					f.close()
					f = open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/information.dat", 'rb')
					self.level_information = pickle.loads(f.read())
					f.close()
					for x in xrange(5):
						if self.level.floors[x].image is not None:
							image_file = game.homedir + "/TimeSplitters Platinum Custom Maps/.temp" + str(x) + "." + ("png" if self.level.floors[x].imgfile[:-3] == "png" else "jpg")
							image_data = open(image_file,"wb")
							image_data.write(self.level.floors[x].image)
							image_data.close()
							self.level.floors[x].add_image(image_file)
					self.options_menu.change_level(self.level,self.level_information)
					self.section = MMS_NAV
					self.focus = True
					self.open_button.render(False)
					self.selected_button = self.nav_button
					self.nav_button.render(True)
					self.current_zoom = 1
					self.start_wall = 0
					self.pos = [0,0]
					self.drag_hand = False
					self.story = 0
					self.change_floor()
			elif self.section == MMS_SAVE: #Save
				result = self.save_browser.loop(mouse_pos,event)
				if result == "CANCEL":
					self.section = MMS_NAV
					self.focus = True
					self.save_button.render(False)
					self.nav_button.render(True)
				elif result is not None:
					self.level_information.last_save = time.time() #Update save time
					#Make map directory if need be
					if not os.path.isdir(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result):
						os.mkdir(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result)
					#Thumbnails
					thumb_surface = Surface((100,100))
					thumb_surface.set_background_alpha(0)
					for x in xrange(5):
						if self.level.floors[x].thumb is not None:
							thumb_addr = game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/thumb" + str(x) + ".png"
							thumb_surface.blit(self.level.floors[x].thumb,(0,0)) #Stack another floor image onto the last thumbnail to make the current
							save_image(thumb_surface,thumb_addr)
							self.level.floors[x].thumb = None #Don't make another thumbnail unless another image is opened
					#Scale images to their original size
					for x in xrange(5):
						if self.level.floors[x].image is not None:
							self.level.floors[x].image.scale(self.level.floors[x].image.get_size())
					#Make a copy of the level
					save_level = copy.deepcopy(self.level)
					#Fill new object copy with image data
					for x in xrange(5):
						if self.level.floors[x].imgfile is not None:
							save_level.floors[x].image = open(self.level.floors[x].imgfile).read()
					#Save data files
					open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/level.dat", 'wb').write(zlib.compress(pickle.dumps(save_level, 2), 9)) #Store object data in string and compress it before writing to the file
					open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/information.dat", 'wb').write(pickle.dumps(self.level_information, 2))
					#Reopen image files
					for x in xrange(5):
						if self.level.floors[x].imgfile is not None:
							self.level.floors[x].image = open_image(self.level.floors[x].imgfile)
					self.section = MMS_NAV
					self.focus = True
					self.save_button.render(False)
					self.nav_button.render(True)
					for x in xrange(4,-1,-1):
						if self.level.floors[x].done_thumb:
							game.set_icon_folder_file(game.homedir + "/TimeSplitters Platinum Custom Maps/" + result, game.homedir + "/TimeSplitters Platinum Custom Maps/" + result + "/thumb" + str(x) + ".png") #Set file icon to the first thumbnail
							break
					self.reposition()
			elif self.section == MMS_OPTIONS: #Options
				self.options_menu.loop(mouse_pos,event,self)
			if (event[0] == MOUSEMOTION or event[0] == MOUSEUP):
				for button in self.buttons:
					if point_collide(mouse_pos,button):
						if event[0] == MOUSEMOTION:
							button.render(True)
						else:
							new_select = True
							self.last_section = self.section
							if button == self.exit_button:
								game.transfer_section(0)
							elif self.focus:
								if button == self.new_button:
									self.level = Level()
									self.level_information = LevelInformation()
									self.pos = [0,0]
									self.options_menu.change_level(self.level,self.level_information)
									self.story = 0
									self.change_floor()
								elif button == self.open_button:
									self.section = MMS_OPEN
								elif self.level:
									if button == self.save_button:
										self.section = MMS_SAVE
										self.focus = False
									elif button == self.image_button:
										self.section = MMS_NEW_IMG
									elif button == self.nav_button:
										self.section = MMS_NAV
									elif button == self.drag_button:
										self.item_drag = None
										self.item_selected = None
										self.section = MMS_DRAG
									elif button == self.wall_button:
										self.section = MMS_WALL
									elif button == self.items_button:
										if self.current_floor.image is not None:
											self.section = MMS_ITEMS
											self.item_drag = None
											self.item_selected = None
										else:
											new_select = False
									elif button == self.options_button:
										self.section = MMS_OPTIONS
									elif button == self.preview_button:
										self.section = MMS_PREVIEW
									elif button == self.stairs_button and self.current_floor.image is not None:
										self.section = MMS_FLOOR_TOOLS
								else:
									new_select = False #Trying to select something that shouldn't be.
								if new_select:
									if self.selected_button is not None:
										self.selected_button.render(False)
									self.selected_button = button
								self.enter = True
					elif event[0] == MOUSEMOTION and self.selected_button != button:
						button.render(False)
		if self.section not in [MMS_NO_IMG,MMS_NEW_IMG,MMS_OPEN]:
			game.blit(self.edit_area,(0,25))
		if self.section == MMS_OPEN:
			game.blit(self.open_browser,(390,60))
		elif self.section == MMS_OPTIONS:
			self.options_menu.render()
			print "Aha"
			game.blit(self.options_menu,(390,60))
			print "During this render of opt?"
		elif self.section == MMS_ITEMS and self.item_drag == None:
			game.blit(self.items,(self.items_button.get_offset()[0]-40,23))
		elif self.section == MMS_FLOOR_TOOLS:
			game.blit(self.floor_tools,(self.stairs_button.get_offset()[0]-40,23))
		elif self.section == MMS_SAVE:
			game.blit(self.save_browser,(390,60))
		if self.level:
			game.blit(self.story_indicator,(1180,25))
	def change_floor(self):
		if self.section != MMS_ITEMS or self.level.floors[self.story].image is not None:
			self.selected_connector_coordinates = None
			self.current_floor = self.level.floors[self.story]
			self.story_indicator.fill((0,0,0))
			Polygon(self.story_edges,menu_theme.not_selected_colour,self.story_indicator)
			Polygon([(x[0],x[1] + 20*(4-self.story)) for x in self.single_story_edges], menu_theme.selected_colour,self.story_indicator)
			for x in xrange(0,34,2):
				add_line(self.story_indicator,menu_theme.text_colour,self.story_lines[x],self.story_lines[x+1],1,True)
			if self.current_floor.image is None: #When an image has not been loaded for the floor use section 0 else 2 for navigation hand
				self.section = MMS_NO_IMG
				for button in self.buttons: #Render all the buttons clear as the newest level story doesn't need them
					button.render(False)
			else:
				self.reposition()
				if self.section == MMS_NO_IMG: #Change to navigation hand when the section before was for no level image
					self.nav_button.render(True)
					self.selected_button = self.nav_button
					self.section = MMS_NAV
	def arrow(self,pos,angle,colour):
		after = self.get_edit_position(pos)
		after[0] += maths.sin(angle)* 70
		after[1] += maths.cos(angle)* 70
		side1 = (after[0] + maths.sin(angle - maths.pi + 0.4) * 20,after[1] + maths.cos(angle - maths.pi + 0.5) * 10)
		add_line(self.edit_area, colour,after,side1,2,True)
		side2 = (after[0] + maths.sin(angle - maths.pi - 0.4) * 20, after[1] + maths.cos(angle - maths.pi - 0.5) * 10)
		add_line(self.edit_area, colour,after,side2,2,True)
		add_line(self.edit_area, colour,side1,side2,2,True)
	def edit_wall(self,w):
		self.new_wall = self.current_floor.walls[w][:]
		del self.current_floor.walls[w]
	def get_level_position(self,pos):
		return [(-self.pos[0] + pos[0])/self.current_zoom,(-self.pos[1] + pos[1])/self.current_zoom]
	def get_screeen_position(self,pos):
		return [pos[0] *self.current_zoom + self.pos[0],pos[1] *self.current_zoom + self.pos[1]]
	def get_edit_position(self,pos):
		pos = self.get_screeen_position(pos)
		return [pos[0],pos[1] - 25]
	def reposition(self):
		zoom = (self.zoom_scrollbar.get_pos() * 150 + 50)/100
		zoom_difference = zoom / self.current_zoom
		self.current_zoom = zoom
		self.pos[0] -= (1280*(zoom_difference-1))/2
		self.pos[1] -= (720*(zoom_difference-1))/2
		new_size = (self.current_floor.image.get_width()*zoom,self.current_floor.image.get_height()*zoom)
		if new_size[0] < 1280:
			self.pos[0] = (1280 - self.current_floor.image.get_width()*zoom)/2
		else:
			if self.pos[0] > 100:
				self.pos[0] = 100
			elif self.pos[0] < -new_size[0] + 1180:
				self.pos[0] = -new_size[0] + 1180
		if new_size[1] < 695:
			self.pos[1] = (695 - self.current_floor.image.get_width()*zoom)/2
		else:
			if self.pos[1] > 100:
				self.pos[1] = 100
			elif self.pos[1] <  -new_size[1] + 620:
				self.pos[1] =  -new_size[1] + 620
		self.current_floor.image.scale(new_size)
	def exit(self):
		pass
class AnacondaGame():
	#The Anaconda minigame section
	def init(self):
		self.music = "/music/anaconda.ogg"
		self.anaconda_game_over = [False] * 5
		self.pause_font = Font("NEUROPOL",70)
		self.pause_text = self.pause_font.render("Paused",(255,255,255))
		self.score_font = Font("NEUROPOL",30)
		self.title_text = self.score_font.render("Anaconda",(255,255,255))
		self.exit_text = self.score_font.render("Exit - Backspace",(255,255,255))
		self.play_area = Surface((1266,673))
	def transfer(self):
		self.login = False
		self.score = 0
		self.redxs = []
		for x in xrange(3):
			self.redxs.append((random.randrange(50,1211),random.randrange(50,608)))
		self.blue_count = 300
		self.snake = [] #Snake co-ordinates.
		self.snake_length = float(200)
		for x in range(0,int(self.snake_length),2):
			self.snake.append([30,450-x])
		self.snake_angle = 0
		self.game_over = False
		self.speed = 2
		self.game_over_first = True
		self.paused = False
		self.online_scores_menu_setup = False
		self.blue_score = 500
		self.angle_done = 2
	def loop(self):
		if not self.game_over:
			if game.key(KEY_P):
				if game.p_key == False:
					self.paused = not self.paused
					game.p_key = True
			else:
				game.p_key = False
		if not self.game_over and not self.paused:
			self.play_area.fill((0,0,0))
			new_c = False
			if game.key(KEY_LEFT):
				self.snake_angle -= (5 - 1.25**self.speed) * 60/game.get_fps()
				new_c = True
			if game.key(KEY_RIGHT):
				self.snake_angle += (5 - 1.25**self.speed) * 60/game.get_fps()
				new_c = True
			if not new_c:
				if self.speed < 5:
					self.speed += 0.08
			else:
				if self.speed > 2:
					self.speed -= 0.15
			snake_direction = [maths.sin(maths.radians(self.snake_angle)) * self.speed * 60/game.get_fps(),-maths.cos(maths.radians(self.snake_angle))* self.speed * 60/game.get_fps()]
			if new_c:
				self.snake.append([self.snake[-1][0] + snake_direction[0],self.snake[-1][1] + snake_direction[1]])
			else:
				self.snake[-1] = [self.snake[-1][0] + snake_direction[0],self.snake[-1][1] + snake_direction[1]]
			for x in xrange(len(self.snake)-1,-1,-1): #Removes co-ordinates which have the additional element to flag them as being used for the head to prevent the co-ordinates moving down the snake, unessicarily
				if len(self.snake[x]) == 3:
					del self.snake[x]
			remaining_length = self.snake_length
			tail_end = False
			for x in xrange(len(self.snake)-1,0,-1):
				if remaining_length != 0:
					dx = self.snake[x][0]-self.snake[x-1][0]
					dy = self.snake[x][1]-self.snake[x-1][1]
					line_len = abs((dx** 2 + dy ** 2)**0.5) #Use pythagoras to find the line length
					if remaining_length - line_len < 150 and not tail_end:
						tail_end = True
						cut_factor = (remaining_length - 150)/line_len
						self.snake.insert(x,[self.snake[x][0]-dx * cut_factor,self.snake[x][1]-dy * cut_factor,None])
					if line_len <= remaining_length: #Take line length from remaining length to gather the lines which will fit in the length
						remaining_length -= line_len
					else: #Trim the line to meet the length
						self.snake[x-1] = [self.snake[x-1][0] + (dx * (1 - remaining_length/line_len)),self.snake[x-1][1] + (dy * (1 - remaining_length/line_len))]
						remaining_length = 0
				else: #No remiang length
					del self.snake[x-1]
			remaining_length = self.snake_length + 1
			for x in xrange(len(self.snake)-1,0,-1): #Loop through the co-ordinates again to add extra co-ordinates for the head
				dx = self.snake[x][0]-self.snake[x-1][0]
				dy = self.snake[x][1]-self.snake[x-1][1]
				line_len = abs((dx** 2 + dy ** 2)**0.5) #Use pythagoras to find the line length
				if self.snake_length - remaining_length < 26 and line_len > 0: #For the head split the lines into more co-ordinates, 1 pixel long.
					newdx = dx/line_len
					newdy = dy/line_len
					limit = remaining_length
					for n in xrange(line_len-1):
						if self.snake_length - limit > 26: #See if the limit to the co-ordinates has been reached
							break
						else:
							limit -= 1
						self.snake.insert(x,[self.snake[x][0]-newdx,self.snake[x][1]-newdy,None]) #Add an additional element so it is known that these co-ordinates are needed for the head only
					remaining_length -= line_len
				else:
					break
			self.snakel = [None] * len(self.snake)
			self.snaker = [None] * len(self.snake)
			distance_traveled = 0
			for x in range(len(self.snake)): #Draw left and right sides of the snake. Do this by adding onto the snake co-ordinates at a certain angle
				xp =  self.snake[x][0] #x position
				yp =  self.snake[x][1] #y position
				if x != len(self.snake) - 1:
					dx = self.snake[x+1][0]-xp
					dy = self.snake[x+1][1]-yp
				else:
					dx = xp-self.snake[x-1][0]
					dy = yp-self.snake[x-1][1]
				angle = find_angle(dy,dx)
				if distance_traveled < 150: #For tail
					distance = distance_traveled/float(15)
				elif x + 25 > len(self.snake):
					distance = maths.sin(maths.acos(float(15 - (len(self.snake) - 1 - x))/float(15))) * 15 #For the head. Create a curve with trigonmetry. A little bit of trial and error needed to get the shape just right.
				else:
					distance = 10 #Snake width divided by two
				xamount = maths.sin(angle) * distance
				yamount = maths.cos(angle) * distance
				if dx <=0: #Odd hack required to flip the direction the line is taken from the center at certain points. 
					self.snaker[x] = [xp + xamount,yp - yamount]
					self.snakel[x] = [xp - xamount,yp + yamount]
				else:
					self.snakel[x] = [xp + xamount,yp - yamount]
					self.snaker[x] = [xp - xamount,yp + yamount]
				distance_traveled += abs(dx**2 + dy**2)**0.5
			if self.blue_count > 0:
				self.blue_pos = [0,0]
				self.blue_count -= 1 * 60/game.get_fps()
				self.blue_set = True
			#Draw the left side of the snake
			add_lines(self.play_area, (150,255,185), self.snakel + self.snaker[::-1],1)
			coordinates = len(self.snake)
			for n in xrange(1,coordinates):
				#Collision tests 
				if n + 15 > coordinates: #Only required for head
					newxs = 0
					for x in xrange(n-15): #Don't include parts that can't be intersected
						if intersect(self.snakel[n],self.snaker[n],self.snakel[x],self.snakel[x+1]) or intersect(self.snakel[n],self.snaker[n],self.snaker[x],self.snaker[x+1]):
							self.game_over = True
							game.play_sound("/sounds/anaconda/collision.ogg")
					if self.snakel[n][0] < 0 or self.snakel[n][0] > 1266 or self.snakel[n][1] < 0 or self.snakel[n][1] > 673 or self.snaker[n][0] < 0 or self.snaker[n][0] > 1266 or self.snaker[n][1] < 0 or self.snaker[n][1] > 673:
						self.game_over = True
						game.play_sound("/sounds/anaconda/collision.ogg")
					for x in xrange(len(self.redxs)):
						if xintersect(self.snakel[n],self.snaker[n],self.redxs[x]):
							game.play_sound("/sounds/anaconda/score.ogg")
							self.score += 85
							self.snake_length += 50
							del self.redxs[x]
							if self.blue_count > 0:
								self.blue_count -= 100
							else:
								self.blue_score += 100
							if len(self.redxs) * 3000 < self.score:
								self.score += 200
								for x in xrange(4):
									self.redxs.append((random.randrange(50,1211),random.randrange(50,608)))
							else:
								rm = int(self.score/6000) + 1
								self.redxs = self.redxs[:-rm]
								newxs = rm
							break
					if xintersect(self.snakel[n],self.snaker[n],self.blue_pos) and self.blue_count <= 0:
						game.play_sound("/sounds/anaconda/score.ogg")
						self.score += self.blue_score
						self.blue_score = 500
						self.snake_length += 100
						self.blue_count = 2000
						self.redxs = self.redxs[:-1]
						newxs = 1
						if len(self.redxs) < self.score/1000 and len(self.redxs) < 10:
							newxs += 1
					for x in xrange(newxs):	
						self.redxs.append((random.randrange(50,1211),random.randrange(50,608)))
				if n + 14 < coordinates and n != coordinates - 1 and self.blue_count <= 0:
					if xintersect(self.snakel[n],self.snakel[n+1],self.blue_pos):
						none_left_right = 1
					elif xintersect(self.snaker[n],self.snaker[n+1],self.blue_pos):
						none_left_right = 2
					else:
						none_left_right = 0
					if none_left_right != 0:
						#Reflect the blue X in the correct direction
						if none_left_right == 1: #Find angle with dy and dx
							angle = find_bearing(self.snakel[n+1][0] - self.snakel[n][0],self.snakel[n+1][1] - self.snakel[n][1])
						else:
							angle = find_bearing(self.snaker[n+1][0] - self.snaker[n][0],self.snaker[n+1][1] - self.snaker[n][1])
						#Get the normal angle of the line
						angle = angle + maths.pi/float(2)
						blue_angle = find_bearing(*self.blue_direction)
						if angle > 360:
							angle -= 360
						blue_angle = blue_angle + maths.pi
						if blue_angle > 360:
							blue_angle -= 360
						if blue_angle < angle: #Reflect the blue_x angle by the normal of the line angle. Isn't mathss fun. :(
							new_angle = angle + (angle - blue_angle)
						else:
							new_angle = angle - (blue_angle - angle)
						#Need to convert angle into one compatible with the direction first. 1.41421356 is the speed
						self.blue_direction[0] = maths.sin(new_angle) *  1.41421356
						self.blue_direction[1] = -maths.cos(new_angle) *  1.41421356
			if self.blue_count <= 0 and self.blue_set:
				self.blue_set = False
				rint = random.choice([-1,1])
				if random.randrange(0,1) == 0:
					self.blue_pos = [-20 if rint == 1 else 1280,random.randrange(0,657)]
					self.blue_direction = [rint,random.choice([-1,1])]
				else:
					blue_pos = [random.randrange(0,1260),-20 if rint == 1 else 677]
					self.blue_direction = [random.choice([-1,1]),rint]
			if self.blue_count <= 0:
				if (self.blue_pos[0] > 1247 and self.blue_direction[0] > 0) or (self.blue_pos[0] < 0 and self.blue_direction[0] < 0):
					self.blue_direction[0] *= -1
				if (self.blue_pos[1] > 657 and self.blue_direction[1] > 0) or (self.blue_pos[1] < 0 and self.blue_direction[1] < 0):
					self.blue_direction[1] *= -1
				self.blue_pos[0] += self.blue_direction[0] * 60/game.get_fps()
				self.blue_pos[1] += self.blue_direction[1] * 60/game.get_fps()
				self.placex((50,50,200), self.blue_pos)
			for x in self.redxs:
				self.placex((200,50,50), x)
		score_str = str(self.score)
		score_str = "0" * (5 - len(score_str)) + score_str
		score_text = self.score_font.render(score_str,(150,255,185))
		game.blit(score_text,(5,5))
		game.blit(self.title_text,(546,5))
		game.blit(self.exit_text,(1280 - self.exit_text.get_width()-5,5))
		add_line(game, (255,255,255), (5,40), (1275,40), 3)
		add_line(game, (255,255,255), (5,717), (1275,717), 3)
		add_line(game, (255,255,255), (5,40), (5,717), 3)
		add_line(game, (255,255,255), (1275,40), (1275,717), 3)
		if self.paused:
			self.play_area.blit(self.pause_text,(640-self.pause_text.get_width()/2,360-self.pause_text.get_height()/2))
		game.blit(self.play_area,(8,43))
		event = ""
		if self.game_over == True:
			if self.game_over_first:
				self.game_over_first = False
				#First time when the game ends.
				#Get local scores
				if os.path.exists(game.homedir + "/.timesplitters_platinum/scores.sav"):
					score_file = open(game.homedir + "/.timesplitters_platinum/scores.sav","rb")
					self.scores = pickle.load(score_file)
					score_file.close()
				else:
					self.scores = []
				username = getpass.getuser()
				self.scores_no = len(self.scores)
				if self.scores_no == 0:
					self.score_pos = 0
				else:
					self.score_pos = self.scores_no
					for x in xrange(self.scores_no):
						if self.score >= self.scores[x][1]:
							self.score_pos = x
							break
				#Create menu
				self.anaconda_game_over[0] = Menu("Game Over")
				self.anaconda_game_over[0].add_text("You Scored " + str(self.score),300,1,40)
				if self.scores_no == 0:
					self.new_score = self.anaconda_game_over[0].add_new_score(username,self.score) #Add a MenuNewScore object to the menu and return a reference for use lower
				else:
					if self.scores_no == 10:
						self.scores_no -= 1
					for x in xrange(self.scores_no + 1):
						if self.score_pos == x:
							self.new_score = self.anaconda_game_over[0].add_new_score(username,self.score)
						if x != self.scores_no:
							self.anaconda_game_over[0].add_score(self.scores[x][0],self.scores[x][1])
				self.anaconda_game_over[0].add_button("Submit Online","LOGIN",True)
				if login_menu.logged_in:
					self.logout_button = self.anaconda_game_over[0].add_button("Logout " + login_menu.username ,LOGOUT,True)
				else:
					self.logout_button = None
				self.anaconda_game_over[0].add_button("Replay",1,True)
				self.anaconda_game_over[0].add_button("Exit",0,True)
				self.anaconda_game_over[0].create()
				self.anaconda_game_over[1] = Menu("Submitting Your Score")
				self.anaconda_game_over[1].add_text("Your score is being submitted to the database and you will be presented with the online scores shortly.",700,1)
				self.anaconda_game_over[1].create()
				self.anaconda_menu = MenuSet(self.anaconda_game_over,game)
				self.submitted = False
			if self.online_scores_menu_setup:
				if not self.score_request.isAlive():
					self.online_scores_menu_setup = False
					self.anaconda_menu.menu_active = 2
					self.anaconda_menu.menu_change = True
					wierd_output = False
					if self.score_request.response_number == "200": #200 OK
						if self.score_request.content[0] == "Y": #Authentication Successful
							if self.logout_button is not None:
								self.anaconda_game_over[0].remove(self.logout_button)
							scores = self.score_request.content[1:].split("\n")
							for x in xrange(len(scores)):
								scores[x] = scores[x].split(";")
								for y in xrange(len(scores[x])):
									scores[x][y] = scores[x][y].split(",")
							if len(scores) > 5:
								self.submitted = True
								self.anaconda_game_over[2] = Menu("Last 24 Hour Top Scores")
								self.anaconda_game_over[2].add_text(scores[3][0][0],700,1)
								self.online_scores(self.anaconda_game_over[2],scores[0])
								self.anaconda_game_over[2].add_button("Top scores for the last week",3)
								self.anaconda_game_over[2].add_button("All-time bests",4)
								self.anaconda_game_over[2].add_button("Back",0)
								self.anaconda_game_over[2].add_button("Replay",1,True)
								self.anaconda_game_over[2].add_button("Exit",0,True)
								self.anaconda_game_over[2].create()
								self.anaconda_game_over[3] = Menu("Top Scores for the Last Week")
								self.anaconda_game_over[3].add_text(scores[4][0][0],700,1)
								self.online_scores(self.anaconda_game_over[3],scores[1])
								self.anaconda_game_over[3].add_button("Last 24 hour top scores",2)
								self.anaconda_game_over[3].add_button("All-time bests",4)
								self.anaconda_game_over[3].add_button("Back",0)
								self.anaconda_game_over[3].add_button("Replay",1,True)
								self.anaconda_game_over[3].add_button("Exit",0,True)
								self.anaconda_game_over[3].create()
								self.anaconda_game_over[4] = Menu("All-time Bests")
								self.anaconda_game_over[4].add_text(scores[5][0][0],700,1)
								self.online_scores(self.anaconda_game_over[4],scores[2])
								self.anaconda_game_over[4].add_button("Last 24 hour top scores",2)
								self.anaconda_game_over[4].add_button("Top scores for the last week",3)
								self.anaconda_game_over[4].add_button("Back",0)
								self.anaconda_game_over[4].add_button("Replay",1,True)
								self.anaconda_game_over[4].add_button("Exit",0,True)
								self.anaconda_game_over[4].create()
							else:
								wierd_output = True
						elif self.score_request.content[0] == "N":
							login_menu.logged_in = False
							self.anaconda_game_over[2] = Menu("Error")
							self.anaconda_game_over[2].add_text("There was an authentication error. Please try to login again.",700,1)
							self.anaconda_game_over[2].add_button("Back",0)
							self.anaconda_game_over[2].add_button("Replay",1,True)
							self.anaconda_game_over[2].add_button("Exit",0,True)
							self.anaconda_game_over[2].create()
						else:
							wierd_output = True
					else:
						self.anaconda_game_over[2] = Menu("Error")
						self.anaconda_game_over[2].add_text("The server gave a " + str(self.score_request.response_number) + " http status code.",700,1)
						self.anaconda_game_over[2].add_button("Back",0)
						self.anaconda_game_over[2].add_button("Replay",1,True)
						self.anaconda_game_over[2].add_button("Exit",0,True)
						self.anaconda_game_over[2].create()
					if wierd_output:
						print "Send this message, including the following to Matthew Mitchell (god0fgod):\n"
						print self.score_request.content
						self.anaconda_game_over[2] = Menu("Error")
						self.anaconda_game_over[2].add_text("The server didn't give the correct output. Check the terminal output for more information.",700,1)
						self.anaconda_game_over[2].add_button("Back",0)
						self.anaconda_game_over[2].add_button("Replay",1,True)
						self.anaconda_game_over[2].add_button("Exit",0,True)
						self.anaconda_game_over[2].create()
			if self.login:
				if not login_menu.logged_in:
					event =  login_menu.loop_login()
				else:
					event = "SUCCESS"
				if event == "CANCEL":
					self.login = False
				elif event == "SUCCESS":
					self.login = False
					if self.submitted == False:
						self.online_scores_menu_setup = True
						self.anaconda_menu.menu_active = 1
						self.anaconda_menu.menu_change = True
						self.score_request = HTTPRequestThread("http://www.crytekuk.info/tsp_requests/anaconda_scores.php",{'username': login_menu.username, 'password': login_menu.password,'score':str(self.score)},10)
					else:
						self.anaconda_menu.menu_active = 2
						self.anaconda_menu.menu_change = True
			else:
				event = self.anaconda_menu.loop(game.events)
				if event == "LOGIN":
					self.login = True
					login_menu.transfer = True
				elif event == LOGOUT:
					login_menu.logged_in = False
					self.anaconda_game_over[0].remove(self.logout_button)
				elif event != -1 and event != "TXT" and event != "LOGIN":
					self.anaconda_add_score()
					game.transfer_section(event)
		if game.fade_screen() == False and not self.game_over:
			if game.key(KEY_BACKSPACE) and event != "TXT":
				game.transfer_section(0)
	def online_scores(self,menu,scores):
		if scores[0][0] == '':
			menu.add_text("No scores available.",700,1)
		else:
			for score in scores:
				menu.add_score(score[0],score[1])
	def placex(self,c,x):
		add_line(self.play_area, c, x, (x[0]+20,x[1]+20))
		add_line(self.play_area, c, (x[0],x[1]+20), (x[0]+20,x[1]))
	def anaconda_add_score(self):
		if self.score_pos < 10:
			self.scores.insert(self.score_pos,[self.new_score.text,self.score]) 
		self.scores = self.scores[:10]
		score_file = open(game.homedir + "/.timesplitters_platinum/scores.sav","wb")
		pickle.dump(self.scores,score_file,2)
		score_file.close()
	def exit(self):
		if self.game_over == True:
			self.anaconda_add_score()
class MonkeyCurling():
	def init(self):
		self.music = "/music/game/Like A Monkey.ogg"
		cmain.add_snow_texture(c_uint(load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/snowflake.png")[0]))
		self.spin_centre = Surface((4,24))
		self.spin_centre.fill((0,0,0))
		self.spin_score_font = Font("NEUROPOL",60)
		self.add_spin_text = self.spin_score_font.render("Add Spin",(0,0,0))
		self.score_text = self.spin_score_font.render("Score",(0,0,0))
		self.metres_text = self.spin_score_font.render("Metres",(0,0,0))
		self.current_score_font = Font("NEUROPOL",40)
		self.current_score_text = self.current_score_font.render("Current Total Score: ",(0,0,0))
		#Snow textures
		#Make scene
		#Sky
		Rectangle(((-1000,700,-1000),(1000,700,-1000),(1000,0,-1000),(-1000,0,-1000)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/sky0.jpg")[0],1,1)
		Rectangle(((1000,700,1000),(-1000,700,1000),(-1000,0,1000),(1000,0,1000)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/sky2.jpg")[0],1,1)
		Rectangle(((-1000,700,1000),(-1000,700,-1000),(-1000,0,-1000),(-1000,0,1000)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/sky3.jpg")[0],1,1)
		#Ground
		Rectangle(((-1000,0,-1000),(1000,0,-1000),(1000,0,1000),(-1000,0,1000)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/snow.png")[0],10,10)
		Rectangle(((-10,0,0),(10,0,0),(10,0,150),(-10,0,150)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/ice.jpg")[0],3,15,(0.95,0.95,1,1)) #Surface for monkey to slide
		Rectangle(((9,0,149),(-9,0,149),(-9,0,129),(9,0,129)),load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/target.png")[0],1,1) #Target to aim for
		concrete = load_image_texture(os.path.dirname(sys.argv[0]) + "/images/curling_textures/concrete.jpg")[0]
		#Inner walls
		Rectangle(((-10, 1, 0), (10, 1, 0), (10, 0, 0), (-10, 0, 0)),concrete,10,1)
		Rectangle(((10, 1, 0), (10, 1, 150), (10, 0, 150), (10, 0, 0)),concrete,100,1)
		Rectangle(((10, 1, 150), (-10, 1, 150), (-10, 0, 150), (10, 0, 150)),concrete,100,1)
		Rectangle(((-10, 1, 150), (-10, 1, 0), (-10, 0, 0), (-10, 0, 150)),concrete,10,1)
		#Outer walls
		Rectangle(((10.1,0,-0.1),(10.1,0,150.1),(10.1,1,150.1),(10.1,1,-0.1)),concrete,100,1)
		#Top of walls
		Rectangle(((10.1,1,-0.1),(10.1,1,150.1),(10,1,150.1),(10,1,-0.1)),concrete,100,0.1)
		Rectangle(((10.1,1,150.1),(-10.1,1,150.1),(-10.1,1,150),(10.1,1,150)),concrete,100,0.1)
		Rectangle(((-10.1,1,150.1),(-10.1,1,-0.1),(-10,1,-0.1),(-10,1,150.1)),concrete,10,0.1)
	def new_round(self):
		self.direction_right = True
		self.power_up = True
		self.spin = 0
		self.monkeys.append([0,5.5,20,0]) #Speed is 20 metres per second per second. Acceleration is -1.8 metres per second per second.
		#Start off at the other end of the ice looking down the ice
		self.eyex = 0
		self.eyey = 2
		self.eyez = 5.5
		self.lookx = 0
		self.looky = 1
		self.lookz = 139
		self.xlook_bit_flags = 0
		self.zlook_bit_flags = 0
		self.section = CURLING_DIRECTION
	def transfer(self):
		#Make OpenGL use 3D
		game.modify_background_colour(0.55,0.85,0.98,1)
		self.round = 0
		self.monkeys = []
		self.new_round()
	def loop(self):
		game.engage_3d(45,0.1,2000) #Imagine each unit as one metre.
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(self.eyex, self.eyey, self.eyez, self.lookx, self.looky, self.lookz, 0, 1,0) 
		draw_3d_items()
		if self.section in [CURLING_DIRECTION,CURLING_POWER]:
			if self.section == CURLING_DIRECTION:
				#Change direction
				if self.direction_right:
					self.monkeys[self.round][MONKEY_DIRECTION] -= 0.8/game.get_fps()
				else:
					self.monkeys[self.round][MONKEY_DIRECTION] += 0.8/game.get_fps()
				if abs(self.monkeys[self.round][MONKEY_DIRECTION]) > 0.15:
					if self.direction_right:
						self.direction_right = False
						self.monkeys[self.round][MONKEY_DIRECTION] = -0.15
					else:
						self.direction_right = True
						self.monkeys[self.round][MONKEY_DIRECTION] = 0.15
				if game.key(KEY_ENTER):
					if not self.enter_key:
						self.enter_key = True
						self.section = CURLING_POWER
				else:
					self.enter_key = False
			elif self.section == CURLING_POWER:
				if self.eyey < 20:
					self.eyey += 10./game.get_fps()
				if self.power_up:
					self.monkeys[self.round][MONKEY_SPEED] += 7./game.get_fps()
				else:
					self.monkeys[self.round][MONKEY_SPEED] -= 7./game.get_fps()
				if abs(self.monkeys[self.round][MONKEY_SPEED] - 19.5) > 2.5:
					if self.power_up:
						self.power_up= False
						self.monkeys[self.round][MONKEY_SPEED] = 22
					else:
						self.power_up = True
						self.monkeys[self.round][MONKEY_SPEED]  = 17
				if game.key(KEY_ENTER):
					if not self.enter_key:
						self.enter_key = True
						self.section = CURLING_SPIN
				else:
					self.enter_key = False
			#Show direction and power representation
			length = (self.monkeys[self.round][MONKEY_SPEED]**2)/3
			end_point = (maths.sin(self.monkeys[self.round][MONKEY_DIRECTION])*length,5 + maths.cos(self.monkeys[self.round][MONKEY_DIRECTION])*length)
			draw_rectangle(((-1, 0, 5.5),(end_point[0]-1,0,end_point[1]),(1, 0, 5.5),(end_point[0]+1,0,end_point[1])),(0.8,0.2,0.1,0.3))
		elif self.section == CURLING_SPIN:
			if self.eyey > 6:
				self.eyex += 6./game.get_fps()
				self.eyey -= 7./game.get_fps()
				self.eyez += 5./game.get_fps()
				self.lookz -= 30./game.get_fps()
			else:
				self.section = CURLING_MOVE
				self.focused = False
			if game.key(KEY_LEFT):
				self.spin += 0.02/game.get_fps()
				if self.spin > 0.02:
					self.spin = 0.02
			if game.key(KEY_RIGHT):
				self.spin -= 0.02/game.get_fps()
				if self.spin < -0.02:
					self.spin = -0.02
		elif self.section == CURLING_MOVE:
			if any([self.monkeys[x][MONKEY_SPEED] > 0 for x in xrange(self.round + 1)]):
				if not self.focused:
					if self.eyey > 4:
						self.eyey -= float(3*self.eyey - 11)/game.get_fps()
					if self.eyex < 18:
						self.eyex += float(-0.75*self.eyex +15)/game.get_fps()
					if self.lookz > self.monkeys[self.round][MONKEY_Z]:
						self.lookz -= 30./game.get_fps()
					else:
						self.focused = True
						self.eyey = 1.2
						self.eyex = 9
						self.eyez = 148
				else:
					self.lookz = self.monkeys[self.round][MONKEY_Z]
				self.lookx = self.monkeys[self.round][MONKEY_X]
				for monkey in self.monkeys:
					if monkey[MONKEY_SPEED] > 0:
						oldx = monkey[MONKEY_X]
						oldz = monkey[MONKEY_Z]
						monkey[MONKEY_X] += maths.sin(monkey[MONKEY_DIRECTION])*monkey[MONKEY_SPEED]/game.get_fps()
						monkey[MONKEY_Z] += maths.cos(monkey[MONKEY_DIRECTION])*monkey[MONKEY_SPEED]/game.get_fps()
						if abs(monkey[MONKEY_X]) > 9.6:
							monkey[MONKEY_SPEED] = monkey[MONKEY_SPEED]/3.0
							monkey[MONKEY_DIRECTION] = -monkey[MONKEY_DIRECTION]
							if monkey[MONKEY_X] > 0:
								monkey[MONKEY_X] = 9.6
							else:
								monkey[MONKEY_X] = -9.6
						else:
							monkey[MONKEY_SPEED] -= 1.5/game.get_fps()
							monkey[MONKEY_DIRECTION] += self.spin/game.get_fps()
						if monkey[MONKEY_Z] > 149.2:
							monkey[MONKEY_Z] = 149.2
							monkey[MONKEY_SPEED] = monkey[MONKEY_SPEED]/4.0
							monkey[MONKEY_DIRECTION] += 3.1415926536
						for monkey2 in self.monkeys:
							if monkey != monkey2:
								if ((monkey[MONKEY_X] - monkey2[MONKEY_X])**2 + (monkey[MONKEY_Z] - monkey2[MONKEY_Z])**2)**0.5 < 1.6:
									monkey[MONKEY_X] = oldx
									monkey[MONKEY_Z] = oldz
									monkey[MONKEY_SPEED] /= 3
									monkey2[MONKEY_SPEED] = monkey[MONKEY_SPEED] * 1.8
									monkey2[MONKEY_DIRECTION] = find_bearing(monkey[MONKEY_X] - monkey2[MONKEY_X],monkey[MONKEY_Z] - monkey2[MONKEY_Z])
			else:
				done = 0
				if self.eyey < 36.2:
					self.eyey += 105./game.get_fps()
				else:
					done += 1
				if self.eyex > 0:
					self.eyex -= 27./game.get_fps()
				else:
					self.eyex = 0
					done += 1
				if self.eyez > 138:
					self.eyez -= 90./game.get_fps()
				else:
					done += 1
				if self.lookx > 0 and not self.xlook_bit_flags & 2:
					self.xlook_bit_flags = self.xlook_bit_flags | 1
					self.lookx -= 40./game.get_fps()
				elif self.lookx < 0 and not self.xlook_bit_flags & 1:
					self.xlook_bit_flags = self.xlook_bit_flags | 2
					self.lookx += 40./game.get_fps()
				else:
					self.lookx = 0
					done += 1
				if self.lookz > 139 and not self.zlook_bit_flags & 2:
					self.zlook_bit_flags = self.zlook_bit_flags | 1
					self.lookz -= 40./game.get_fps()
				elif self.lookz < 139 and not self.zlook_bit_flags & 1:
					self.xlook_bit_flags = self.zlook_bit_flags | 2
					self.lookz += 40./game.get_fps()
				else:
					self.lookz = 139
					done += 1
				if done == 5:
					self.section = CURLING_SCORE
					self.score_start = time.time()
		#Draw monkeys
		for monkey in self.monkeys:
			draw_rectangle(((monkey[MONKEY_X]-0.4, 0, monkey[MONKEY_Z]-0.8),(monkey[MONKEY_X] -0.4,0,monkey[MONKEY_Z] + 0.8),(monkey[MONKEY_X] + 0.4,0,monkey[MONKEY_Z] - 0.8),(monkey[MONKEY_X] + 0.4, 0, monkey[MONKEY_Z] + 0.8)),(0.8,0.2,0.1,0.3))
		#Draw snow
		cmain.draw_snow(c_uint(game.get_fps()))
		#Get current scores for each monkey
		scores = []
		for monkey in self.monkeys:
			metres = ((monkey[MONKEY_X]**2 + (monkey[MONKEY_Z] - 139)**2)**0.5)/2
			score = int((5 - metres)*200) #Convert metres to the score. < 5 metres = 0, 0 metres = 1000
			if score < 0:
				score = 0
			scores.append(score)
		game.engage_2d() #Go back to 2D to do all 2D things
		if self.section == CURLING_SPIN:
			w = abs(self.spin*10000)
			if w > 1:
				surface = Surface((w,20))
				surface.fill((204,51,25.5,200))
				if self.spin < 0:
					game.blit(surface,(640,680))
				else:
					game.blit(surface,(640 - w,680))
			game.blit(self.spin_centre,(638,680))
			game.blit(self.add_spin_text,(492,610))
		elif self.section == CURLING_SCORE:
			if self.score_start + 4 > time.time():
				game.blit(self.metres_text,(30,300))
				game.blit(self.score_text,(900,300))
				game.blit(self.spin_score_font.render(str(round(metres,2)),(0,0,0)),(30,500)) #Get latest monkey metres from the varible made in the fot loop just above
				game.blit(self.spin_score_font.render(str(scores[self.round]),(0,0,0)),(900,500))
			else:
				self.round += 1
				self.new_round()
		if self.section != CURLING_GAME_OVER:
			game.blit(self.current_score_text,(20,20))
			game.blit(self.current_score_font.render(str(sum(scores)),(0,0,0)),(450,20))
		if game.fade_screen() == False and self.section != CURLING_GAME_OVER:
			if game.key(KEY_BACKSPACE):
				#Reset OpenGL to normal viewing mode
				game.modify_background_colour(0,0,0,1)
				game.transfer_section(0)
class MainMenu():
	def init(self):
		login_menu.init()
		self.music = "/music/menu.ogg"
		self.menu = [None] * 18
		self.images = []
		for x in range(2):
			image = open_image(os.path.dirname(sys.argv[0]) + "/images/menu_images/" + str(x) + ".png")
			self.images.append(image)
		self.transfer(True)
		self.enter = True
		map_selection_menu = False
		menu = [Menu("Select game mode")]
		menu[0].add_button("Deathmatch",DEATHMATCH,True)
		menu[0].add_button("Team Deathmatch",TEAMDEATHMATCH,True)
		menu[0].add_button("Elimination",ELIMINATION,True)
		menu[0].add_button("Team Elimination",TEAMELIMINATION,True)
		menu[0].create()
		self.mode_selection_menu = MenuSet(menu,game)
		self.arcade_setup_map = False
		self.arcade_setup_mode = False
		self.arcade_setup_options = False
		self.arcade_setup_bots = False
		self.arcade_setup_weapons = False
		self.arcade_setup_player = False
		self.map_selection_menu = False
	def create_gradient(self):
		self.background_gradient.fill((255,255,255,255))
		if game.options[OPTION_THEME] == 0: #Blue
			for x in xrange(256):
				add_line(self.background_gradient, (x/5,x/3,x), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 1: #Red
			for x in xrange(256):
				add_line(self.background_gradient, (x,x/5,x/4), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 2: #Green
			for x in xrange(256):
				add_line(self.background_gradient, (x/5,x,x/4), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 3: #Yellow
			for x in xrange(256):
				add_line(self.background_gradient, (x,x,x/5), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 4: #Orange
			for x in xrange(256):
				add_line(self.background_gradient, (x,x/2,x/5), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 5: #Pink
			for x in xrange(256):
				add_line(self.background_gradient, (x,x/1.5,x/1.5), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 6: #White
			for x in xrange(256):
				add_line(self.background_gradient, (x,x,x), (0,x), (1280,x), 1)
		elif game.options[OPTION_THEME] == 7: #Black
			for x in xrange(256):
				add_line(self.background_gradient, (x/10,x/10,x/9), (0,x), (1280,x), 1)
	def make_map_selection_menu(self,order,desc):
		maps = []
		for map in os.listdir(game.homedir + "/TimeSplitters Platinum Custom Maps"):
			if os.path.isdir(game.homedir + "/TimeSplitters Platinum Custom Maps/" + map): #Only allow folders which will be the maps
				level_information = pickle.loads(open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + map + "/information.dat", 'rb').read())
				maps.append((map,level_information.established,level_information.plays,level_information.last_played,level_information.last_save,level_information.description))
		if not maps:
			menu = [Menu("Custom Maps")]
			menu[0].add_text("No Maps Found",500,1,40)
			menu[0].add_button("Return",MAPRETURN,True)
			menu[0].create()
			menu_set = MenuSet(menu,game)
			menu_set.return_key = True
			return menu_set
		if order == ORDER_MAPS_NAME:
			maps.sort(key=lambda x:x[0],reverse=desc)
		elif order == ORDER_MAPS_ESTABLISH:
			maps.sort(key=lambda x:x[1],reverse=desc)
		elif order == ORDER_MAPS_PLAYS:
			maps.sort(key=lambda x:x[2],reverse=desc)
		elif order == ORDER_MAPS_LAST_PLAY:
			maps.sort(key=lambda x:x[3],reverse=desc)
		elif order == ORDER_MAPS_LAST_EDIT:
			maps.sort(key=lambda x:x[4],reverse=desc)
		menu = [Menu("Custom Maps")]
		scroll_area = MenuScrollArea()
		for map in maps:
			thumbs = []
			for file in os.listdir(game.homedir + "/TimeSplitters Platinum Custom Maps/" + map[0]):
				if file[:5] == "thumb":
					thumbs.append(game.homedir + "/TimeSplitters Platinum Custom Maps/" + map[0] + "/" + file)
			scroll_area.add_map_preview_button(map[0],map[1],map[4],map[2],map[3],map[5],thumbs)
		menu[0].add_scrollable_area(scroll_area,600)
		menu[0].create()
		menu_set = MenuSet(menu,game)
		menu_set.return_key = True
		self.backspace = False
		return menu_set
	def transfer(self,first = False):
		game.show_cursor(False)
		game.disable_mouse()
		if game.get_fade() == 255:
			game.play_sound("/sounds/menu3/unfade.ogg")
		self.current_img = random.choice(self.images)
		if not first:
			active = self.main_menu.menu_active
		self.menu[0] = Menu("TimeSplitters Platinum Pre-Alpha",-2)
		self.menu[0].add_button("Arcade",9)
		self.menu[0].add_button("Mapmaker",[2],True)
		self.menu[0].add_button("Mini Games",1)
		self.menu[0].add_button("Options",OPTTOG,True)
		self.menu[0].add_button("Controls",CONTROLS,True)
		self.menu[0].add_button("Credits",4)
		self.menu[0].add_button("The Unofficial Crytek UK Blog",BLOG,True)
		if login_menu.logged_in:
			self.logout_button = self.menu[0].add_button("Logout",LOGOUT,True)
		self.menu[0].create()
		self.menu[1] = Menu("Mini Games")
		self.menu[1].add_button("Anaconda",2)
		self.menu[1].add_button("Monkey Curling",16)
		self.menu[1].create()
		self.menu[2] = Menu("Anaconda")
		self.menu[2].add_button("Start",[1],True)
		self.menu[2].add_button("Instructions",3)
		self.menu[2].create()
		self.menu[3] = Menu("Anaconda Instructions")
		self.menu[3].add_text("The object of the game is to score as many points as possible by collecting blue and red Xs with a snake before hiting a wall or yourself.\n\nBlue Xs will move and are harder to collect. Red Xs will change position as you collect them. Collecting Xs increases the size of the snake. Turn the snake with the arrow keys. Turning will slow the snake down. Press P to pause at any time during the game. \n\nBlue Xs are worth 500 points. Red Xs are worth 85 points and will add 100 points to the next blue X if one is on the screen or it will make the next blue X appear faster. Clearing them to a limit gives a 200 point bonus. \n",700,0)
		self.menu[3].add_text("You are able to submit scores afterwards online. Good luck!",700,1)
		self.menu[3].create()
		self.menu[4] = Menu("Credits")
		self.menu[4].add_text("Matthew Mitchell",500,1,40)
		self.menu[4].add_text("Project leader\nProgrammer\nMenu Music",400,0,30)
		self.menu[4].add_button("Website",BLOG,True)
		self.menu[4].add_button("Next",5)
		self.menu[4].create()
		self.menu[5] = Menu("Credits")
		self.menu[5].add_text("Andrew Soto",500,1,40)
		self.menu[5].add_text("Anaconda Music\nSpaceport Surge Mix\nTS2 Streets + 1",400,0,30)
		self.menu[5].add_button("NewGrounds Profile",ANDREW,True)
		self.menu[5].add_button("ForFinancialFreedom",ANDREWFFF,True)
		self.menu[5].add_button("Next",6)
		self.menu[5].create()
		self.menu[6] = Menu("Credits")
		self.menu[6].add_text("Dominic Russel",500,1,40)
		self.menu[6].add_text("Graphics\nSound extraction\nTesting",400,0,30)
		self.menu[6].add_button("Next",7)
		self.menu[6].create()
		self.menu[7] = Menu("Credits")
		self.menu[7].add_text("Caleb Taylor",500,1,40)
		self.menu[7].add_text("Programmer",400,0,30)
		self.menu[7].add_button("Next",8)
		self.menu[7].create()
		self.menu[8] = Menu("Credits")
		self.menu[8].add_text("Alex Flame",500,1,40)
		self.menu[8].add_text("Spaceport remix",400,0,30)
		self.menu[8].add_button("Done",0)
		self.menu[8].create()
		self.menu[9] = Menu("Arcade Match")
		self.menu[9].add_button("Builtin maps",10)
		self.menu[9].add_button("Custom maps",11)
		self.menu[9].create()
		self.menu[11] = Menu("Custom Maps")
		self.menu[11].add_button("List by name",NAMEMAPS,True)
		self.menu[11].add_button("List by date of establishment",12)
		self.menu[11].add_button("List by date of last edit",15)
		self.menu[11].add_button("List by number of plays",13)
		self.menu[11].add_button("List by date last played",14)
		self.menu[11].create()
		self.menu[12] = Menu("Custom Maps")
		self.menu[12].add_button("Newest first",DATENEWMAPS,True)
		self.menu[12].add_button("Oldest first",DATEOLDMAPS,True)
		self.menu[12].create()
		self.menu[13] = Menu("Custom Maps")
		self.menu[13].add_button("Most played first",PLAYSMOSTMAPS,True)
		self.menu[13].add_button("Least played first",PLAYSLEASTMAPS,True)
		self.menu[13].create()
		self.menu[14] = Menu("Custom Maps")
		self.menu[14].add_button("Most recently played first",LASTPLAYRECENTMAPS,True)
		self.menu[14].add_button("Longest time since last play first",LASTPLAYLONGESTMAPS,True)
		self.menu[14].create()
		self.menu[15] = Menu("Custom Maps")
		self.menu[15].add_button("Newest first",EDITNEWMAPS,True)
		self.menu[15].add_button("Oldest first",EDITOLDMAPS,True)
		self.menu[15].create()
		self.menu[16] = Menu("Monkey Curling")
		self.menu[16].add_button("Start",[4],True)
		self.menu[16].add_button("Instructions",17)
		self.menu[16].create()
		self.menu[17] = Menu("Monkey Curling Instructions")
		self.menu[17].add_text("The object of the game is to curl a monkey as close to the centre of a target as possible.\n\n You can select the power and direction with the enter/return key. Moving bars indicate the current selection. You can apply spin to the monkey using the arrow keys directly after selecting the power and direction. Tapping enter will brush the ice in front of the monkey, making it slow down slightly less.\n\n The monkey will reach a series of circles and where the monkey stops inside these circles will determine the score. The outer most circle represents 0 points and the points continuously increase to 1000 toward the center. Each game has 5 turns and your cumulative score will be put onto the scoreboard at the end of the game but beware because hitting monkeys will cause them to move and potentially lose your earlier scores. \n\nYou may submit your scores online to be compared around the world.\n",700,0)
		self.menu[17].add_text("Good luck!",700,1)
		self.menu[17].create()
		self.main_menu = MenuSet(self.menu,game)
		self.options_menu_active = self.main_menu
		if not first:
			self.main_menu.menu_active = active
			self.main_menu.return_key = True #To prevent entering twice as this variable is reset to false.
	def loop(self):
		if self.enter:
			self.background_gradient = Surface((1280,255))
			self.create_gradient()
			self.enter = False
		game.blit(self.background_gradient,(0,464))
		game.blit(self.current_img,(20,20))
		if self.arcade_setup_bots:
			if game.key(KEY_BACKSPACE) and not self.backspace:
				self.arcade_setup_bots = False
				self.backspace = True
			else:
				self.backup = False
			event = self.arcade_setup_weapons.loop(game.events)
		elif self.arcade_setup_options:
			if game.key(KEY_BACKSPACE) and not self.backspace:
				self.arcade_setup_options = False
				self.backspace = True
			else:
				self.backup = False
			event = self.arcade_setup_bot_menu.loop(game.events)
			if event == DONEGAMEOPTS:
				self.arcade_setup_bots = self.arcade_setup_bot_menu.menu[0].get_options()
				menu = [Menu("Game Weapons")]
				for x in xrange(5):
					menu[0].add_multiple_option("Weapon " + str(x + 1),weapon_list,self.level.weapons[x])
				menu[0].add_button("Done",DONEGAMEOPTS,True)
				menu[0].create()
				self.arcade_setup_weapons = MenuSet(menu,game)
		elif self.arcade_setup_mode:
			if game.key(KEY_BACKSPACE) and not self.backspace:
				self.arcade_setup_mode = False
				self.backspace = True
			else:
				self.backup = False
			event = self.game_options_menu.loop(game.events)
			if event == DONEGAMEOPTS:
				self.arcade_setup_options = self.game_options_menu.menu[0].get_options()
				menu = [Menu("Game Bots")]
				for x in xrange(self.bot_number):
					menu[0].add_multiple_option("Bot " + str(x + 1),character_names,0)
				menu[0].add_button("Done",DONEGAMEOPTS,True)
				menu[0].create()
				self.arcade_setup_bot_menu = MenuSet(menu,game)
			elif event != -1: #Option changed
				if event.option  == "Number of Bots":
					self.bot_number = event.option + 1
		elif self.arcade_setup_map:
			if game.key(KEY_BACKSPACE) and not self.backspace:
				self.arcade_setup_map = False
				self.backspace = True
			else:
				self.backspace = False
			event = self.mode_selection_menu.loop(game.events)
			if event != -1:
				menu = [Menu("Game Options")]
				if event == DEATHMATCH or event == TEAMDEATHMATCH:
					menu[0].add_multiple_option("Score limit",['None', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '35', '40', '45', '50', '60', '70', '80', '90', '100'],10)
					menu[0].add_multiple_option("Time limit",['None', '3 Minutes', '5 Minutes', '10 Minutes','15 Minutes', '20 Minutes', '25 Minutes', '30 Minutes', '35 Minutes', '40 Minutes'],0)
					menu[0].add_multiple_option("Scoring",["Kills","Kills/Suicides","Kills/Losses","Kills/Losses/Suicides"],1)
				else:
					menu[0].add_multiple_option("Lives",['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '35', '40', '45', '50', '60', '70', '80', '90', '100'],9)
					menu[0].add_multiple_option("Time limit",['None', '3 Minutes', '5 Minutes', '10 Minutes','15 Minutes', '20 Minutes', '25 Minutes', '30 Minutes', '35 Minutes', '40 Minutes'],0)
				if event == TEAMDEATHMATCH:
					menu[0].add_multiple_option("Friendly Fire",['On','On with score penalty','Off'],0)
				if event == TEAMELIMINATION:
					menu[0].add_multiple_option("Friendly Fire",['On','Off'],0)
				if event == DEATHMATCH:
					self.arcade_setup_mode = MODE_DEATHMATCH
					self.arcade_setup_team_mode = False
				elif event == TEAMDEATHMATCH:
					self.arcade_setup_mode = MODE_DEATHMATCH
					self.arcade_setup_team_mode = True
				elif event == ELIMINATION:
					self.arcade_setup_mode = MODE_DEATHMATCH
					self.arcade_setup_team_mode = False
				elif event == TEAMELIMINATION:
					self.arcade_setup_mode = MODE_DEATHMATCH
					self.arcade_setup_team_mode = True
				menu[0].add_multiple_option("Radar",["On","Off"],0)
				menu[0].add_multiple_option("One Shot Kill",["On","Off"],1)
				menu[0].add_multiple_option("Number of Bots",["1","2","3","4","5","6","7","8","9"],8)
				self.bot_number = 9
				menu[0].add_multiple_option("Music",[file[:-4] for file in os.listdir(os.path.dirname(sys.argv[0]) + "/music/game/") if file[-4:] == ".ogg"],self.level.recomended_muisc)
				menu[0].add_button("Done",DONEGAMEOPTS,True)
				menu[0].create()
				self.game_options_menu = MenuSet(menu,game)
		elif self.map_selection_menu:
			event = self.map_selection_menu.loop(game.events)
			print event
			print "End"
			if event == MAPRETURN or (game.key(KEY_BACKSPACE) and not self.backspace):
				self.map_selection_menu = False
				game.play_sound("/sounds/menu3/change.ogg")
			else:
				self.backspace = False
				if event != -1:
					#Load map's level object and make temporary images
					self.arcade_setup_map = event
					f = open(game.homedir + "/TimeSplitters Platinum Custom Maps/" + event + "/level.dat", 'rb')
					self.level = pickle.loads(zlib.decompress(f.read()))
					f.close()
					for x in xrange(5):
						if self.level.floors[x].image is not None:
							image_file = game.homedir + "/TimeSplitters Platinum Custom Maps/.temp" + str(x) + "." + ("png" if self.level.floors[x].imgfile[:-3] == "png" else "jpg")
							image_data = open(image_file,"wb")
							image_data.write(self.level.floors[x].image)
							image_data.close()
							self.level.floors[x].add_image(image_file)
		else:
			if self.options_menu_active != self.main_menu:
				event = self.options_menu_active.loop(self.main_menu,self.create_gradient)
			else:
				event = self.options_menu_active.loop(game.events)
			if event != -1:
				if event == LOGOUT:
					login_menu.logged_in = False
					self.menu[0].remove(self.logout_button)
				elif event == OPTTOG: #Toggle options menu
					game.play_sound("/sounds/menu3/change.ogg")
					if self.options_menu_active == options_menu:
						self.options_menu_active = self.main_menu
					else:
						self.options_menu_active = options_menu
						options_menu.return_key = True
				elif event == CONTROLS:
					game.play_sound("/sounds/menu3/change.ogg")
					if self.options_menu_active == controls_menu:
						self.options_menu_active = self.main_menu
					else:
						self.options_menu_active = controls_menu
						controls_menu.enter = True
						controls_menu.return_key = True
				elif event == BLOG:
					website("http://crytekuk.info/")
				elif event == ANDREW:
					website("http://ltsurge659.newgrounds.com/")
				elif event == ANDREWFFF:
					website("http://forfinancialfreedom.info/")
				elif event == NAMEMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_NAME,False)
				elif event == DATENEWMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_ESTABLISH,True)
				elif event == DATEOLDMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_ESTABLISH,False)
				elif event == PLAYSMOSTMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_PLAYS,True)
				elif event == PLAYSLEASTMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_PLAYS,False)
				elif event == LASTPLAYRECENTMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_LAST_PLAY,True)
				elif event == LASTPLAYLONGESTMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_LAST_PLAY,False)
				elif event == EDITNEWMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_LAST_EDIT,True)
				elif event == EDITOLDMAPS:
					self.map_selection_menu = self.make_map_selection_menu(ORDER_MAPS_LAST_EDIT,False)
				else:
					game.transfer_section(event[0])
	def exit(self):
		pass
def null():
	pass
class ControlsMenu(MenuSet):
	def __init__(self):
		self.menu = [None] * 3
		self.menu[0] = Menu("Controls")
		self.menu[0].add_text("You can change the keys used for the keyboard and mouse control modes. The keyboard mode uses the keyboard for turning. The mouse mode uses the mouse or trackpad to turn and aim. The level roation mode causes the level to rotate as the player faces forwards, the player roation mode causes the player to rotate as the level does not rotate.",700)
		self.menu[0].add_multiple_option("Turning mode",["Mouse","Keyboard"],game.controls[CONTROLS_TURNING_MODE])
		self.menu[0].add_multiple_option("Rotation mode",["Level rotation","Player rotation"],game.controls[CONTROLS_ROTATION_MODE])
		self.menu[0].add_button("Keyboard mode controls",1)
		self.menu[0].add_button("Mouse mode controls",2)
		self.menu[0].add_button("Apply and Save","SAVE",True)
		self.menu[0].add_button("Apply for this time only","APPLY",True)
		self.menu[0].create()
		self.menu[1] = Menu("Keyboard Mode Controls")
		self.menu[1].add_text("Press enter and then the key you wish to use for the control. There is no undo.",700)
		self.menu[1].add_key_option("Forward",game.controls[CONTROLS_KEYBOARD_FORWARD])
		self.menu[1].add_key_option("Backward",game.controls[CONTROLS_KEYBOARD_BACKWARD])
		self.menu[1].add_key_option("Strafe left",game.controls[CONTROLS_KEYBOARD_STRAFE_LEFT])
		self.menu[1].add_key_option("Strafe right",game.controls[CONTROLS_KEYBOARD_STRAFE_RIGHT])
		self.menu[1].add_key_option("Turn left",game.controls[CONTROLS_KEYBOARD_TURN_LEFT])
		self.menu[1].add_key_option("Turn right",game.controls[CONTROLS_KEYBOARD_TURN_RIGHT])
		self.menu[1].add_key_option("Fire",game.controls[CONTROLS_KEYBOARD_FIRE])
		self.menu[1].add_key_option("Switch weapon",game.controls[CONTROLS_KEYBOARD_SWITCH])
		self.menu[1].add_key_option("Reload",game.controls[CONTROLS_KEYBOARD_RELOAD])
		self.menu[1].add_key_option("Pause",game.controls[CONTROLS_KEYBOARD_PAUSE])
		self.menu[1].add_button("Done",0)
		self.menu[1].create()
		self.menu[2] = Menu("Mouse Mode Controls")
		self.menu[2].add_text("Press enter and then the key you wish to use for the control. There is no undo.",700)
		self.menu[1].add_key_option("Forward",game.controls[CONTROLS_MOUSE_FORWARD])
		self.menu[2].add_key_option("Backward",game.controls[CONTROLS_MOUSE_BACKWARD])
		self.menu[2].add_key_option("Strafe left",game.controls[CONTROLS_MOUSE_STRAFE_LEFT])
		self.menu[2].add_key_option("Strafe right",game.controls[CONTROLS_MOUSE_STRAFE_RIGHT])
		self.menu[2].add_key_option("Switch weapon",game.controls[CONTROLS_MOUSE_SWITCH])
		self.menu[2].add_key_option("Reload",game.controls[CONTROLS_MOUSE_RELOAD])
		self.menu[2].add_key_option("Pause",game.controls[CONTROLS_MOUSE_PAUSE])
		self.menu[2].add_button("Done",0)
		self.menu[2].create()
		MenuSet.__init__(self,self.menu,game)
	def loop(self,menu,in_game = False):
		event = MenuSet.loop(self,game.events)
		if event == "SAVE" or event == "APPLY":
			if event == "SAVE":
				update_controls()
			menu.menu_change = True
			event = CONTROLS
		elif event != -1: #Option changed
			if event.__class__ == MenuKeyOption:
				game.controls[event.id + 2] = event.current_value #Plus 2 for the first two irrelevant options
				event = -1
			else:
				if event.option  == "Turning mode":
					game.controls[CONTROLS_TURNING_MODE] = event.current_value
					if in_game:
						if event.current_value == MOUSE_TURNING:
							game.track_mouse()
						else:
							game.disable_mouse()
				else:
					game.controls[CONTROLS_ROTATION_MODE] = event.current_value
		return event
class OptionsMenu(MenuSet):
	def __init__(self):
		self.menu = [None]
		self.menu[0] = Menu("Options")
		self.menu[0].add_multiple_option("Music Volume",[str(x) for x in range(11)],game.options[OPTION_MUSIC_VOLUME])
		self.menu[0].add_multiple_option("Sounds Volume",[str(x) for x in range(11)],game.options[OPTION_SOUND_VOLUME])
		self.menu[0].add_boolean_option("Fullscreen on startup",game.options[OPTION_FULLSCREEN_STARTUP])
		self.menu[0].add_boolean_option("Scale display to fullscreen aspect ratio",game.options[OPTION_FULLSCREEN_SCALE])
		self.menu[0].add_multiple_option("Menu Theme",["Blue","Red","Green","Yellow","Orange","Pink","White","Black"],game.options[OPTION_THEME])
		self.menu[0].add_button("Apply and Save","SAVE",True)
		self.menu[0].add_button("Apply for this time only","APPLY",True)
		self.menu[0].create()
		MenuSet.__init__(self,self.menu,game)
	def loop(self,menu,create_gradient = null):
		event = MenuSet.loop(self,game.events)
		if event == "SAVE" or event == "APPLY":
			if event == "SAVE":
				update_options()
			menu.menu_change = True
			event = OPTTOG
		elif event != -1: #Option changed
			if event.option  == "Music Volume":
				game.options[OPTION_MUSIC_VOLUME] = event.current_value
				game.set_music_volume(event.current_value)
			elif event.option == "Fullscreen on startup":
				game.options[OPTION_FULLSCREEN_STARTUP] = event.current_value
			elif event.option == "Menu Theme":
				game.options[OPTION_THEME] = event.current_value
				create_gradient()
				menu_theme.set_theme(game)
			elif event.option == "Scale display to fullscreen aspect ratio":
				game.options[OPTION_FULLSCREEN_SCALE] = event.current_value
				game.scale_to_screen = event.current_value
				if game.is_fullscreen():
					game.enter_fullscreen()
			elif event.option == "Sounds Volume":
				game.options[OPTION_SOUND_VOLUME] = event.current_value
			event = -1
		return event
#The login menu for when online features are requested
class LoginMenuSet(MenuSet):
	def __init__(self):
		pass
	def init(self):
		self.username = ""
		self.password = ""
		self.menu = [None] * 4
		self.menu[0] = Menu("Login or Register for Online")
		self.menu[0].add_text("To use the online features of this game you must have an account registered at CrytekUK.info. You can login with your details or register quick and easily.",700)
		self.menu[0].add_button("Login",1)
		self.menu[0].add_button("Register","REG",True)
		self.menu[0].add_button("Cancel","CANCEL",True)
		self.menu[0].create()
		self.menu[1] = Menu("Login to CrytekUK.info")
		self.username_input = self.menu[1].add_text_input("Username: ",max = 60)
		self.password_input = self.menu[1].add_text_input("Password: ",max = 64)
		self.menu[1].add_button("Submit","LOGIN",True)
		self.menu[1].add_button("Register","REG",True)
		self.menu[1].add_button("Cancel","CANCEL",True)
		self.menu[1].create()
		self.menu[2] = Menu("Login to CrytekUK.info")
		self.menu[2].add_text("Logging in",500,1,40)
		self.menu[2].create()
		MenuSet.__init__(self,self.menu,game)
		self.transfer = True
		self.logged_in = False
	def loop_login(self):
		if self.transfer == True:
			self.transfer = False
			self.menu_active = 0
			self.menu_change = True
			self.return_key = True
			self.waiting_for_request = False
			self.logged_in = False
			self.login_prompt()
		event = self.loop(game.events)
		if event == "CANCEL":
			self.transfer = True
			self.password = ""
			self.username = ""
		elif event == "REG":
			website("http://crytekuk.info/forums/ucp.php?mode=register")
		elif event == "LOGIN" and self.username_input.text != "" and self.password_input.text != "":
			self.menu_active = 2
			self.menu_change = True
			self.login_request = HTTPRequestThread("http://www.crytekuk.info/tsp_requests/login.php",{'username': self.username_input.text, 'password': self.password_input.text},10)
			self.waiting_for_request = True
			self.password = self.password_input.text
			self.username = self.username_input.text
		if self.waiting_for_request == True:
			if not self.login_request.isAlive():
				self.waiting_for_request = False
				if self.login_request.response_number == "200": #200 OK
					if self.login_request.content == "Y": #Login Successful
						self.logged_in = True
						event = "SUCCESS"
					elif self.login_request.content == "N": #Authentication error
						self.login_prompt("The login details you provided are not correct")
					elif self.login_request.content == "L": #Try limit reached
						self.login_prompt("The login details you provided are not correct. You have reached your login limit for this username for " + self.login_request.content + " minutes.")
					elif self.login_request.content == "": #Try limit reached
						self.login_prompt("The server gave an empty response.")
					else:
						self.login_prompt("There has been an error with the login scripts. Please look at terminal output for more details")
						print "Send this message, including the following to Matthew Mitchell (god0fgod):\n"
						print self.login_request.content
				else:
					print "Login Error: Server responded with a " + str(self.login_request.response_number) + " http status code. Send this message, including the following to Matthew Mitchell (god0fgod):\n"
					print self.login_request.details
					self.login_prompt("There has been a problem while attempting to login. This may be a temporary issue. Please check terminal output for a desciptive error.")
				self.password_input.text = ""
		return event
	def login_prompt(self,notice=None):
		self.menu[1] = Menu("Login to CrytekUK.info")
		if notice is not None:
			self.menu[1].add_text(notice,500,1,30)
			self.menu_active = 1
			self.menu_change = True
		self.username_input = self.menu[1].add_text_input("Username: ",self.username,max = 60)
		self.password_input = self.menu[1].add_text_input("Password: ",max = 64,password=True)
		self.menu[1].add_button("Submit","LOGIN",True)
		self.menu[1].add_button("Register","REG",True)
		self.menu[1].add_button("Cancel","CANCEL",True)
		self.menu[1].create()
#Import psyco
try:
	import psyco
	psyco.profile(0)
except ImportError:
	pass
################################################# MEM LEAK DEBUGGING #####################################################
'''import cherrypy
import dowser
cherrypy.tree.mount(dowser.Root())
cherrypy.config.update({
  'environment': 'embedded',
  'server.socket_port': 80
})
cherrypy.server.quickstart()
cherrypy.engine.start(blocking=False)'''
######################################################## END ################################################################
if __name__ == '__main__': #Run if being run directly and not as a module
	game = Game("TimeSplitters Platinum Pre-Alpha",[1280,720])  #1280x720 HD resolution game. Creates an object with the game Surface
	#Set up version file
	if not os.path.isdir(game.homedir + "/.timesplitters_platinum"):
		os.mkdir(game.homedir + "/.timesplitters_platinum")
	if not os.path.isdir(game.homedir + "/TimeSplitters Platinum Custom Maps"):
		os.mkdir(game.homedir + "/TimeSplitters Platinum Custom Maps")
	if os.path.exists(game.homedir + "/.timesplitters_platinum/version"):
		version_file = open(game.homedir + "/.timesplitters_platinum/version","rb")
		last_used_version = pickle.load(version_file)
		version_file.close()
		if last_used_version != TSPVERSION:
			change_version = True
		else:
			change_version = False
	else:
		change_version = True
		last_used_version = [0,0,3]
	if change_version == True:#If any of the files needs to be converted for a new version, it will be done here.
		version_file = open(game.homedir + "/.timesplitters_platinum/version","wb")
		pickle.dump(TSPVERSION,version_file,2)
		version_file.close()
	if os.path.exists(game.homedir + "/.timesplitters_platinum/options.sav"):
		options_file = open(game.homedir + "/.timesplitters_platinum/options.sav","rb")
		game.options = pickle.load(options_file)
		options_file.close()
	else:
		game.options = {OPTION_MUSIC_VOLUME: 10,OPTION_FULLSCREEN_STARTUP: False,OPTION_THEME: 0,OPTION_FULLSCREEN_SCALE: False,OPTION_SOUND_VOLUME: 10}
		update_options()
	if os.path.exists(game.homedir + "/.timesplitters_platinum/controls.sav"):
		controls_file = open(game.homedir + "/.timesplitters_platinum/controls.sav","rb")
		game.controls = pickle.load(controls_file)
		controls_file.close()
	else:
		game.controls = [1,0,KEY_W,KEY_S,KEY_A,KEY_D,KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_R,KEY_P,KEY_W,KEY_S,KEY_A,KEY_D,KEY_SPACE,KEY_R,KEY_P]
		update_controls()
	game.volume = game.options[OPTION_SOUND_VOLUME]
	menu_theme.set_theme(game)
	game.scale_to_screen = game.options[OPTION_FULLSCREEN_SCALE]
	weapon_classes = [AK47,Revolver,Shotgun,Minigun]
	weapon_list = ["AK-47","Garrett Revolver","Shotgun","Minigun","None"]
	character_classes = [Monkey]
	character_names = ["Monkey"]
	login_menu = LoginMenuSet()
	options_menu = OptionsMenu()
	controls_menu = ControlsMenu()
	game.add_section(MainMenu()) #Add MainMenu object as a section
	game.add_section(AnacondaGame()) #Same for AnacondaGame
	game.add_section(Mapmaker())
	game.add_section(GameSession())
	game.add_section(MonkeyCurling())
	game.set_section(game.get_section(0)) #Sets MainMenu as the current section. It was added first so the index is 0. AnacondaGame is index 1 for sections list.
	if game.options[1]:
		game.enter_fullscreen()
	game.start()