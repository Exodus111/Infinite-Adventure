

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
			self.collide(time)
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
		
"""
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
"""

class Bolt(MagicEffect):
	"""A Basic magic bolt"""
	def __init__(self, image, speed, pos, damage):
		MagicEffect.__init__(self)
		self.dirty = 1
		self.image = image
		self.rect = self.image.get_bounding_rect()
		self.pos = vec2d(pos)
		self.dir = vec2d(0,0)
		self.target = vec2d(0,0)
		self.speed = speed
		self.dmg = damage

		self.state = "LOADED"
		self.lvl = 1
		self.aoe_lvl = 0
		self.bounce_lvl = 0
		self.collided_mob = None

		self.bounce_counter = 0
		self.counter = 0.0
		self.discharge_lvl = 0
		self.dot_lvl = 0
		self.knockback_lvl = 0
		self.fear_lvl = 0

	
	def collide(self, dt):
		self.rect.center = self.pos.inttup()
		self.discharge(self.mobs)
		for mob in self.mobs:
			if mob.rect.collidepoint(self.pos.inttup()):
				mob.damage(self.dmg)
				self.bounce(dt, mob)
				self.dot(mob, dt)
				self.knockback(mob)
				self.aoe(self.mobs)
				self.fear(mob, dt)

		for room in self.rooms:
			if self.rect.colliderect(room.rect):
				for wall in room.walls:
					if wall.rect.collidepoint(self.pos.inttup()):
						self.aoe(self.mobs)
						self.bounce(dt, wall)
		
		
	def aoe(self, mobs):
		if self.aoe_lvl > 0:
			aoe_range = self.aoe_lvl * 50
			dmg = self.aoe_lvl + 50
			for mob in mobs:
				if mob.pos - self.pos <= aoe_range:
					mob.hp -= dmg

	def bounce(self, dt, ob):
		if self.bounce_lvl > 0:
			if self.bounce_counter < self.bounce_lvl:
				self.state = "FIRING"
				self.bounce_counter += 1
				self.counter = dt + 0.02
				if ob.ident == "Mob":
					if self.collided_mob != ob:
						self.collided_mob = ob
						self.dir.angle *= -1
				elif ob.ident == "Vertical Wall":
					self.dir.y *= -1
				elif ob.ident == "Horizontal Wall":
					self.dir.x *= -1
				else:
					self.state = "DEAD"
			else:
				if dt > self.counter:
					self.state = "DEAD"
		else:
			if dt > self.counter:
				self.state = "DEAD"
		

	def discharge(self, mobs):
		if self.state == "FIRING":
			if self.discharge_lvl > 0:
				discharge_range = self.discharge_lvl * 5
				dmg = self.discharge_lvl + 5
				for mob in mobs:
					if mob.pos - self.pos <= discharge_range:
						mob.hp -= dmg
	
	def dot(self, mob, dt):
		if self.dot_lvl > 0:
			dot_dmg = (self.dot_lvl, self.dot_lvl + 10)
			dot_timestart = dt
			dot_timestop = dt + self.dot_lvl
			mob.dotted(dot_dmg, dot_timestart, dot_timestop)
	
	def knockback(self, mob):
		if self.knockback_lvl > 0:
			shove = mob.pos - self.pos
			distance = self.knockback_lvl * 32
			shove.length = distance
			mob.pos += shove
			
		
	def fear(self, mob, dt):
		if self.fear_lvl > 0:
			fear_timer = self.fear_lvl + 3
			mob.feared(fear_timer, dt)
		

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

