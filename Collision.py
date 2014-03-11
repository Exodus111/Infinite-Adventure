"""
2.0
The Class that handles all Collision
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d

class Collision(object):
	"""Collision"""
	moblist = []
	def __init__(self, entity):
		self.old_xy = entity.pos.inttup()
		self.current_quad = pygame.sprite.LayeredDirty()
		self.current_floor = None
		self.dungeon = None
		self.doonce = True

	def quad_collide(self, dungeon, entity):
		if self.doonce:
			self.dungeon = dungeon
			self.doonce = False
		if len(self.current_quad) > 100:
			self.current_quad.empty()
		for room in dungeon:
			if room.rect.colliderect(entity.rect):
				self.current_floor = room
				if room.rect.colliderect(entity.collide_rect):
					if room.nw_rect.colliderect(entity.collide_rect):
						if room.nwgroup not in self.current_quad:
							self.current_quad.add(room.nwgroup)
					if room.ne_rect.colliderect(entity.collide_rect):
						if room.negroup not in self.current_quad:
							self.current_quad.add(room.negroup)
					if room.sw_rect.colliderect(entity.collide_rect):
						if room.swgroup not in self.current_quad:
							self.current_quad.add(room.swgroup)
					if room.se_rect.colliderect(entity.collide_rect):
						if room.segroup not in self.current_quad:
							self.current_quad.add(room.segroup)

	def collide_other(self, entity):
		for mob in self.moblist:
			dist = entity.pos.get_distance(mob.pos)
			if dist < 20:
				direction = mob.pos - entity.pos
				mob.pos += direction
				entity.pos -= direction


	def collide(self, entity):
		collide = False
		for tile in self.current_quad:
			if tile.rect.colliderect(entity.rect):
				collide = True
				entity.pos = vec2d(self.old_xy)
				entity.rect.center = entity.pos.inttup()
		self.old_xy = entity.pos.inttup()
		return collide

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

"""
Old methods.

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
"""
