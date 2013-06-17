"""
This class is intended to be a simple raycasting class for Pygame.
It uses pygame's rect collisions to make the ray collisions easy to handle.
The class requires the starting and ending positions (x,y tupples) of the ray.
"""

import pygame, random, math
from pygame.locals import *
from pygame import vec2d

class Raycasting(object):
	"""A Raycasting object made utilizing Pygame's rect collision function"""
	def __init__(self, pos, target):
		self.pos = vec2d(pos)
		self.target = vec2d(target)

	
	"""
	If the ray collides with any sprite in the group,
	this returns a list of the X,Y coords of the collision point that is the closest to the center of the colliding sprite.
	Returns an empty list if there are no collisions. (What it should probably be used for) 
	"""	
	def collisionany(self, tiles):
		collisions = []
		self.ray = self.target - self.pos
		for tile in tiles:
			centralpoint = vec2d(tile.rect.center)
			hypothenuse = centralpoint - self.pos
			angle = hypothenuse.get_angle_between(self.ray)
			radians = math.radians(angle)
			adjecent = math.cos(radians) * hypothenuse.length
			self.ray.length = adjecent
			point = self.pos + self.ray
			if tile.rect.collidepoint(point):
				collisions.append(point.inttup())

		return collisions


	"""
	A simple range check that returns the length between the starting position
	and the center of the closest Sprite. 
	"""
	def checklength(self, tiles):
		length = 0
		for tile in tiles:
			cp = vec2d(tile.rect.center)
			distance = cp.get_distance(self.pos)
			if length < distance:
				length = distance

		return length

	""" 
	Actual ray casting, and checking every point of the ray for collision. 
	Allows for increments. Also allows for full collision detection or just the closest point.
	Returns a list of the X,Y coords of all the collisions in Full mode, or just the first collision in simple mode.
	(full=False is simple mode.) 
	"""
	def cast(self, tiles, increments=1, full=False):
		ray = self.target - self.pos
		length = int(ray.length)
		ray.length = 1
		dotlist = []
		breakloop = False
		for dot in xrange(length):
			dot = self.pos + ray
			for tile in tiles:
				if tile.rect.collidepoint(dot.inttup()):
					dotlist.append(dot.inttup())
					if full == False:
						breakloop = True
					break
			if breakloop == True:
				break
					
			ray.length += increments

		return dotlist

	# For testing purposes this will give the coordinates to draw the ray.
	def draw_ray(self):
		return self.pos.inttup(), self.target.inttup()
