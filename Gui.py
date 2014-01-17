"""
2.0
The Gui class for the game.
"""

import pygame
from pygame.locals import *

class Gui(object):
	"""a Gui class intended to be a one size fits all
	for all the Gui creation in the game """
	def __init__(self, image, screen_size, division=1.0):
		self.image = pygame.image.load(image).convert()
		self.screen_size = screen_size
		self.division = division
		self.rect = self.image.get_rect()
		self._transform()
		self._divide()
		self.new_rect.center = (self.screen_size[0]/2, self.screen_size[1]/2)
		self.dyn_text = []
		self.buttons = {}
		self.button_color = {}

	def _transform(self):
		orig_y = float(self.screen_size[1])
		orig_h = float(self.rect.height)
		multiple = orig_y / orig_h
		new_w = int(self.rect.width * multiple)
		new_h = int(self.rect.height * multiple)
		self.new_image = pygame.transform.smoothscale(self.image, (new_w, new_h))
		self.new_rect = self.new_image.get_rect()


	def _divide(self):
		if self.division != 1.0:
			new_w = int(self.new_rect.w / self.division)
			new_h = int(self.new_rect.h / self.division)
			self.new_image = pygame.transform.smoothscale(self.new_image, (new_w, new_h))
			self.new_rect = self.new_image.get_rect()

	def make_button(self, name, size, placement, text, images=None):
		if images == None:
			adj_place = self._adjust_placement(placement)
			button_rect = pygame.Rect(adj_place, size)
			self.buttons[name] = button_rect
			self.button_color[name] = (0,0,0)
			txt_place = (placement[0]+5, placement[1]+5)
			self.make_dynamic_text(txt_place, text, txtsize=20)


	def make_dynamic_text(self, placement, text, color=(0,0,0), txtsize=40, font="arial"):
		myfont = pygame.font.SysFont(font, txtsize)
		ad_placement = self._adjust_placement(placement)
		d_text = myfont.render(text, True, color)
		d_place = pygame.Rect(int(ad_placement[0]), int(ad_placement[1]), 5, 5)
		self.dyn_text.append(d_text)
		self.dyn_text.append(d_place)

	def _adjust_placement(self, placement):
		w_multiple = float(self.new_rect.w) / float(self.rect.w)
		h_multiple = float(self.new_rect.h) / float(self.rect.h)
		adj_placement = ((placement[0]*w_multiple),
					(placement[1]*h_multiple))
		return adj_placement

	def button_collision(self, name, point, press=None):
		new_point = (point[0] - self.new_rect.x, point[1] - self.new_rect.y)
		if self.buttons[name].collidepoint(new_point):
			if press == True:
				self.button_color[name] = (255, 0, 0)
				return True
			else:
				self.button_color[name] = (50, 50, 50)
				return False
		elif self.button_color[name] != (0, 0, 0):
			self.button_color[name] = (0, 0, 0)
			return False

	def update(self, x, upd_text=None):
		# Updating Dynamic Text
		if upd_text != None:
			for i in upd_text:
				d_text = self.myfont.render(i, True, (255,0,0))
				self.dyn_text[x] = d_text
				x += 2

	def draw(self, surf, trans):

		# Drawing the Buttons to our surface
		if self.buttons != {}:
			for i in self.buttons.keys():
				pygame.draw.rect(self.new_image, self.button_color[i], self.buttons[i], 3)

		# Drawing Dynamic Text to our surface
		if self.dyn_text != []:
			x = 0
			for i in xrange(len(self.dyn_text)/2):
				self.new_image.blit(self.dyn_text[x], self.dyn_text[x+1])
				x += 2
		tras_setting = (trans * 255)
		self.new_image.set_alpha(tras_setting)
		# Drawing The Background Surface to the screen
		surf.blit(self.new_image, self.new_rect)










