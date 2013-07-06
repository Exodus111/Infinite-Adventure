"""
This class creates our levels.
"""

import pygame
from pygame.locals import *
from Engine import Tile

class Levelgen(object):
 	"""This class will generate our levels"""
 	def __init__(self, images):
 		self.images = images

 	def test_lvl(self, size, block):
 		x = y = 0
 		num = 1
 		floor = pygame.sprite.LayeredDirty()
 		walls = pygame.sprite.LayeredDirty()
 		for col in xrange(size[1]):
 			for row in xrange(size[0]):
 				if x == 0 or x == (size[0] * block - block ) or y == 0 or y == (size[1] * block - block):
 					row = Tile(self.images[0], (x,y), num)
 					walls.add(row)
 				else:
 					row = Tile(self.images[1], (x,y), num)
 					floor.add(row)
 				num += 1
 				x += block
 			y += block
 			x = 0

 		return floor, walls



 		

 		
 
