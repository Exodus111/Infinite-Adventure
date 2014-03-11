"""
2.0
Entity class, that iterates to Player and Mob classes
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d
from Collision import Collision
from AI import Behavior

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

class Mob(Entity):
	"""NPC class"""
	def __init__(self, img, pos, dir):
		Entity.__init__(self)
		self.image = pygame.image.load(img).convert_alpha()
		self.image_old = self.image
		self.rect = self.image.get_rect()
		self.pos = vec2d(pos)
		self.dir = vec2d(dir)
		self.old_dir = self.dir
		self.target = self.pos
		self.rect.center = self.pos.inttup()
		self.speed = 5
		self.timer = 0.0
		self.collision = Collision(self)
		self.collided = False
		self.behavior = Behavior(self)

	def update(self, tiles, dt):
		self.dirty = 1
		self.collision.quad_collide(tiles, self)
		self.collide_rect.center = self.rect.center
		self.behavior.update(dt)
		self.collision.collide_other(self)
		self.move()
		self.collided = self.collision.collide(self)
		self._rotate()

	def move(self):
		distance = self.pos.get_distance(self.target)
		if distance > 5:
			self.pos += self.dir
			self.rect.center = self.pos.inttup()

	def move_to(self, target):
		target = vec2d(target)
		if target != self.target:
			self.target = target
			if target != self.pos:
				self.dir = target - self.pos
				self.dir.length = self.speed

	def _rotate(self):
			if self.dir != self.old_dir:
				img_fix = self.image.get_rect()
				image = pygame.transform.rotate(self.image_old, (self.dir.get_angle() * -1))
				img_fix.center = image.get_rect().center
				image = image.subsurface(img_fix).copy()
				self.image = image
				self.old_dir = self.dir


class Player(Entity):
	"""Player Object"""
	def __init__(self, img, pos, direction):
		Entity.__init__(self)
		self.image = pygame.image.load(img).convert_alpha()
		self.image_old = self.image
		self.rect = self.image.get_rect()
		self.pos = vec2d(pos)
		self.dir = vec2d(direction)
		self.rect.center = self.pos.inttup()
		self.speed = 5
		self.timer = 0.0
		self.screen_rect = pygame.Rect(1, 1, 256, 256)
		self.collision = Collision(self)
		self.arrows = [0,0,0,0]
		self.type = "player"
		self.name = "Ragnok The Awesome"
		self.title = "Slayer of Unicorns"
		self.level = 1
		self.old_level = 1

	def update(self, tiles, dt):
			self.dirty = 1
			self.collide_rect.center = self.rect.center
			self.screen_rect.center = self.rect.center
			self.collision.collide_other(self)
			self.collision.quad_collide(tiles, self)
			if self.arrows != [0,0,0,0]:
				self.move()
				self.movement_speed(dt)

	def move(self):
		if self.arrows[0]: #Up
			self.dir.y = -self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()
			self.collision.player_collision(self, "Up")
			self.dir.y = 0
		if self.arrows[1]: #Left
			self.dir.x = -self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()
			self.collision.player_collision(self, "Left")
			self.dir.x = 0
		if self.arrows[2]: #Down
			self.dir.y = self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()
			self.collision.player_collision(self, "Down")
			self.dir.y = 0
		if self.arrows[3]: #Right
			self.dir.x = self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()
			self.collision.player_collision(self, "Right")
			self.dir.x = 0

	def set_timer(self, dt):
		if sum(self.arrows) < 2:
			self.timer = dt

	def movement_speed(self, dt):
		diff = (dt * 25) - (self.timer * 25)
		if diff == 0:
			self.speed = 1
		elif diff >= 7:
			self.speed = 7
		else:
			self.speed = int(diff)

	def rotate_player(self, pos, xy):
		mousevec = vec2d(pos)
		ppos = self.pos.inttup()
		player_vec = vec2d(ppos[0] - (xy[0]*-1), ppos[1] - (xy[1]*-1))
		new_vec = mousevec - player_vec
		img_fix = self.image.get_rect()
		image = pygame.transform.rotate(self.image_old, (new_vec.get_angle())*-1)
		img_fix.center = image.get_rect().center
		image = image.subsurface(img_fix).copy()
		self.image = image



"""
Old or alternative methods that do no work.


	def move_2(self):
		if self.arrows[0]: #Up
			self.movement(self.dir.y, -self.speed, "Up")
		if self.arrows[1]: #Left
			self.movement(self.dir.x, -self.speed, "Left")
		if self.arrows[2]: #Down
			self.movement(self.dir.y, self.speed, "Down")
		if self.arrows[3]: #Right
			self.movement(self.dir.x, self.speed, "Right")

	def movement(self, coord, speed, direction):
		coord = speed
		self.pos += self.dir
		self.rect.center = self.pos.inttup()
		self.collision.player_collision(self, direction)
		coord = 0

	def move_alt(self):
		if self.arrows[0]: #Up
			self.rect.y -= self.speed
			self.collision.player_collision(self, "Up")
		if self.arrows[1]: #Left
			self.rect.x -= self.speed
			self.collision.player_collision(self, "Left")
		if self.arrows[2]: #Down
			self.rect.y += self.speed
			self.collision.player_collision(self, "Down")
		if self.arrows[3]: #Right
			self.rect.x += self.speed
			self.collision.player_collision(self, "Right")

	def move_vec(self):
		if self.arrows != [0,0,0,0]:
			self.dir.length = self.speed
			self.pos += self.dir
			self.rect.center = self.pos.inttup()

"""

