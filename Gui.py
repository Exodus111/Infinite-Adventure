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


	def make_button(self, size, placement, text, image=None):
		pass

	def make_dynamic_text(self, placement, text, color, txtsize=40, font="arial"):
		myfont = pygame.font.SysFont(font, txtsize)
		w_multiple = float(self.new_rect.w) / float(self.rect.w)
		h_multiple = float(self.new_rect.h) / float(self.rect.h)
		placement = ((placement[0]*w_multiple) + self.new_rect.x, 
					(placement[1]*h_multiple) + self.new_rect.y)
		d_text = myfont.render(text, True, color)
		d_place = pygame.Rect(int(placement[0]), int(placement[1]), 5, 5)
		self.dyn_text.append(d_text)
		self.dyn_text.append(d_place)

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

	def update(self, upd_text=None, upd_butt=None):
		if upd_text != None:
			x = 0
			for i in upd_text:
				d_text = self.myfont.render(i, True, (255,0,0))
				self.dyn_text[x] = d_text
				x += 2


	def draw(self, surf):
		surf.blit(self.new_image, self.new_rect)
		if self.dyn_text != []:
			x = 0
			for i in xrange(len(self.dyn_text)/2):
				surf.blit(self.dyn_text[x], self.dyn_text[x+1])
				x += 2




		




