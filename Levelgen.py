"""
This class creates our levels.
"""

import pygame, random
from pygame.locals import *
from Engine import Tile

class Levelgen(object):
 	"""This class will generate our levels"""
 	def __init__(self, images):
 		self.images = images
 		self.myrandom = random.Random()
 		self.myrandom.seed(54321)

 	def make_dungeon(self, start, surf_size, minmax_row, block, ch_corr):
 		self.start = start
 		self.max_size = minmax_row[1] * block
 		self.minmax_row = minmax_row
 		self.mydungeon = []
 		making = True
 		while making == True:
 			print "making room"
 			room_size = (self.myrandom.randrange(self.minmax_row[0], self.minmax_row[1]), 
 						self.myrandom.randrange(self.minmax_row[0], self.minmax_row[1]))
 			room = self.make_room(self.start, room_size, block)
 			self.mydungeon.append(room)
 			self.direction = [0, 1, 2, 3]
 			direction = self.pick_direction(surf_size, room)
 			if direction != None:
 				self.pick_room(ch_corr)	
 			else:
 				print "Ended"
 				making = False

 		return self.mydungeon

 	def pick_direction(self, size, room):
 		checking = True
 		while checking == True:
 			direction = None
 			if self.direction != []:
	 			direction = self.myrandom.choice(self.direction)
	 			print direction

	 			if direction == 0: # Right
		 			dist = (self.start[0] + (self.max_size*2), self.start[1])
		 			pos = (self.start[0] + self.max_size, self.start[1])
		 			check_dist = self.check_distance(dist, size)
		 			check_col = self.check_collision(pos)
		 			if check_dist == False and check_col == False:
		 				self.direction.remove(0)
		 			else:
		 				self.start = pos
		 				checking = False
		 		elif direction == 1: # Left
		 			dist = (self.start[0] - (self.max_size), self.start[1])
		 			pos = (self.start[0] - self.max_size, self.start[1])
		 			check_dist = self.check_distance(dist, size)
		 			check_col = self.check_collision(pos)
		 			if check_dist == False and check_col == False:
		 				self.direction.remove(1)
		 			else:
		 				self.start = pos
		 				checking = False
		 		elif direction == 2: # Up
		 			dist = (self.start[0], self.start[1] - (self.max_size))
		 			pos = (self.start[0], self.start[1] - self.max_size)
		 			check_dist = self.check_distance(dist, size)
		 			check_col = self.check_collision(pos)
		 			if check_dist == False and check_col == False:
		 				self.direction.remove(2)
		 			else:
		 				self.start = pos
		 				checking = False
		 		elif direction == 3: # Down
		 			dist = (self.start[0], self.start[1] + (self.max_size*2))
		 			pos = (self.start[0], self.start[1] + self.max_size)
		 			check_dist = self.check_distance(dist, size)
		 			check_col = self.check_collision(pos)
		 			if check_dist == False and check_col == False:
		 				self.direction.remove(3)
		 			else:
		 				self.start = pos
		 				checking = False
		 	else:
		 		checking = False

 		return direction

 	def check_distance(self, dist, size):
 		check = False
 		if dist[0] < size[0] and dist[0] > 0 and dist[1] < size[1] and dist[1] > 0:
 			check = True
 		else:
 			check = False

 		return check

 	def check_collision(self, pos):
 		check = True
 		max_rect = pygame.Rect(pos[0], pos[1], self.max_size, self.max_size)
 		for room in self.mydungeon:
 			if room.rect.colliderect(max_rect):
 				check = False

 		return check

 	def pick_room(self, ch_corr):
 		pass


 	def make_room(self, start, size, block):
 		self.room1 = Room(start, size, block, self.images)

 		return self.room1

class Room(object):
	"""The Room class"""
	def __init__(self, start, size, block, images):
		self.start = start
		self.size = size
		self.block = block
		self.images = images
		self._generate()
		self.rect = pygame.Rect(self.start[0], self.start[1], size[0]*block, size[1]*block)
		self.nw_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w/2, self.rect.h/2)
		self.nwgroup = self._quad_tree(self.nw_rect)
		self.ne_rect = pygame.Rect(self.rect.x + (self.rect.w/2), self.rect.y, self.rect.w/2, self.rect.h/2)
		self.negroup = self._quad_tree(self.ne_rect)
		self.sw_rect = pygame.Rect(self.rect.x, self.rect.y + (self.rect.h/2), self.rect.w/2, self.rect.h/2)
		self.swgroup = self._quad_tree(self.sw_rect)
		self.se_rect = pygame.Rect(self.rect.x + (self.rect.w/2), self.rect.y + (self.rect.h/2), self.rect.w/2, self.rect.h/2)
		self.segroup = self._quad_tree(self.se_rect)

	def _generate(self):
		x = self.start[0]
 		y = self.start[1]
 		num = 1
 		self.floor = pygame.sprite.LayeredDirty()
 		self.walls = pygame.sprite.LayeredDirty()
 		for col in xrange(self.size[1]):
 			for row in xrange(self.size[0]):
 				if x == self.start[0] or x == (self.start[0] + self.size[0] * self.block - self.block ) or y == self.start[1] or y == (self.start[1] + self.size[1] * self.block - self.block):
 					row = Tile(self.images[0], (x,y), num)
 					self.walls.add(row)
 				else:
 					row = Tile(self.images[1], (x,y), num)
 					self.floor.add(row)
 				num += 1
 				x += self.block
 			y += self.block
 			x = self.start[0]

 	def _quad_tree(self, quad):
 		quad_group = pygame.sprite.LayeredDirty()
 		for tile in self.walls:
 			if quad.colliderect(tile):
 				quad_group.add(tile)

 		return quad_group

		



 		

 		
 
