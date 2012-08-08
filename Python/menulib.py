#!/usr/bin/env python2.3
#
#  Menu library for pygame
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

#Import modules
import pygame,time,os,sys
from datetime import datetime
from pygame.locals import *
from string import capitalize
from scalelib import *
#Strings for each allowed key
key_strings = {KEY_1: "1",KEY_2: "2",KEY_3: "3",KEY_4: "4",KEY_5: "5",KEY_6: "6",KEY_7: "7",KEY_8: "8",KEY_9: "9",KEY_0: "0",KEY_Q: "Q",KEY_W: "W",KEY_E: "E",KEY_R: "R",KEY_T: "T",KEY_Y: "Y",KEY_U: "U",KEY_I: "I",KEY_O: "O",KEY_P: "P",KEY_A: "A",KEY_S: "S",KEY_D: "D",KEY_F: "F",KEY_G: "G",KEY_H: "H",KEY_J: "J",KEY_K: "K",KEY_L: "L",KEY_Z: "Z",KEY_X: "X",KEY_C: "C",KEY_V: "V",KEY_B: "B",KEY_N: "N",KEY_M: "M",KEY_UP: "Up",KEY_RIGHT: "Right",KEY_DOWN: "Down",KEY_LEFT: "Left",KEY_SPACE: "Space",KEY_BACKSPACE: "Backspace",KEY_DELETE: "Delete",KEY_ENTER: "Enter",KEY_ESCAPE: "Escape",KEY_TAB: "Tab"}
#Functions
def remove_from_list(item,list):
	for x in xrange(len(list)):
		if item == list[x]:
			del list[x]
			break
#Global variables for thumb change
time_of_last_thumb = 0
current_thumb = 1
object_for_thumb = None
#Classes
class MenuTheme():
	def set_theme(self,game):
		self.text_colour = (255,255,255)
		if game.options[2] == 0: #Blue
			self.not_selected_colour = (30,30,50)
			self.selected_colour = (30,80,120)
		elif game.options[2] == 1: #Red
			self.not_selected_colour = (50,20,20)
			self.selected_colour = (120,40,30)
		elif game.options[2] == 2: #Green
			self.not_selected_colour = (30,50,30)
			self.selected_colour = (30,120,40)
		elif game.options[2] == 3: #Yellow
			self.not_selected_colour = (100,100,0)
			self.selected_colour = (180,180,20)
		elif game.options[2] == 4: #Orange
			self.not_selected_colour = (150,70,0)
			self.selected_colour = (200,100,30)
		elif game.options[2] == 5: #Pink
			self.not_selected_colour = (160,90,90)
			self.selected_colour = (230,130,130)
		elif game.options[2] == 6: #White
			self.not_selected_colour = (200,200,200)
			self.selected_colour = (255,255,255)
			self.text_colour = (0,0,0)
		elif game.options[2] == 7: #Black
			self.not_selected_colour = (0,0,0)
			self.selected_colour = (25,25,30)
class Menu():
	def __init__(self,name,parent=-1):
		self.parent = parent
		self.last_menu = 0
		self.items = []
		self.interactitems = []
		self.textentries = []
		self.options = []
		self.selected = 0
		self.title = MenuButton(name,None,False,True)
		self.score_rank = 0
		self.key_wait = False
		self.map_selected = False
	def add_scrollable_area(self,area,height):
		area.prepare(height)
		self.items.append(area)
		if area.interactitems:
			self.interactitems.append(area)
		self.options += area.options #The area's options are the menu's.
	def add_button(self,name,event,type = False):
		item = MenuButton(name,event,type)
		self.items.append(item)
		self.interactitems.append(item)
		return item
	def add_map_preview_button(self,name,established,edit,plays,last_play,description,thumbs):
		item = MenuMapPreviewButton(name,established,edit,plays,last_play,description,thumbs)
		self.items.append(item)
		self.interactitems.append(item)
		return item
	def add_text(self,text,size,a=0,s=25):
		item = MenuText(text,size,a,s)
		self.items.append(item)
		return item
	def add_boolean_option(self,option,d,size=30):
		item = MenuBooleanOption(option,d,size)
		self.items.append(item)
		self.interactitems.append(item)
		self.options.append(item)
		return item
	def add_multiple_option(self,option,l,d=0,size=30):
		item = MenuMultipleOption(option,l,d,size)
		self.items.append(item)
		self.interactitems.append(item)
		self.options.append(item)
		return item
	def add_text_input(self,name,text = "",width = 500,size = 30,max = 100,password = False):
		item = MenuTextInput(name,text,width,size,max,password)
		self.items.append(item)
		self.interactitems.append(item)
		self.textentries.append(item)
		return item
	def add_new_score(self,name,score):
		self.score_rank += 1
		item = MenuNewScore(self.score_rank,name,score)
		self.items.append(item)
		self.interactitems.append(item)
		self.textentries.append(item)
		return item
	def add_score(self,name,score):
		if self.score_rank == 10:
			self.score_rank = 1
		else:
			self.score_rank += 1
		item = MenuNewScore(self.score_rank,name,score)
		self.items.append(item)
		return item
	def add_key_option(self,name,key,size=30):
		item = MenuKeyOption(name,key,size)
		self.items.append(item)
		self.interactitems.append(item)
		self.options.append(item)
		return item
	def create(self,select = 0):
		width = self.title.size[0]
		height = self.title.size[1]
		for item in self.items:
			if item.size[0] > width:
				width = item.size[0]
			height += item.size[1]
		self.s = Surface((width,height))
		self.s.fill((10,10,10,220))
		if len(self.interactitems) > 0:
			self.interactitems[select].selected = True
			if self.interactitems[select].__class__ == MenuMapPreviewButton:
				global current_thumb
				current_thumb = 1
				self.interactitems[select].size[1] = 200
				self.map_selected = self.interactitems[select]
	def render(self):
		offset = self.title.create(self,0)
		self.title.render(self)
		for item in self.items:
			offset = item.create(self,offset)
			item.render(self)
		self.s.round_corners(30)
	def select(self,up):
		GameClass.instance.play_sound("/sounds/menu3/move.ogg")
		no_change = False
		if self.interactitems[self.selected].__class__ == MenuScrollArea:
			no_change = self.interactitems[self.selected].select(up,self)
		if not no_change:
			length = len(self.interactitems) - 1
			if length > -1:
				self.s.fill((10,10,10,220))
				self.interactitems[self.selected].selected = False
				self.interactitems[self.selected].render(self)
				if up == True:
					if self.selected > 0:
						self.selected -= 1
					else:
						self.selected = length 
				else:
					if self.selected < length:
						self.selected += 1
					else:
						self.selected = 0
				if self.interactitems[self.selected].__class__ == MenuScrollArea:
					self.create(self.selected)
					if up: #Prepare and select bottom one
						self.interactitems[self.selected].prepare(self.interactitems[self.selected].size[1],len(self.interactitems[self.selected].interactitems)-1)
					else: #Prepare and select top one
						self.interactitems[self.selected].prepare(self.interactitems[self.selected].size[1],0)
					self.render()
				else:
					if self.interactitems[self.selected].__class__ == MenuMapPreviewButton:
						global current_thumb
						current_thumb = 1
						NSLog("Change thumb")
						self.interactitems[self.selected].size[1] = 200
						self.map_selected = self.interactitems[self.selected]
						NSLog("Change map selected")
						self.create(self.selected)
						self.render()
						NSLog("Done rendering")
					elif self.map_selected:
						global object_for_thumb
						object_for_thumb = None #No longer needs to change thumbnail
						self.map_selected.size[1] = 60
						self.map_selected = False
						self.create(self.selected)
						self.render()
					self.interactitems[self.selected].selected = True
					self.interactitems[self.selected].render(self)
	def activate(self,event):
		if len(self.interactitems) > 0:
			return self.interactitems[self.selected].activate(self,event)
		else:
			return None
	def get_options(self):
		option_values = []
		for item in self.options:
			option_values.append(item.current_value)
		return option_values
	def remove(self,rm_item): #Removes an object from the menu.
		remove_from_list(rm_item,self.items)
		remove_from_list(rm_item,self.interactitems)
		remove_from_list(rm_item,self.textentries)
		temp = self.selected
		self.create()
		if temp == 0:
			self.selected = 0
		else:
			self.selected = temp - 1
		self.render()
class MenuScrollArea(Menu):
	def __init__(self):
		self.items = []
		self.interactitems = []
		self.textentries = []
		self.options = []
		self.item_selected = 0
		self.items_offset = 0
		self.map_selected = False
	def prepare(self,height,select = 0):
		width = 0
		for item in self.items:
			if item.size[0] > width:
				width = item.size[0]
		self.s = Surface((width,height))
		self.size = (width,height)
		self.s.fill(menu_theme.not_selected_colour[:3] + (255,))
		if len(self.interactitems) > 0:
			self.item_selected = select
			self.interactitems[select].selected = True
			if self.interactitems[select].__class__ == MenuMapPreviewButton:
				global current_thumb
				current_thumb = 1
				self.interactitems[select].size[1] = 200
				self.map_selected = self.interactitems[select]
	def create(self,menu,offset):
		self.offset = offset
		return offset + self.size[1]
	def render(self,menu):
		NSLog("Rendering scrollable area")
		offset = 0 #Take away the offset into the items for scrolling
		for item in self.items:
			offset = item.create(self,offset)
		NSLog("1")
		if self.interactitems:
			if self.interactitems[self.item_selected].offset < self.items_offset: #Item offset below offset for items so new offset must start at the item's offset
				self.items_offset = self.interactitems[self.item_selected].offset
			elif self.interactitems[self.item_selected].offset + self.interactitems[self.item_selected].s.get_height() > self.size[1] + self.items_offset: #Item offset above height of area at offset so new offset must put the item at the bottom of the area
				self.items_offset = self.interactitems[self.item_selected].offset - self.size[1] + self.interactitems[self.item_selected].s.get_height() 
		NSLog("2")
		for item in self.items:
			item.offset -= self.items_offset
			if item.offset + item.s.get_height() > 0 and item.offset < self.size[1]:
				item.render(self)
			item.offset += self.items_offset
		NSLog("3")
		menu.s.blit(self.s,(0,self.offset))
		NSLog("Fin Rendering scrollable area")
	def activate(self,menu,event):
		if len(self.interactitems) > 0:
			return self.interactitems[self.item_selected].activate(self,event)
		else:
			return None
	def select(self,up,menu):
		'''Returns wether or not the selection remains within the area'''
		self.s.fill(menu_theme.not_selected_colour[:3] + (255,))
		length = len(self.interactitems) - 1
		self.interactitems[self.item_selected].selected = False
		self.interactitems[self.item_selected].render(self)
		if self.map_selected:
			global object_for_thumb
			object_for_thumb = None #No longer needs to change thumbnail
			self.map_selected.size[1] = 60
		if up == True:
			if self.item_selected > 0:
				self.item_selected -= 1
			else:
				return False
		else:
			if self.item_selected < length:
				self.item_selected += 1
			else:
				return False
		re_render = False
		if self.interactitems[self.item_selected].__class__ == MenuMapPreviewButton:
			global current_thumb
			current_thumb = 1
			re_render = True
		elif self.map_selected: #Only when no longer any map selection
			self.map_selected = False
			re_render = True
		if re_render:
			self.prepare(self.size[1],self.item_selected)
			menu.create()
			menu.render()
		self.interactitems[self.item_selected].selected = True
		self.interactitems[self.item_selected].render(self)
		return True
class MenuButton():
	def __init__(self,name,event,type,title = False):
		self.title = title
		self.name = name
		self.selected = False
		self.event = (type,event)
		if title:
			font_surface = title_font.render(name,menu_theme.text_colour)
			self.hp = 12
		else:
			self.hp = 6
			font_surface = button_font.render(name,menu_theme.text_colour)
		self.size = [font_surface.get_width() + 30,font_surface.get_height() + self.hp]
	def create(self,menu,offset):
		self.offset = offset
		menu_width = menu.s.get_width()
		if self.title:
			font_surface = title_font.render(self.name,menu_theme.text_colour)
		else:
			font_surface = button_font.render(self.name,menu_theme.text_colour)
		self.s = Surface((menu_width,font_surface.get_height() + self.hp)) #20 and 6 for padding
		return offset + self.s.get_height()
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		if self.title:
			font_surface = title_font.render(self.name,menu_theme.text_colour)
		else:
			font_surface = button_font.render(self.name,menu_theme.text_colour)
		self.s.blit(font_surface,((menu.s.get_width() - font_surface.get_width())/2,3))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		if e == KEY_ENTER:
			return self.event
		return None
class MenuMapPreviewButton():
	def __init__(self,name,established,edit,plays,last_play,description,thumbs):
		self.name = name
		established_text = information_font.render(datetime.fromtimestamp(established).strftime("%d/%m/%y"),menu_theme.text_colour)
		edit_text = information_font.render(datetime.fromtimestamp(edit).strftime("%d/%m/%y"),menu_theme.text_colour)
		plays_text = information_font.render(str(plays),menu_theme.text_colour)
		established_time_text = information_font.render(datetime.fromtimestamp(established).strftime("%H:%M"),menu_theme.text_colour)
		edit_time_text = information_font.render(datetime.fromtimestamp(edit).strftime("%H:%M"),menu_theme.text_colour)
		if last_play:
			last_play_text = information_font.render(datetime.fromtimestamp(last_play).strftime("%d/%m/%y"),menu_theme.text_colour)
			last_play_time_text = information_font.render(datetime.fromtimestamp(last_play).strftime("%H:%M"),menu_theme.text_colour)
		else:
			last_play_text = information_font.render("Never",menu_theme.text_colour)
		#Make surface for information at the top
		self.info_surface = Surface((520,40))
		self.info_surface.set_background_alpha(0)
		self.info_surface.blit(established_text,(65 - established_text.get_width()/2.,0))
		self.info_surface.blit(edit_text,(195 - edit_text.get_width()/2.,0))
		self.info_surface.blit(plays_text,(325 - plays_text.get_width()/2.,10))
		self.info_surface.blit(established_time_text,(65 - established_time_text.get_width()/2.,20))
		self.info_surface.blit(edit_time_text,(195 - edit_time_text.get_width()/2.,20))
		self.description = description_font.render_wordwrap(description,800, menu_theme.text_colour,0)
		if last_play:
			self.info_surface.blit(last_play_text,(455 - last_play_text.get_width()/2.,0))
			self.info_surface.blit(last_play_time_text,(455 - last_play_time_text.get_width()/2.,20))
		else:
			self.info_surface.blit(last_play_text,(455 - last_play_text.get_width()/2.,10))
		self.thumbs = [open_image(thumb) for thumb in thumbs]
		self.selected = False
		self.size = [1050,60]
	def create(self,menu,offset):
		self.offset = offset
		self.s = Surface((menu.s.get_width(),self.size[1])) #20 and 6 for padding
		return offset + self.s.get_height()
	def render(self,menu):
		NSLog("Rendering")
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		NSLog("1")
		self.s.blit(button_font.render(self.name,menu_theme.text_colour),(10,10))
		self.s.blit(self.info_surface,(menu.s.get_width() - 530,10))
		NSLog("2")
		if self.selected:
			global object_for_thumb
			global time_of_last_thumb
			global current_thumb
			self.s.blit(self.description,(220,80))
			self.s.blit(self.thumbs[current_thumb - 1],(60,70))
			NSLog("3")
			time_of_last_thumb = time.time()
			object_for_thumb = self
		NSLog("4")
		menu.s.blit(self.s,(0,self.offset))
		NSLog("End render")
	def activate(self,m,e):
		if e == KEY_ENTER:
			return [True,self.name]
		return -1
class MenuTextInput():
	def __init__(self,name,text,width,size,max,password):
		self.text_font = Font("Geneva",size/1.5)
		self.selected = False
		self.size = [width,size]
		self.text = text
		self.name = name
		self.no_letters = len(text)
		self.max_letters = max
		self.password = password
		self.name_surface = self.text_font.render(self.name,menu_theme.text_colour)
		self.s = None
	def create(self,menu,offset):
		self.offset = offset
		menu_width = menu.s.get_width()
		self.s = Surface((menu_width,self.size[1]))
		return offset + self.size[1]
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		self.s.blit(self.name_surface,(20,3))
		self.s.blit(self.text_font.render("*" * len(self.text) if self.password else self.text,menu_theme.text_colour),(20 + self.name_surface.get_width(),3))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		pass
class MenuNewScore():
	def __init__(self,pos,default_name,score):
		self.text_font = Font("Geneva",15)
		self.selected = False
		self.score_surface = self.text_font.render(str(score),menu_theme.text_colour)
		self.size = [600 + self.score_surface.get_width(),27]
		self.text = default_name
		self.pos = pos
		self.no_letters = len(default_name)
		self.max_letters = 20
	def create(self,menu,offset):
		self.offset = offset
		menu_width = menu.s.get_width()
		self.s = Surface((menu_width,27)) #6 for padding on top of 21
		return offset + self.s.get_height()
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		self.text = self.text.capitalize()
		self.name_surface = self.text_font.render(str(self.pos) + ". " + self.text,menu_theme.text_colour)
		self.s.blit(self.name_surface,(20,3))
		self.s.blit(self.score_surface,((menu.s.get_width() - self.score_surface.get_width() - 20),3))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		pass
class MenuScore():
	def __init__(self,pos,name,score):
		text_font = Font("Geneva",15)
		self.score_surface = text_font.render(str(score),menu_theme.text_colour)
		self.size = [600 + self.score_surface.get_width(),27]
		self.name = name
		self.name_surface = text_font.render(str(pos) + ". " + self.name,menu_theme.text_colour)
	def create(self,menu,offset):
		self.offset = offset
		menu_width = menu.s.get_width()
		self.s = Surface((menu_width,27)) #6 for padding on top of 21
		return offset + self.s.get_height()
	def render(self,menu):
		self.s.blit(self.name_surface,(20,3))
		self.s.blit(self.score_surface,((menu.s.get_width() - self.score_surface.get_width() - 20),3))
		menu.s.blit(self.s,(0,self.offset))
class MenuText():
	def __init__(self,text,w,a,size):
		self.text_font = Font("Geneva",size)
		self.text = text
		self.w = w
		self.a = a
		font_surface = self.text_font.render_wordwrap(self.text, self.w, menu_theme.text_colour,self.a)
		self.size = [font_surface.get_width() + 30,font_surface.get_height() + 20]
	def create(self,menu,offset):
		font_surface =  self.text_font.render_wordwrap(self.text, self.w, menu_theme.text_colour,self.a)
		self.offset = offset
		menu_width = menu.s.get_width()
		self.s = Surface((menu_width,font_surface.get_height() + 20))
		return offset + self.s.get_height()
	def render(self,menu):
		font_surface = self.text_font.render_wordwrap(self.text,self.w,menu_theme.text_colour,self.a)
		self.s.fill(menu_theme.not_selected_colour)
		self.s.blit(font_surface,((menu.s.get_width() - font_surface.get_width())/2,10))
		menu.s.blit(self.s,(0,self.offset))
class MenuBooleanOption():
	def __init__(self,option,d,size):
		self.option = option
		self.text_font = Font("Geneva",size)
		self.selected = False
		option_text = self.text_font.render(option,menu_theme.text_colour)
		if d:
			dt = "Yes"
		else:
			dt = "No"
		self.current_value = d
		boolean_text = self.text_font.render(dt,menu_theme.text_colour)
		self.size = [option_text.get_width() + boolean_text.get_width() + 130,max(option_text.get_height(),boolean_text.get_height()) + 10]
	def create(self,menu,offset):
		self.offset = offset
		self.s = Surface((menu.s.get_width(),self.size[1])) #20 and 40 for padding
		return offset + self.s.get_height()
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		if self.current_value:
			dt = "Yes"
		else:
			dt = "No"
		option_text = self.text_font.render(self.option,menu_theme.text_colour)
		boolean_text = self.text_font.render(dt,menu_theme.text_colour)
		self.s.blit(option_text,(15,5))
		self.s.blit(boolean_text,(self.s.get_width() - 15 - boolean_text.get_width(),5))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		self.current_value = not self.current_value
		self.render(m)
		if e != KEY_ENTER:
			return self
		else:
			return [True,self]
class MenuMultipleOption():
	def __init__(self,option,values,default,size):
		self.text_font = Font("Geneva",size)
		self.selected = False
		self.option = option
		option_text = self.text_font.render(option,menu_theme.text_colour)
		self.current_value = default
		self.values = values
		value_text = self.text_font.render(self.values[self.current_value],menu_theme.text_colour)
		self.size = [option_text.get_width() + value_text.get_width() + 130,max(option_text.get_height(),value_text.get_height()) + 10]
	def create(self,menu,offset):
		self.offset = offset
		self.s = Surface((menu.s.get_width(),self.size[1])) #20 and 40 for padding
		return offset + self.s.get_height()
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		option_text = self.text_font.render(self.option,menu_theme.text_colour)
		value_text = self.text_font.render(self.values[self.current_value],menu_theme.text_colour)
		self.s.blit(option_text,(15,5))
		self.s.blit(value_text,(self.s.get_width() - 15 - value_text.get_width(),5))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		if e == KEY_LEFT:
			if self.current_value == 0:
				self.current_value = len(self.values) - 1
			else:
				self.current_value -= 1
		else:
			if self.current_value + 1 == len(self.values):
				self.current_value = 0
			else:
				self.current_value += 1
		self.render(m)
		if e != KEY_ENTER:
			return self
		else:
			return [True,self]
class MenuKeyOption():
	next_id = 0
	def __init__(self,name,key,size):
		self.id = MenuKeyOption.next_id
		MenuKeyOption.next_id += 1
		self.text_font = Font("Geneva",size)
		self.selected = False
		self.name = name
		option_text = self.text_font.render(name,menu_theme.text_colour)
		self.current_value = key
		value_text = self.text_font.render(key_strings[key],menu_theme.text_colour)
		self.size = [option_text.get_width() + value_text.get_width() + 130,max(option_text.get_height(),value_text.get_height()) + 10]
	def create(self,menu,offset):
		self.offset = offset
		self.s = Surface((menu.s.get_width(),self.size[1])) #20 and 40 for padding
		return offset + self.s.get_height()
	def render(self,menu):
		if not self.selected:
			self.s.fill(menu_theme.not_selected_colour)
		else:
			self.s.fill(menu_theme.selected_colour)
		option_text = self.text_font.render(self.name,menu_theme.text_colour)
		value_text = self.text_font.render("Press key" if menu.key_wait else key_strings[self.current_value],menu_theme.text_colour)
		self.s.blit(option_text,(15,5))
		self.s.blit(value_text,(self.s.get_width() - 15 - value_text.get_width(),5))
		menu.s.blit(self.s,(0,self.offset))
	def activate(self,m,e):
		if m.key_wait:
			self.current_value = e
			m.key_wait = False
			self.render(m)
			return self
		elif e == KEY_ENTER:
			m.key_wait = True
			self.render(m)
			return [True,-1]
class MenuSet():
	def __init__(self,menus,surface):
		self.menu = menus
		self.menu_active = 0
		self.menu_change = True
		self.surface = surface
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		self.back_key = False
		self.return_key = False
		self.no_letter = 0
		self.last_input = 0
		self.last_letter = ""
		self.repeated_letter = False
		self.cursor = True
	def loop(self,events):
		global object_for_thumb
		global time_of_last_thumb
		global current_thumb
		NSLog("Doing thumb things")
		if object_for_thumb is not None and time_of_last_thumb + 1 < time.time():
			if current_thumb == len(object_for_thumb.thumbs):
				current_thumb = 1
			else:
				current_thumb += 1
			self.menu_change = True
		NSLog("Done it")
		if self.menu_change: #Set to true if the menu is being changed so it re-renders a new menu.
			self.menu[self.menu_active].render()
			self.menu_change = False
		self.surface.blit(self.menu[self.menu_active].s,((self.surface.get_width() - self.menu[self.menu_active].s.get_width())/2,(self.surface.get_height() - self.menu[self.menu_active].s.get_height())/2))
		if self.menu[self.menu_active].key_wait:
			latest_key = self.surface.get_latest_key()
			if latest_key in key_strings:
				#Make the game believe all the keys which control the menus have already been pressed as one would have been
				self.up = True
				self.down = True
				self.left = True
				self.right = True
				self.return_key = True
				self.back_key = True
				return self.menu[self.menu_active].activate(latest_key)
			else:
				return -1
		if not self.surface.fade_screen() or self.surface.unfade(): #Only process input when not fading out.
			if self.surface.key(KEY_UP):
				if self.up == False:
					self.menu[self.menu_active].select(True)
					self.menu_change = True
					self.up = True
			else:
				self.up = False
			if self.surface.key(KEY_DOWN) or self.surface.key(KEY_TAB):
				if self.down == False:
					self.menu[self.menu_active].select(False)
					self.menu_change = True
					self.down = True
			else:
				self.down = False
			if self.surface.key(KEY_LEFT):
				if self.left == False:
					self.menu_change = True
					self.left = True
					event = self.menu[self.menu_active].activate(KEY_LEFT)
					if event != None:
						return event
			else:
				self.left = False
			if self.surface.key(KEY_RIGHT):
				if self.right == False:
					self.menu_change = True
					self.right= True
					event = self.menu[self.menu_active].activate(KEY_RIGHT)
					if event != None:
						return event
			else:
				self.right = False
			if self.surface.key(KEY_ENTER):
				if self.return_key == False:
					event = self.menu[self.menu_active].activate(KEY_ENTER)
					self.return_key = True
					if event != None:
						if not event[0]:
							if event[1] < len(self.menu) and event != None:
								self.menu[event[1]].last_menu = self.menu_active
								self.menu_active = event[1]
								self.menu_change = True
								self.surface.play_sound("/sounds/menu3/change.ogg")
						else:
							return event[1]
			else:
				self.return_key = False
			backspace_ok = True
			if len(self.menu[self.menu_active].interactitems) > 0:
				if self.menu[self.menu_active].interactitems[self.menu[self.menu_active].selected] in self.menu[self.menu_active].textentries:
					for event in events:
						if event[0] == KEYDOWN:
							text_entry = self.menu[self.menu_active].interactitems[self.menu[self.menu_active].selected]
							letter = ""
							print ord(event[1])
							if ord(event[1]) != 127:
								try:
									letter = event[1]
								except: #Ignore any flase character input
									pass
								if text_entry.no_letters < text_entry.max_letters and len(letter) == 1 and not ord(event[1]) in [63272,63236,63237,63238,63239,63240,63242,63232,63233,63234,63235] and ord(event[1]) > 31: #63272,63236,63237,63238,63239,63240,63242,63232,63233,63234,63235 are the delete key, the function keys and the arrow keys
									text_entry.no_letters += 1
									text_entry.text += letter
							else:
								letter = "BK"
								if text_entry.no_letters > 0:
									text_entry.no_letters -= 1
									text_entry.text = text_entry.text[:-1]
							self.menu_change = True
							break
					return "TXT"
					backspace_ok = False
			if backspace_ok:
				if self.surface.key(KEY_BACKSPACE) or self.surface.key(KEY_ESCAPE):
					if self.back_key == False:
						if not self.menu[self.menu_active].parent == -2:
							self.menu_change = True
						if self.menu[self.menu_active].parent == -1:
							self.menu_active = self.menu[self.menu_active].last_menu
						elif not self.menu[self.menu_active].parent == -2:
							self.menu_active = self.menu[self.menu_active].parent
						self.back_key = True
				else:
					self.back_key = False
		return -1
menu_theme = MenuTheme()
description_font = Font("Geneva",20)
button_font = Font("NEUROPOL",30)
information_font = Font("NEUROPOL",20)
title_font = Font("NEUROPOL",40)