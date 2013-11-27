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
		self.current_quad = pygame.sprite.LayeredDirty()
		self.current_floor = None

	def quad_collide(self, dungeon, entity):
		if len(self.current_quad) > 100:
			self.current_quad.empty()
		for rooms in dungeon:
			if rooms.rect.colliderect(entity.rect):
				self.current_floor = rooms.rect
			if rooms.rect.colliderect(entity.collide_rect):
				if rooms.nw_rect.colliderect(entity.collide_rect):
					self.current_quad.add(rooms.nwgroup)
				if rooms.ne_rect.colliderect(entity.collide_rect):
					self.current_quad.add(rooms.negroup)
				if rooms.sw_rect.colliderect(entity.collide_rect):
					self.current_quad.add(rooms.swgroup)
				if rooms.se_rect.colliderect(entity.collide_rect):
					self.current_quad.add(rooms.segroup)

	def collide(self, tiles, entity):
		collide = False
		for tile in tiles:
			if tile.rect.colliderect(entity.rect):
				collide = True
				entity.pos = vec2d(self.old_xy)
				
		if collide == False:
			self.old_xy = entity.pos.inttup()
			
		return entity.pos

	def player_collision(self, entity, direction):
		if self.current_quad != None:
			if direction == "Up":
				for tile in self.current_quad:
					if entity.rect.colliderect(tile):
						entity.rect.top = tile.rect.bottom
						entity.pos = vec2d(entity.rect.center)
			elif direction == "Left":
				for tile in self.current_quad:
					if entity.rect.colliderect(tile):
						entity.rect.left = tile.rect.right
						entity.pos = vec2d(entity.rect.center)
			elif direction == "Down":
				for tile in self.current_quad:
					if entity.rect.colliderect(tile):
						entity.rect.bottom = tile.rect.top
						entity.pos = vec2d(entity.rect.center)
			elif direction == "Right":
				for tile in self.current_quad:
					if entity.rect.colliderect(tile):
						entity.rect.right = tile.rect.left
						entity.pos = vec2d(entity.rect.center)

	def player_collision_old(self, entity, direction):
		if self.current_quad != None:
			for tile in self.current_quad:
				if entity.rect.colliderect(tile):
					self.keep_in_room(entity)
					entity.pos = vec2d(entity.rect.center) 

	def keep_in_room(self, entity):
		if entity.rect.right + 32 > self.current_floor.right:
			entity.rect.right = self.current_floor.right - 32 
		if entity.rect.left < self.current_floor.left:
			entity.rect.left = self.current_floor.left
		if entity.rect.top < self.current_floor.top:
			entity.rect.top = self.current_floor.top
		if entity.rect.bottom + 32 > self.current_floor.bottom:
			entity.rect.bottom = self.current_floor.bottom - 32
 

	

