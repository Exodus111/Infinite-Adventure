"""
Mobtest, I need to test out the possibilites and functions of vec2d, hence this file
"""
import pygame, random, math
from vec2d import vec2d
from pygame.locals import *

class Main(object):
 	"""Main class"""
 	def __init__(self):
 		self.clock = pygame.time.Clock()
 		self.size = (1240, 960)
 		self.screen = pygame.display.set_mode(self.size)
 		self.counter = 0
 		self.surface = pygame.Surface(self.size)
 		self.base_surf = pygame.Surface(self.size)
 		self.base_surf.fill((0,0,0))
 		self.mobs = self.make_mobs()
 		pygame.time.set_timer(USEREVENT+1, 10000)
 		

 	def make_mobs(self):
 		mobs = pygame.sprite.LayeredDirty()
 		for i in xrange(50):
 			a = Mob((random.randint(0, self.size[0]), random.randint(0, self.size[1])), 
 					(random.choice([-1, 1]), random.choice([-1, 1])), self.surface)
 			a.num = i
 			a.size = self.size
 			a.time = 60
 			a.rotate_img()
 			mobs.add(a)

 		return mobs

 	def collide_other(self):
 		for mob in self.mobs:
 			for mob2 in self.mobs:
 				if mob != mob2:
					dist = mob.pos.get_distance(mob2.pos)
					if dist < 32:
						overlap = 32 - dist
						shove = mob2.pos - mob.pos
						shove.length = overlap/2
						mob2.pos += shove
						mob.pos -= shove



 	def mainloop(self):
 		
 		while True:
 			self.events()
 			self.update()
 			self.draw()
 			pygame.display.flip()
 			self.clock.tick(60)

 	def events(self):
 		for event in pygame.event.get():
 			if event.type == QUIT:
 				self.exit()
 			if event.type == USEREVENT+1:
 				print "Printer"

 	def update(self):
 		self.collide_other()
 		


 	def draw(self):
 		pygame.display.update()
 		self.mobs.update()
 		self.mobs.draw(self.surface)
 		self.screen.blit(self.surface, (0,0))
 		self.surface.fill((0,0,0))


 	def exit(self):
 		pygame.quit()


class Mob(pygame.sprite.DirtySprite):
	"""docstring for mob"""
	def __init__(self, init_pos, init_dir, bg):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.image.load("mob_white.png").convert_alpha()
		self.base_image = self.image
		self.rect = pygame.Rect(0, 0, 10, 10)
		self.dirty = 1
		self.pos = vec2d(init_pos)
		self.dir = vec2d(init_dir).normalized()
		self.num = 0
		self.counter = 0
		self.size = (0,0)
		self.time = 0
		self.speed = 0.05
		self.health = 15
		self.bg = bg
		self.rotate_img()



	def update(self):
		self.dirty = 1
		move = vec2d(self.dir.x * self.speed * 60, self.dir.y * self.speed * 60)
		self.pos += move
		self.rect.centerx, self.rect.centery = self.pos.inttup()
		health_bar_x = self.pos.x - 7
		health_bar_y = self.pos.y - 7
		self.bg.fill(pygame.Color("red"), (health_bar_x, health_bar_y, 30, 4))
		self.bg.fill(pygame.Color("green"), (health_bar_x, health_bar_y, self.health, 4))
		self.collide()
		self.rotate()
		



	def collide(self):
		if self.pos.x >= self.size[0]:
			self.dir.x *= -1
			self.rotate_img()
		if self.pos.x <= 0:
			self.dir.x *= -1
			self.rotate_img()
		if self.pos.y >= self.size[1]:
			self.dir.y *= -1
			self.rotate_img()
		if self.pos.y <= 0:
			self.dir.y *= -1
			self.rotate_img()


	def rotate(self):
		self.counter += 5
 		if self.counter > random.randint(600, 1000):
	 		self.dir.rotate(45 * random.randint(-1, 1))
			self.counter = 0
			self.rotate_img()


	def rotate_img(self):
		angle = self.dir.angle
		self.image = pygame.transform.rotate(self.base_image, -angle)

		
start = Main()
start.mainloop()
