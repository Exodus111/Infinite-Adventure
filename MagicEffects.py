

import pygame, random, math
from pygame.locals import *
from vec2d import vec2d
from Powers import *

class MagicEffect(pygame.sprite.DirtySprite):
	"""Magical effects as they are seen on the screen"""
	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)
		self.dirty = 1
		self.var = 0
	

	def set_collision(self, rooms, mobs):
		
		self.rooms = rooms
		self.mobs = mobs

	def update(self, time):

		if self.state == "LOADED":
			self.dirty = 0
		elif self.state == "CONE":
			self.dirty = 1
		elif self.state == "FIRING":
			self.dirty = 1
			self.move()
			self.collide()
		elif self.state == "DEAD":
			self.kill()
			self.state = "LOADED"
		elif self.state == "EXPLODING":
			if self.var != 0:
				self.state = "DEAD"
			else:
				self.var += 1

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
		self.damage = damage
		self.state = "LOADED"
		

	def collide(self):
		for room in self.rooms:
			if self.rect.colliderect(room.rect):
				for wall in room.walls:
					if self.rect.colliderect(wall.rect):
						self.aoe()
						
		for mob in self.mobs:
			if self.rect.colliderect(mob):
				mob.damage(self.damage)
				self.aoe()
				

	def aoe(self):
		self.radius = 250
		self.state = "EXPLODING"
		for mob in self.mobs:
			if pygame.sprite.collide_circle(self, mob):
				mob.damage(self.damage)

		

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
		self.angle = 20
		self.dot = 0.0
		

	def fire(self, p_pos, target, time):
		self.timer = time
		self.pos = vec2d(p_pos)
		self.target = vec2d(target)
		self.vector = self.pos - self.target
		self.vector.angle += 90
		self.vector.length = self.vector.length/20
		self.vector1 = self.pos - self.vector
		self.vector2 = self.pos + self.vector
		self.vector.length = self.vector.length*6
		self.vector3 = self.target + self.vector
		self.vector4 = self.target - self.vector
		self.vectorlist = [self.vector1, self.vector2, self.vector3, self.vector4]
		self.state = "CONE"
		self.collide()

		
	def collide(self):
		for mob in self.mobs:
			mobvec = self.pos - mob.pos
			if mobvec.length < self.vector.length:
				self.vector = self.vector.normalized()
				mobvec = mobvec.normalized()
				theDot = self.vector.dot(mobvec)
				angle = math.radians(self.angle)
				if angle > math.acos(theDot):
					self.damage_dot(mob)

	def damage_dot(self, mob):
		if self.dot < self.timer:
			mob.damage(self.damage)
			self.dot = self.timer + 0.5




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

	def fire(self, p_pos, target):
		self.pos = vec2d(p_pos)
		self.rect.center = self.pos.inttup()
		self.aoe()
		
	def aoe(self):
		self.dirty = 1
		self.radius = 300
		self.state = "EXPLODING"
		for mob in self.mobs:
			if pygame.sprite.collide_circle(self, mob):
				mob.damage(self.damage)


		


		
		
