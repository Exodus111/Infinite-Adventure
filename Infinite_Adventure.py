#!/usr/bin/env python
'''
Created on Dec 22, 2012

@author: aurelio
'''
# Importing dependencies:
import pygame, math
from pygame.locals import *

# Setting up the screen
screen_mode = (1240, 960)
color_blue = 100,149,237

class Game(object):      
    def __init__(self):
# Here I load stuff up, and set a lot of global variables :-P
        
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(screen_mode)
        pygame.display.set_caption("Pygame stuff")
        self.mouse_image = pygame.image.load("Red_Sights.png")
        self.player_image = pygame.image.load("Arrow_cursor.png")
        self.mx = (screen_mode[0])/2
        self.my = (screen_mode[1])/2
        self.kx = (screen_mode[0])/2
        self.ky = (screen_mode[1])/2
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False
        self.clock = pygame.time.Clock()
        self.rotangle = 0

        self.quit = False
        
    def update(self):
# This function is called in the gameloop, and so I use it to run code.
# This updates the position of the mouse image.        
        (self.mx, self.my) = pygame.mouse.get_pos()   
            
# This updates the movement of the player sprite
        if self.moveup == True:
            self.ky -= 10
        if self.movedown == True:
            self.ky += 10
        if self.moveleft == True:
            self.kx -= 10
        if self.moveright == True:
            self.kx += 10

# This updates the rotation of the playersprite towards the mouse
        mouse_x, mouse_y = self.mx, self.my
        player_x, player_y = self.kx, self.ky 
        angle = math.atan2(player_x-mouse_x, player_y-mouse_y)
        angle = angle * (180/ math.pi)
        angle = (angle) % 360
          
        self.rotangle = angle + 90
        self.player = pygame.transform.rotate(self.player_image, self.rotangle)

    def draw(self):
# This is the actual graphics, code must be added after the fill line.
        
        self.screen.fill(color_blue)
        self.screen.blit(self.mouse_image, (self.mx,self.my))
        self.screen.blit(self.player, (self.kx, self.ky))
        
        pygame.display.flip()
        
    def mainLoop(self):     
# The famous main loop. No game can run without it.
        
        while not self.quit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                elif event.type == KEYDOWN:
                    if event.key in (K_w, K_UP):
                        self.moveup = True
                    if event.key in (K_a, K_LEFT):
                        self.moveleft = True
                    if event.key in (K_s, K_DOWN):
                        self.movedown = True
                    if event.key in (K_d, K_RIGHT):
                        self.moveright = True
                elif event.type == KEYUP:
                    if event.key in (K_w, K_UP):
                        self.moveup = False
                    if event.key in (K_a, K_LEFT):
                        self.moveleft = False
                    if event.key in (K_s, K_DOWN):
                        self.movedown = False
                    if event.key in (K_d, K_RIGHT):
                        self.moveright = False
                          
            self.update()
            self.draw()
            self.clock.tick(60)
                
if __name__ == "__main__":
    game = Game()
    game.mainLoop()