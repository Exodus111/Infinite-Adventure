#!/usr/bin/env Python
'''
Created on Dec 29, 2012

This is the game file, this is where the actual game code will be stored.
At this moment this is my experiment file, and a lot of what I do here I'll push into the Game's "engine" file once I polish them.

@author: aurelio
'''
import pygame
from pygame.locals import *
from Mainloop import *

# This is the main class of the game, it inherits from the "engine" class, the __init__ method loads most of the game assets. 
class Game(GameState):
    def __init__(self):
        # First I load my chosen screen size and use it to override the default one, while initializing the engine.
        self.w = 1240
        self.h = 960 
        GameState.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        
        # Some colors, these will change.
        self.brickColor = (156, 102, 31)
        self.coldgreyColor = (128, 138, 135)
        self.yellowColor = (255, 255, 0)
        
        # Setting up some class variables for the game map, (background surface).
        self.level_size = (3200, 3200)
        self.background = pygame.Surface(self.level_size)
        self.bx_pos, self.by_pos = (0, 0)
        self.cp = (0,0)
        self.background.fill(self.brickColor)      
        # Then I load the first lvl from the external file.
        # And call the map creation method from the engine.
        level1 = [line.strip() for line in open('level_1.txt')]
        self.blocksize = 44
        self.walls, self.end_rect, self.space = self.draw_map(level1, self.blocksize, self.blocksize)
        
        # Here we quickly set up an image file for the mouse cursor (making sure to convert it and keep transparency)
        self.mouse_image = pygame.image.load("Red_Sights.png").convert_alpha()
        self.mouse_pos = (0, 0)
        
        # Here I load up the player, and the variables necesary for movement and rotation.
        self.player_rect = pygame.Rect(132, 132, 38, 38)
        self.player_image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.player_moveUp, self.player_moveLeft, self.player_moveDown, self.player_moveRight = False, False, False, False
        self.player_rot = 90
        
        
            
        
    # the update method. This one is called in the game_loop (from the engine) but it must be run in this file.    
    def update(self):
        
        # Here I find the player location on the screen. (since the player is actually moving around on the background surface) 
        self.cp = self.find_player(self.player_rect.x, self.player_rect.y, self.bx_pos, self.by_pos)
        
        # Movement for the player.
        if self.player_moveUp == True:
            if self.cp[1] > (self.h/50):    
                self.player_rect.y -= 15
                self.collision(self.walls, self.player_rect, "UP")
        if self.player_moveLeft == True:
            if self.cp[0] > (self.w/50):
                self.player_rect.x -= 15
                self.collision(self.walls, self.player_rect, "LEFT")
        if self.player_moveDown == True:
            if self.cp[1] < (self.h - (self.h/50)):
                self.player_rect.y += 15
                self.collision(self.walls, self.player_rect, "DOWN")
        if self.player_moveRight == True:
            if self.cp[0] < (self.w - (self.w/50)):
                self.player_rect.x += 15
                self.collision(self.walls, self.player_rect, "RIGHT")
        
        # This method call ensures the player image does not deform under rotation
        # IMPORTANT: the player image MUST be a square (equal sides).
        self.playerimg = self.rotate_image(self.player_image, (self.player_rot + 90))
        
        # Here we scroll the map using the mouse pointer.
        if self.mouse_pos[0] >= (self.w - (self.w /8)):
            if (self.bx_pos + self.level_size[0])  >= self.w + self.blocksize:
                if self.cp[0] > (self.w/50): 
                    self.bx_pos -= 50
        elif self.mouse_pos[0] <= (self.w /8):
            if self.bx_pos  != 0:
                if self.cp[0] < (self.w - (self.w/50)):
                    self.bx_pos += 50
        elif self.mouse_pos[1] >= (self.h - (self.h /8)):
            if (self.by_pos + self.level_size[1])  >= self.h + self.blocksize:
                if self.cp[1] > (self.h/50):
                    self.by_pos -= 50
        elif self.mouse_pos[1] <= (self.h /8):
            if (self.by_pos)  != 0:
                if self.cp[1] < (self.h - (self.h/50)):
                    self.by_pos += 50 
    
    # The draw function. This is where things are actually drawn to screen.
    # Its called in the engines mainloop, but must be run in this file.            
    def draw(self):
        # Here we blit background surface to the screen.
        self.screen.blit(self.background, (self.bx_pos, self.by_pos))
        
        # Here we draw the map onto the background surface.
        for floor in self.space:
            pygame.draw.rect(self.background, (self.brickColor), floor)
        for wall in self.walls:
            pygame.draw.rect(self.background, (self.coldgreyColor), wall)    
        pygame.draw.rect(self.background, (self.yellowColor), self.end_rect)
        
        # Here we draw the player, and the player image to the background.
        pygame.draw.rect(self.background, (255, 255, 255,), self.player_rect, -1)
        self.background.blit(self.playerimg, ((self.player_rect.x -3), (self.player_rect.y -3)))
        
        # Here we draw the mouse pointer image to the screen (NOT the background)
        self.screen.blit(self.mouse_image, self.mouse_pos)
        
     
    # An event method giving us all key down presses.
    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player_moveUp = True
        if key in (K_a, K_LEFT):
            self.player_moveLeft = True
        if key in (K_s, K_DOWN):
            self.player_moveDown = True
        if key in (K_d, K_RIGHT):
            self.player_moveRight = True
        if key == K_ESCAPE:
            pygame.quit()

    # An event method giving us all key up presses. 
    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player_moveUp = False
        if key in (K_a, K_LEFT):
            self.player_moveLeft = False
        if key in (K_s, K_DOWN):
            self.player_moveDown = False
        if key in (K_d, K_RIGHT):
            self.player_moveRight = False
        
    # Two event Methods for the mouse keys (down and up). buttons are 1=left , 2=middle, 3=right. 
    def mouse_down(self, button, pos):
        pass
    
    def mouse_up(self, button, pos):
        pass
    
    # Event method for mouse motion.
    def mouse_motion(self, buttons, pos, rel):
        self.mouse_pos = pos
        
        # Here we call the method to rotate the mouse.
        self.player_rot = self.rotate((self.cp[0], self.cp[1]), self.mouse_pos)
             
    

            
# This runs the game once we run this file. The number is fps.            
s = Game()
s.main_loop(60)