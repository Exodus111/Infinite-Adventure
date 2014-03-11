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
		if "png" in image:
			self.image = pygame.image.load(image).convert_alpha()
		else:
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
		self.spritegroup = pygame.sprite.LayeredDirty()

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

	def make_sprite(self, placement, images):
		pos = _adjust_placement(placement)
		sprite = Sprite(images, pos)
		self.spritegroup.add(sprite)

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
				self.button_color[name] = (150, 150, 150)
				return True
		elif self.button_color[name] != (0, 0, 0):
			self.button_color[name] = (0, 0, 0)
			return False

	def sprite_collision(self, point, press=None):
		collided = self.spritegroup.get_sprite_at(point)
		if collided != []:
			sprite = collided[0]
			if press != None:
				sprite.update(1)
			else:
				sprite.update(2)
		else:
			self.spritegroup.update(0)


	def update(self, x, upd_text=None):
		# Updating Dynamic Text
		if upd_text != None:
			for i in upd_text:
				d_text = self.myfont.render(i, True, (255,0,0))
				self.dyn_text[x] = d_text
				x += 2

	def draw(self, surf, trans=1):

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
		# Drawing the sprites to our surface
		if self.spritegroup.sprites() != []:
			self.spritegroup.draw(surf)
		# Setting Transparancy of the surface
		tras_setting = (trans * 255)
		self.new_image.set_alpha(tras_setting)
		# Drawing The Background Surface to the screen
		surf.blit(self.new_image, self.new_rect)


class MouseOver(object):
	def __init__(self, image):
		self.pointer = Pointer(image)
		self.rect = None
		self.my_font = pygame.font.SysFont("arial", 15)
		self.targets = {}
		self.state = 0
		self.pos = (0,0)
		self.txt_color = (255, 255, 0)

	def update(self, pos):
		self.pointer.update(pos)
		self.pos = (pos[0] + 10, pos[1] + 20)

	def draw(self, surf):
		self.pointer.draw(surf)
		if self.state == 0:
			pass
		elif self.state == 1:
			surf.blit(self.window, self.pos)

	def setup_text(self, txt):
		width = 0
		message = []
		for line in txt:
			if len(line) > width:
				width = len(line)
			the_line = self.my_font.render(line, True, self.txt_color)
			message.append(the_line)
		size = (width*7, len(txt)*20)
		self.window = pygame.Surface((size))
		rect = pygame.Rect(5, 0, 5, 5)
		x = 0
		for msg in message:
			self.window.blit(message[x], rect)
			rect.y += 20
			x += 1
		self.rect = self.window.get_rect()
		pygame.draw.rect(self.window, self.txt_color, self.rect, 1)

class Pointer(pygame.sprite.DirtySprite):
	def __init__(self, image):
		self.image = pygame.image.load(image).convert_alpha()
		self.rect = self.image.get_rect()
		self.dirty = 2

	def update(self, pos):
		self.rect.center = pos

	def draw(self, surf):
		surf.blit(self.image, self.rect)












