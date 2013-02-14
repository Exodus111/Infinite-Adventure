

import pygame, random
from pygame.locals import *
from vec2d import vec2d
from Powers import *

class MagicEffect(pygame.sprite.DirtySprite):
	"""Magical effects as they are seen on the screen"""
	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)
		self.dirty = 1

	def set_collision(self, rooms, mobs):
		
		self.rooms = rooms
		self.mobs = mobs

	def update(self):
		if self.state == "LOADED":
			self.dirty = 0
		elif self.state == "FIRING":
			self.dirty = 1
			self.move()
			self.collide()
		elif self.state == "DEAD":
			self.kill()
			self.state = "LOADED"

	def fire(self, p_pos, target):
		self.pos = vec2d(p_pos)
		self.target = vec2d(target)
		self.dir = self.target - self.pos
		self.state = "FIRING"

	def move(self):
		if self.dir.length > self.speed:
			self.dir.length = self.speed
		self.pos += self.dir
		self.rect.center = self.pos.inttup()
		

	def collide(self):
		for room in self.rooms:
			if self.rect.colliderect(room.rect):
				for wall in room.walls:
					if self.rect.colliderect(wall.rect):
						self.state = "DEAD"
		for mob in self.mobs:
			if self.rect.colliderect(mob):
				mob.damage(self.damage)
				self.state = "DEAD"

class Bolt(MagicEffect):
	"""A Basic magic bolt"""
	def __init__(self, image, speed, pos, damage):
		MagicEffect.__init__(self)
		self.dirty = 1
		self.image = image
		self.rect = self.image.get_bounding_rect()
		self.pos = vec2d(pos)
		self.target = vec2d(0,0)
		self.speed = speed
		self.damage = damage
		self.state = "LOADED"

class Ball(MagicEffect):
	def __init__(self, image, speed, pos, damage):
		MagicEffect.__init__(self)
		self.dirty = 1
		self.image = image
		self.rect = self.image.get_bounding_rect()
		self.pos = vec2d(pos)
		self.target = vec2d(0,0)
		self.speed = speed
		seld.damage = damage
		self.state = "LOADED"

class Cone(MagicEffect):
	"""A Magical cone effect"""
	def __init__(self, image, speed, pos, damage):
		MagicEffect.__init__(self)
		self.image = image
		self.dirty = 1
		self.rect = self.image.get_bounding_rect()
		self.speed = speed
		self.pos = vec2d(pos)
		self.target = vec2d(0,0)
		self.damage = damage
		self.state = "LOADED"

class Ring(MagicEffect):
	"""Aoe effect"""
	def __init__(self, image, speed, pos, damage):
		MagicEffect.__init__(self)
		self.dirty = 1
		self.image = image
		self.rect = self.image.get_bounding_rect()
		self.speed = speed
		self.pos = vec2d(pos)
		self.target = vec2d(0,0)
		self.damage = damage
		self.state = "LOADED"
		


		


		
		
