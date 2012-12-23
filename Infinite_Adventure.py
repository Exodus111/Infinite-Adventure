'''
Created on Dec 22, 2012

@author: aurelio
'''
# Importing dependencies:
import pygame
from pygame.locals import *

# Setting up the screen
screen_mode = (640, 480)
color_blue = 100,149,237

class Game(object):      
    def __init__(self):
# Here I load stuff up, and set a lot of global variables :-P
        
        pygame.init()
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

        self.quit = False
        
    def update(self):
# This function is called in the gameloop, and so I use it to run code.
       
        (self.mx, self.my) = pygame.mouse.get_pos()
        if self.moveup == True:
            self.ky -= 20
        if self.movedown == True:
            self.ky += 20
        if self.moveleft == True:
            self.kx -= 20
        if self.moveright == True:
            self.kx += 20     
     
    def draw(self):
# This is the actual grapics, code must be added after the fill line.
        
        self.screen.fill(color_blue)
        self.screen.blit(self.mouse_image, (self.mx,self.my))
        self.screen.blit(self.player_image, (self.kx, self.ky))
        
        pygame.display.flip()
        
    def mainLoop(self):     
# The famous main loop. No game can run without it.
        
        while not self.quit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        self.moveup = True
                    if event.key == K_a:
                        self.moveleft = True
                    if event.key == K_s:
                        self.movedown = True
                    if event.key == K_d:
                        self.moveright = True
                elif event.type == KEYUP:
                    if event.key == K_w:
                        self.moveup = False
                    if event.key == K_a:
                        self.moveleft = False
                    if event.key == K_s:
                        self.movedown = False
                    if event.key == K_d:
                        self.moveright = False
                          
            self.update()
            self.draw()
            self.clock.tick(60)
                
if __name__ == "__main__":
    game = Game()
    game.mainLoop()