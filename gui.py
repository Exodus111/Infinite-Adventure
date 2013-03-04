"""
The GUI file.
Contains both the graphical, and code logic for the gui.
"""

import pygame, random
from pygame.locals import *
from vec2d import vec2d

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
		self.my_font = pygame.font.SysFont("arial", 20)
		self.player_lvl = self.my_font.render(str(self.player_level), True, (255, 255, 255))
		self.player_health_pos = pygame.Rect(0, 0, 10, 10)
		self.player_health_pos.center = self.top
		self.player_health_pos.y -= 8

		self.msg1 = self.my_font.render("Magic Missile", True, (255, 255, 255))
		self.msg1_rect = pygame.Rect(self.bottom_row[0][0]-60, self.bottom_row[0][1]+60, 50, 10)
		self.button_1 = self.my_font.render("Button 1", True, (255, 255, 255))
		self.button_1_rect = pygame.Rect(self.bottom_row[0][0]-60, self.bottom_row[0][1]+40, 50, 10)

		self.msg2 = self.my_font.render("Fire Ball", True, (255, 255, 255))
		self.msg2_rect = pygame.Rect(self.bottom_row[1][0]-60, self.bottom_row[1][1]+60, 50, 10)
		self.button_2 = self.my_font.render("Button 2", True, (255, 255, 255))
		self.button_2_rect = pygame.Rect(self.bottom_row[1][0]-60, self.bottom_row[1][1]+40, 50, 10)
		
		self.msg3 = self.my_font.render("Cone of Frost", True, (255, 255, 255))
		self.msg3_rect = pygame.Rect(self.bottom_row[2][0]-60, self.bottom_row[2][1]+60, 50, 10)
		self.button_3 = self.my_font.render("Button 3", True, (255, 255, 255))
		self.button_3_rect = pygame.Rect(self.bottom_row[2][0]-60, self.bottom_row[2][1]+40, 50, 10)
		
		self.msg4 = self.my_font.render("Ring of Fire", True, (255, 255, 255))
		self.msg4_rect = pygame.Rect(self.bottom_row[3][0]-60, self.bottom_row[3][1]+60, 50, 10)
		self.button_4 = self.my_font.render("Button 4", True, (255, 255, 255))
		self.button_4_rect = pygame.Rect(self.bottom_row[3][0]-60, self.bottom_row[3][1]+40, 50, 10)
		
		self.msg5 = self.my_font.render("Incomporable", True, (255, 255, 255))
		self.msg5_rect = pygame.Rect(self.bottom_row[4][0]-60, self.bottom_row[4][1]+60, 50, 10)
		self.button_5 = self.my_font.render("Button 5", True, (255, 255, 255))
		self.button_5_rect = pygame.Rect(self.bottom_row[4][0]-60, self.bottom_row[4][1]+40, 50, 10)
		

	def update(self, player):
		self.max_hp = player.max_hp
		self.max_mana = player.max_mana
		self.hp = player.hp
		self.mana = player.mana
		if self.max_hp != self.hp:
			hp_bar_diff = ((self.unit / self.max_hp) * self.hp)
			self.healthbar.width = hp_bar_diff
		if self.max_mana != self.mana:
			ma_bar_diff = ((self.unit / self.max_mana) * self.mana)
			self.manabar.width = ma_bar_diff
		else:
			self.manabar.width = self.unit
		self.player_lvl = self.my_font.render(str(player.level), True, (255, 255, 255))
		


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




class PowerWindow(object):
	"""The powers window"""
	def __init__(self, size, player):
		self.size = (int(size[0] / 1.2), int(size[1] / 1.2))
		self.pos = ((size[0] % self.size[0]) / 2, (size[1] % self.size[1]) / 2)
		self.player = player
		self.my_font = pygame.font.SysFont("arial", 20)
		self.state = False


	def update(self):
		position1_x = int(self.size[0]/6)
		position1_y = int(self.size[1]/4)
		self.power1_msg = self.my_font.render("Magic Missile", True, (255, 255, 255))
		self.power1_rect = pygame.Rect(position1_x, position1_y, 50, 10)

		position2_x = position1_x
		position2_y = position1_y + (self.size[1]/10)
		self.power2_msg = self.my_font.render("Fireball", True, (255, 255, 255))
		self.power2_rect = pygame.Rect(position2_x, position2_y, 50, 10)

		position3_x = position1_x
		position3_y = position2_y + (self.size[1]/10)
		self.power3_msg = self.my_font.render("Cone of Ice", True, (255, 255, 255))
		self.power3_rect = pygame.Rect(position3_x, position3_y, 50, 10)


	def draw_window(self, surf):
		window = pygame.Surface(self.size)
		window.blit(self.power1_msg, self.power1_rect)
		window.blit(self.power2_msg, self.power2_rect)
		window.blit(self.power3_msg, self.power3_rect)
		surf.blit(window, self.pos)

class MouseOver(object):
	"""The Mouse Over Window"""
	def __init__(self):
		self.state = 1
		self.my_font = pygame.font.SysFont("arial", 15)

	def mouse_img(self):
		if self.state == 1:
			img = pygame.image.load("Red_Sights.png").convert_alpha()
		elif self.state >= 2:
			img = pygame.image.load("Eye_Sights.png").convert_alpha()
		return img

	def check_mobs(self, mobs, bg):
		if self.state == 2:
			for mob in mobs:
				true_pos = vec2d((self.pos[0] - bg.rect.x),(self.pos[1] - bg.rect.y))
				distance = true_pos.get_distance(mob.pos)
				if distance < 15:
					self.update_txt(mob.text)
					self.state = 3

	def check_gui(self):
		pass
		

	def update_pos(self, pos):
		self.pos = (pos[0], pos[1] + 25)

	def update_txt(self, text):
		if text != []:
			message = []
			for line in text:
				the_line = self.my_font.render(line, True, (255, 255, 255))
				message.append(the_line)
			
			size = (150, len(text)*20)
			self.window = pygame.Surface((size))
			rect = pygame.Rect(0, 0, 5, 5)
			x = 0
			for msg in message:
				self.window.blit(message[x], rect)
				rect.y += 20
				x += 1
			
		


	def draw(self, surf):
		if self.state == 3:
			surf.blit(self.window, self.pos)
			

		


		




		
