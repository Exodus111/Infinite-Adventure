"""
The GUI file.
Contains both the graphical, and code logic for the gui.
"""

import pygame, random
from pygame.locals import *
from vec2d import vec2d

class GUI(object):
	"""
	This is the GUI overlay for the screen.

	"""
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
			self.healthbar.width = self.unit
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

class StartMenu(object):
	"""
	The Start Menu.
	The menu has three options:
	1. New Game
	2. Load Game (Only on if there is a game to load)
	3. Exit
	"""
	def __init__(self, size, select=1):
		self.size = size
		self.select(select)

		self.my_fontbig = pygame.font.SysFont("URW Chancery L Medium Italic", 72)
		self.my_fontsmall = pygame.font.SysFont("URW Chancery L Medium Italic", 38)

		self.m_rect = pygame.Rect(0, 0, 1, 1)
		self.menu_rects = []
		self.unit = (self.size[0]/4, self.size[1]/16)

		self.button1 = False
		self.button2 = False
		self.button3 = False

	def select(self, select):
		if select == 1:
			self.base_image = pygame.image.load("start_menu.jpg").convert()
		elif select == 2:
			self.base_image = pygame.image.load("death_menu.jpg").convert()
		self.base_rect = self.base_image.get_rect()
		self.image = pygame.transform.scale(self.base_image, self.size)
		self.rect = self.image.get_rect()

	def update(self):
		self.new_game = self.my_fontbig.render("New Game", True, (5, 5, 5))
		self.newrect = pygame.Rect(0,0, self.unit[0], self.unit[1])
		self.newrect.center = (self.size[0]/2, ((self.size[1]/2) - self.unit[1])) 
		self.menu_rects.append(self.newrect)

		self.load_game = self.my_fontbig.render("Load Game", True, (5, 5, 5))
		self.loadrect = pygame.Rect(0,0, self.unit[0], self.unit[1])
		self.loadrect.center = (self.size[0]/2, self.size[1]/2)
		self.menu_rects.append(self.loadrect)

		self.exit_game = self.my_fontbig.render("Exit", True, (5, 5, 5))
		self.exitrect = pygame.Rect(0,0, self.unit[0], self.unit[1])
		self.exitrect.center = (self.size[0]/2, ((self.size[1]/2) + self.unit[1]))
		self.menu_rects.append(self.exitrect)


	def draw(self, surf):
		surf.blit(self.image, self.rect)
		surf.blit(self.new_game, self.newrect)
		surf.blit(self.load_game, self.loadrect)
		surf.blit(self.exit_game, self.exitrect)
		if self.button1 == True:
			pygame.draw.rect(surf, pygame.Color("black"), self.newrect, 1)
		elif self.button2 == True:
			pygame.draw.rect(surf, pygame.Color("black"), self.loadrect, 1)
		elif self.button3 == True:
			pygame.draw.rect(surf, pygame.Color("black"), self.exitrect, 1)

	def mouse_mov(self, pos):
		self.m_rect.center = pos

		if self.m_rect.colliderect(self.newrect):
			self.button1 = True
			self.button2 = False
			self.button3 = False

		elif self.m_rect.colliderect(self.loadrect):
			self.button1 = False
			self.button2 = True
			self.button3 = False

		elif self.m_rect.colliderect(self.exitrect):
			self.button1 = False
			self.button2 = False
			self.button3 = True

		else: 
			self.button1 = False
			self.button2 = False
			self.button3 = False

	def mouse_press(self):
		button = 0
		if self.m_rect.colliderect(self.newrect):
			button = 1
		elif self.m_rect.colliderect(self.exitrect):
			button = 3
		return button


class PlayerWindow(object):
	"""The Player window
	The window consist of 5 positions.
	1. The players level: 160, 120
	2. Basic player information (Name and Class): 310, 85
	3. More information about the player: 310, 178
	4. Headline for Quests: 667, 472
	5. Quests, point by point: 528, 531
	6. Powers button: 180, 342
	"""
	def __init__(self, size, player):
		self.base_image = pygame.image.load("player_menu.jpg").convert()
		self.base_rect = self.base_image.get_rect()
		self.size = (int(size[0]/1.2), int(size[1]/1.2))
		self.pos_center = (int(size[0]/2), int(size[1]/2))
		self.image = pygame.transform.scale(self.base_image, self.size) 
		self.rect = self.image.get_rect()
		self.rect.center = self.pos_center

		self.pos_1 = (self._calc(160, 120))
		self.pos_2 = (self._calc(310, 75))
		self.pos_3 = (self._calc(340, 178))
		self.pos_4 = (self._calc(310, 420))
		self.pos_5 = (self._calc(340, 531))
		self.pos_6 = (self._calc(180, 342))

		self.my_fontbig = pygame.font.SysFont("URW Chancery L Medium Italic", 72)
		self.my_fontsmall = pygame.font.SysFont("URW Chancery L Medium Italic", 38)
		self.player = player
		self.state = False
		self.powerstate = False
		self.windowstate = False
		
	def _calc(self, xop, yop):
		old_basew = float(self.base_rect.w)
		old_baseh = float(self.base_rect.h)
		new_basew = float(self.rect.w)
		new_baseh = float(self.rect.h)
		xdiff = new_basew / old_basew
		ydiff = new_baseh / old_baseh
		x_pos = self.rect.x
		y_pos = self.rect.y
 		
 		return int((xop * xdiff) + x_pos), int((yop * ydiff) + y_pos)

 	def mouse_mov(self, pos, button):
 		if self.powerrect.collidepoint(pos):
 			self.windowstate = True
 		else: 
 			self.windowstate = False

 	def mouse_button(self, button):
 		if button == 1:
 			if self.windowstate == True:
 				self.powerstate = True

	def update(self):

		self.lvl = self.my_fontbig.render(str(self.player.level), True, (255, 0, 0))
		self.lvlrect = pygame.Rect(self.pos_1[0], self.pos_1[1], 50, 50)

		self.name = self.my_fontbig.render(self.player.ident, True, (0, 0, 0))
		self.namerect = pygame.Rect(self.pos_2[0], self.pos_2[1], 50, 50)

		playerinfo = "Hitpoints: %i/%i Mana: %i/%i Speed: %i" % (self.player.hp, self.player.max_hp, self.player.mana, self.player.max_mana, self.player.speed)
		self.info = self.my_fontsmall.render(playerinfo, True, (0, 0, 0))
		self.inforect = pygame.Rect(self.pos_3[0], self.pos_3[1], 50, 50)

		self.headquest = self.my_fontbig.render("Current Quests:", True, (0, 0, 0))
		self.headrect = pygame.Rect(self.pos_4[0], self.pos_4[1], 50, 50)

		self.quests = self.my_fontsmall.render("Quest 1...", True, (0, 0, 0))
		self.questrect = pygame.Rect(self.pos_5[0], self.pos_5[1], 50, 50)

		self.powers = self.my_fontbig.render("Powers", True, (0, 0, 0))
		self.powerrect = pygame.Rect(0, 0, 180, 50)
		self.powerrect.center = self.pos_6



	def draw(self, surf):
		surf.blit(self.image, self.rect.topleft)
		surf.blit(self.lvl, self.lvlrect)
		surf.blit(self.name, self.namerect)
		surf.blit(self.info, self.inforect)
		surf.blit(self.headquest, self.headrect)
		surf.blit(self.quests, self.questrect)
		surf.blit(self.powers, self.powerrect)
		pygame.draw.rect(surf, (0,0,0), self.powerrect, 2)
		if self.windowstate == True:
			pygame.draw.rect(surf, (255, 0, 0), self.powerrect, 5)

		#pygame.draw.rect(surf, (255, 0, 0), self.testrect)

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

	def check_tiles(self, tiles, bg):
		if self.state == 2:
			msg = []
			true_point = ((self.pos[0] - bg.rect.x),(self.pos[1] - bg.rect.y))
			for tile in tiles:
				if tile.rect.collidepoint(true_point):
					msg.append(tile.ident)
					self.update_txt(msg)
					self.state = 3


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
		self.pos = pos
		self.win_pos = (pos[0], pos[1] + 25) 

	def update_txt(self, text):
		if text != []:
			message = []
			width = 0
			for line in text:
				if width < len(line):
					width = len(line)
				the_line = self.my_font.render(line, True, (255, 255, 255))
				message.append(the_line)
			
			size = (width*7, len(text)*20)
			self.window = pygame.Surface((size))
			rect = pygame.Rect(0, 0, 5, 5)
			x = 0
			for msg in message:
				self.window.blit(message[x], rect)
				rect.y += 20
				x += 1
			
		


	def draw(self, surf):
		if self.state == 3:
			surf.blit(self.window, self.win_pos)
			

		


		




		
