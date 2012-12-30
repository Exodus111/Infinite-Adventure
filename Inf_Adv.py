'''
Created on Dec 29, 2012

@author: aurelio
'''
import pygame
from pygame.locals import *
from Mainloop import *

class Game(GameState):
    def __init__(self):
        self.w = 1240
        self.h = 960 
        GameState.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        self.brickColor = (156, 102, 31)
        self.coldgreyColor = (128, 138, 135)
        self.yellowColor = (255, 255, 0)
              
        level1 = [line.strip() for line in open('level_1.txt')]
        self.walls, self.end_rect = self.draw_map(level1, 16, 16)
        
        self.player_rect = pygame.Rect(32, 32, 16, 16)
        self.player_image = pygame.image.load("Arrow_cursor.png")
        self.player_moveUp, self.player_moveLeft, self.player_moveDown, self.player_moveRight = False, False, False, False
        
    def update(self):
        if self.player_moveUp == True:
            self.player_rect.y -= 5
        if self.player_moveLeft == True:
            self.player_rect.x -= 5
        if self.player_moveDown == True:
            self.player_rect.y += 5
        if self.player_moveRight == True:
            self.player_rect.x += 5
            
    
    def draw(self):
        self.screen.fill(self.brickColor)        
        for wall in self.walls:
            pygame.draw.rect(self.screen, (self.coldgreyColor), wall)
        pygame.draw.rect(self.screen, (self.yellowColor), self.end_rect)
        
        pygame.draw.rect(self.screen, (255, 255, 255), self.player_rect )
        self.screen.blit(self.player_image, (self.player_rect.x, self.player_rect.y))
     
    
    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player_moveUp = True
        if key in (K_a, K_LEFT):
            self.player_moveLeft = True
        if key in (K_s, K_DOWN):
            self.player_moveDown = True
        if key in (K_d, K_RIGHT):
            self.player_moveRight = True
             
            
    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player_moveUp = False
        if key in (K_a, K_LEFT):
            self.player_moveLeft = False
        if key in (K_s, K_DOWN):
            self.player_moveDown = False
        if key in (K_d, K_RIGHT):
            self.player_moveRight = False
        
    def mouse_down(self, button, pos):
        pass
    
    def mouse_up(self, button, pos):
        pass
    
    def mouse_motion(self, buttons, pos, rel):
        pass
    
    

            
            
s = Game()
s.main_loop(60)