"""
Entity class, that iterates to Player and Mob classes
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d
from Collision import Collision

class Entity(pygame.sprite.DirtySprite):
	"""Entity parent class for Player and Mobs"""
	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)
		self.dirty = 1

	def update(self, dt):
		pass

	def move(self):
		pass


class Player(Entity):
	"""Player Object"""
	def __init__(self, img, pos, direction):
		Entity.__init__(self)
		self.image = pygame.image.load(img).convert_alpha()
		self.rect = self.image.get_rect()
		self.pos = vec2d(pos)
		self.dir = vec2d(direction)
		self.speed = 5
		self.collision = Collision(self.pos)
		self.arrows = [0,0,0,0]

	def update(self, tiles, dt):
			self.dirty = 1
			self.move()
			self.rect.center = self.pos.inttup()
			self.pos = self.collision.collide(tiles, self.pos, self.rect)
			self.rect.center = self.pos.inttup()

	def move(self):
		if self.arrows[0] == 1: #up
			self.dir[1] = -5
		
		if self.arrows[1] == 1: #left
			self.dir[0] = -5
		
		if self.arrows[2] == 1: #down
			self.dir[1] = 5
		
		if self.arrows[3] == 1: #right
			self.dir[0] = 5
		

		if self.arrows != [0,0,0,0]:
			self.dir.length = self.speed
			self.pos += self.dir

		
		
		
