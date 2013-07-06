"""
The Class that handles all Collision
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d

class Collision(object):
	"""Collision"""
	def __init__(self, pos):
		self.old_xy = pos.inttup()

	def collide(self, tiles, pos, rect):
		collide = False
		for tile in tiles:
			if tile.rect.colliderect(rect):
				collide = True
				pos = vec2d(self.old_xy)
				
		if collide == False:
			self.old_xy = pos.inttup()
		return pos

	

