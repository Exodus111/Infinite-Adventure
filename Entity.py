"""
2.0
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
		self.collide_rect = pygame.Rect(1, 1, 64, 64)

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
		self.screen_rect = pygame.Rect(1, 1, 256, 256)
		self.collision = Collision(self)
		self.arrows = [0,0,0,0]

		self.name = "Ragnok The Awesome"
		self.title = "Slayer of Unicorns"
		self.level = 1
		self.old_level = 1

	def update(self, tiles, dt):
			self.dirty = 1
			if self.arrows != [0,0,0,0]:
				self.move()
				self.movement_speed(dt)
			self.collide_rect.center = self.rect.center
			self.screen_rect.center = self.rect.center
			self.collision.quad_collide(tiles, self)
			
	def move(self):
		if self.arrows[0]: #Up
			self.rect.y -= self.speed
			self.collision.player_collision(self, "Up")
			self.pos = vec2d(self.rect.center)
		if self.arrows[1]: #Left
			self.rect.x -= self.speed
			self.collision.player_collision(self, "Left")
			self.pos = vec2d(self.rect.center)
		if self.arrows[2]: #Down
			self.rect.y += self.speed
			self.collision.player_collision(self, "Down")
			self.pos = vec2d(self.rect.center)
		if self.arrows[3]: #Right
			self.rect.x += self.speed
			self.collision.player_collision(self, "Right")
			self.pos = vec2d(self.rect.center)

	def movement_speed(self, dt):
		speed = 1.0
		timer = 1 + dt
		


	def move_vec(self):
		if self.arrows != [0,0,0,0]:
			self.dir.length = self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()
		
		
		
