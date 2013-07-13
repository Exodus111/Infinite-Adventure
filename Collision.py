"""
The Class that handles all Collision
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d

class Collision(object):
	"""Collision"""
	def __init__(self, entity):
		self.old_xy = entity.pos.inttup()

	def quad_collide(self, dungeon, entity):
		ep = entity.pos
		for rooms in dungeon:
			if rooms.rect.colliderect(entity.rect):
				if rooms.nw_rect.colliderect(entity.rect):
					ep = self.collide(rooms.nwgroup, entity)
				elif rooms.ne_rect.colliderect(entity.rect):
					ep = self.collide(rooms.negroup, entity)
				elif rooms.sw_rect.colliderect(entity.rect):
					ep = self.collide(rooms.swgroup, entity)
				elif rooms.se_rect.colliderect(entity.rect):
					ep = self.collide(rooms.segroup, entity)
		return ep


	def collide(self, tiles, entity):
		collide = False
		for tile in tiles:
			if tile.rect.colliderect(entity.rect):
				collide = True
				entity.pos = vec2d(self.old_xy)
				
		if collide == False:
			self.old_xy = entity.pos.inttup()
			
		return entity.pos

	

