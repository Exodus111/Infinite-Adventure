"""
The GUI file.
Contains both the graphical, and code logic for the gui.
"""

import pygame, random
from pygame.locals import *

class GUI(object):
	"""docstring for GUI"""
	def __init__(self, screen_size, player):
		self.screen_size = screen_size
		self.player_level = player.level
		self.max_hp = player.hp
		self.max_mana = player.mana
		self.button_one = 1
		self.unit = (int(screen_size[0] * 0.2))
		self.top = (int(screen_size[0] * 0.05), int(screen_size[1] * 0.05))
		self.bottom = (int(screen_size[0] * 0.1), int(screen_size[1] * 0.9))
		self.bottom_row = [self.bottom, (self.bottom[0] + self.unit, self.bottom[1]), 
										(self.bottom[0] + self.unit*2, self.bottom[1]), 
										(self.bottom[0] + self.unit*3, self.bottom[1]), 
										(self.bottom[0] + self.unit*4, self.bottom[1]),
										(self.bottom[0] + self.unit*5, self.bottom[1])]
		self.healthbar = pygame.Rect(self.top[0]+30, self.top[1]-20, self.unit, 15)
		self.redbar = pygame.Rect(self.top[0]+30, self.top[1]-20, self.unit, 15)
		self.manabar = pygame.Rect(self.top[0]+30, self.top[1], self.unit, 15)
		self.greybar = pygame.Rect(self.top[0]+30, self.top[1], self.unit, 15)
		self.images()
		self.text()

	def images(self):
		self.m_missile_image = pygame.image.load("Magic_Bolt.png").convert_alpha()
		self.f_ball_image = pygame.image.load("Fire_Ball.png").convert_alpha()
		self.c_frost_image = pygame.image.load("Fire_Ball.png").convert_alpha()
		self.r_fire_image = pygame.image.load("Fire_Ball.png").convert_alpha()
		self.incomp_image = pygame.image.load("Fire_Ball.png").convert_alpha()

	def text(self):
		my_font = pygame.font.SysFont("arial", 20)
		self.player_lvl = my_font.render(str(self.player_level), True, (255, 255, 255))
		self.player_health_pos = pygame.Rect(0, 0, 10, 10)
		self.player_health_pos.center = self.top
		self.player_health_pos.y -= 8

		self.msg1 = my_font.render("Magic Missile", True, (255, 255, 255))
		self.msg1_rect = pygame.Rect(self.bottom_row[0][0]-60, self.bottom_row[0][1]+60, 50, 10)
		self.button_1 = my_font.render("Button 1", True, (255, 255, 255))
		self.button_1_rect = pygame.Rect(self.bottom_row[0][0]-60, self.bottom_row[0][1]+40, 50, 10)

		self.msg2 = my_font.render("Fire Ball", True, (255, 255, 255))
		self.msg2_rect = pygame.Rect(self.bottom_row[1][0]-60, self.bottom_row[1][1]+60, 50, 10)
		self.button_2 = my_font.render("Button 2", True, (255, 255, 255))
		self.button_2_rect = pygame.Rect(self.bottom_row[1][0]-60, self.bottom_row[1][1]+40, 50, 10)
		
		self.msg3 = my_font.render("Cone of Frost", True, (255, 255, 255))
		self.msg3_rect = pygame.Rect(self.bottom_row[2][0]-60, self.bottom_row[2][1]+60, 50, 10)
		self.button_3 = my_font.render("Button 3", True, (255, 255, 255))
		self.button_3_rect = pygame.Rect(self.bottom_row[2][0]-60, self.bottom_row[2][1]+40, 50, 10)
		
		self.msg4 = my_font.render("Ring of Fire", True, (255, 255, 255))
		self.msg4_rect = pygame.Rect(self.bottom_row[3][0]-60, self.bottom_row[3][1]+60, 50, 10)
		self.button_4 = my_font.render("Button 4", True, (255, 255, 255))
		self.button_4_rect = pygame.Rect(self.bottom_row[3][0]-60, self.bottom_row[3][1]+40, 50, 10)
		
		self.msg5 = my_font.render("Incomporable", True, (255, 255, 255))
		self.msg5_rect = pygame.Rect(self.bottom_row[4][0]-60, self.bottom_row[4][1]+60, 50, 10)
		self.button_5 = my_font.render("Button 5", True, (255, 255, 255))
		self.button_5_rect = pygame.Rect(self.bottom_row[4][0]-60, self.bottom_row[4][1]+40, 50, 10)
		





	def update(self, player):
		self.hp = player.hp
		self.mana = player.mana
		if self.max_hp != self.hp:
			bar_diff = ((self.unit / self.max_hp) * self.hp)
			self.healthbar.width = bar_diff
		if self.max_mana != self.mana:
			bar_diff = ((self.unit / self.max_mana) * self.mana)
			self.manabar.width = bar_diff
		else:
			self.manabar.width = self.unit    
		


	def draw(self, surf):
		# Making the bottom row:
		# First power
		pygame.draw.circle(surf, (10, 10, 10), (self.bottom_row[0]), 30,)
		pygame.draw.circle(surf, (255, 100, 0), (self.bottom_row[0]), 30, 4)
		surf.blit(self.m_missile_image, (self.bottom_row[0][0]-15, self.bottom_row[0][1]-15))
		surf.blit(self.msg1, self.msg1_rect)
		surf.blit(self.button_1, self.button_1_rect)

		# Second Power
		pygame.draw.circle(surf, (10, 10, 10), (self.bottom_row[1]), 30,)
		pygame.draw.circle(surf, (255, 100, 0), (self.bottom_row[1]), 30, 4)
		surf.blit(self.f_ball_image, (self.bottom_row[1][0]-15, self.bottom_row[1][1]-15))
		surf.blit(self.msg2, self.msg2_rect)
		surf.blit(self.button_2, self.button_2_rect)

		# Third Power
		pygame.draw.circle(surf, (10, 10, 10), (self.bottom_row[2]), 30,)
		pygame.draw.circle(surf, (255, 100, 0), (self.bottom_row[2]), 30, 4)
		surf.blit(self.c_frost_image, (self.bottom_row[2][0]-15, self.bottom_row[2][1]-15))
		surf.blit(self.msg3, self.msg3_rect)
		surf.blit(self.button_3, self.button_3_rect)

		# Fourth Power
		pygame.draw.circle(surf, (10, 10, 10), (self.bottom_row[3]), 30,)
		pygame.draw.circle(surf, (255, 100, 0), (self.bottom_row[3]), 30, 4)
		surf.blit(self.r_fire_image, (self.bottom_row[3][0]-15, self.bottom_row[3][1]-15))
		surf.blit(self.msg4, self.msg4_rect)
		surf.blit(self.button_4, self.button_4_rect)

		# Fifth Power
		pygame.draw.circle(surf, (10, 10, 10), (self.bottom_row[4]), 30,)
		pygame.draw.circle(surf, (255, 100, 0), (self.bottom_row[4]), 30, 4)
		surf.blit(self.incomp_image, (self.bottom_row[4][0]-15, self.bottom_row[4][1]-15))
		surf.blit(self.msg5, self.msg5_rect)
		surf.blit(self.button_5, self.button_5_rect)

		# Making the top row:
		pygame.draw.circle(surf, (10, 10, 10), (self.top), 20, )
		pygame.draw.circle(surf, (255, 0, 0), (self.top), 20, 1)
		pygame.draw.rect(surf, pygame.Color("red"), self.redbar)
		pygame.draw.rect(surf, pygame.Color("green"), self.healthbar)
		pygame.draw.rect(surf, pygame.Color("grey"), self.greybar)
		pygame.draw.rect(surf, pygame.Color("blue"), self.manabar)
		surf.blit(self.player_lvl, self.player_health_pos)

	def button_one(self, p_pos, target):
			if self.button_one == 1:
				pass

	def select_power(self):
		pass

