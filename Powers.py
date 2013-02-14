"""
This file contains the powers and abilities of the player, and the mobs.
"""

import pygame, random

from pygame.locals import *
from vec2d import vec2d
from Mainloop import *
from MagicEffects import *


class Powers(object):
	def __init__(self, p_lvl, p_pos):
		self.p_lvl = p_lvl
		self.p_pos = p_pos
		self.base_dmg = (10, 50)
		
		

	def magic_missile(self):
		self.dmg = (self.base_dmg[0] + (self.base_dmg[0] * self.p_lvl * 0.2), 
					self.base_dmg[1] + (self.base_dmg[1] * self.p_lvl * 0.2))
		self.speed = self.p_lvl + 4
		self.name = "Magic Missile"
		self.image1 = pygame.image.load("Magic_Bolt.png").convert_alpha()
		self.descript = "A magic bolt that shoots out of the casters hands and does between %s and %d damage" % (self.dmg[0], self.dmg[1])
		self.cast = "Magic Missile"
		self.bolt = Bolt(self.image1, self.speed, self.p_pos, self.dmg)
		

	def fire_ball(self):
		self.dmg = (self.base_dmg[0] + (self.base_dmg[0] * self.p_lvl * 0.2) *2, 
					self.base_dmg[1] + (self.base_dmg[1] * self.p_lvl * 0.2) *5)
		self.speed = 2 + (self.p_lvl * 0.2)
		self.name = "Fire Ball"
		self.image1 = pygame.image.load("Magic_Bolt.png").convert_alpha()
		self.descript = "A ball of fire that does between %s and %d damage in a large area" % (self.dmg[0], self.dmg[1])
		self.cast = "Fire Ball"

		self.ball = Ball(self.image1, self.speed, self.p_pos, self.dmg)

	def set_collision(self, room, mobs):
		self.bolt.set_collision(room, mobs)




	

