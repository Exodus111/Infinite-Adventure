#!/usr/bin/env Python
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
        self.level_size = (3200, 3200)
        GameState.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        
        
        self.brickColor = (156, 102, 31)
        self.coldgreyColor = (128, 138, 135)
        self.yellowColor = (255, 255, 0)
        
        
        self.background = pygame.Surface(self.level_size)
        self.bx_pos, self.by_pos = (0, 0)
        self.cp = (0,0)
        
        self.background.fill(self.brickColor)
        print self.screen.get_size()      
        level1 = [line.strip() for line in open('level_1.txt')]
        self.walls, self.end_rect, self.space = self.draw_map(level1, 44, 44)
        
        self.mouse_image = pygame.image.load("Red_Sights.png").convert_alpha()
        self.mouse_pos = (0, 0)
        
        self.player_rect = pygame.Rect(132, 132, 38, 38)
        self.player_image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.player_moveUp, self.player_moveLeft, self.player_moveDown, self.player_moveRight = False, False, False, False
        self.player_rot = 90
        

    def find_player(self, px, py, mx, my):
        
        if mx >= 0:
            player_x =  ((px - px) - mx) + px
        elif mx < 0:
            player_x = ((px - px) + mx) + px
        if my >= 0:
            player_y = ((py - py) - my) + py
        elif my < 0:
            player_y = ((py - py) + my) + py
            
        return (player_x, player_y)
            
        
                
        
        
    def update(self):

        self.cp = self.find_player(self.player_rect.x, self.player_rect.y, self.bx_pos, self.by_pos)
        
        
        if self.player_moveUp == True:
            self.player_rect.y -= 15
            self.collision(self.walls, self.player_rect, "UP")
        if self.player_moveLeft == True:
            self.player_rect.x -= 15
            self.collision(self.walls, self.player_rect, "LEFT")
        if self.player_moveDown == True:
            self.player_rect.y += 15
            self.collision(self.walls, self.player_rect, "DOWN")
        if self.player_moveRight == True:
            self.player_rect.x += 15
            self.collision(self.walls, self.player_rect, "RIGHT")
        
        self.playerimg = self.rotate_image(self.player_image, (self.player_rot + 90))
        
        if self.mouse_pos[0] >= (self.w - (self.w /8)):
            if (self.bx_pos + self.level_size[0])  != self.w:
                #if self.bx_pos < self.player_rect.x:
                self.bx_pos = self.bx_pos - 50
        elif self.mouse_pos[0] <= (self.w /8):
            if self.bx_pos  != 0:
                #if (self.bx_pos + self.level_size[0]) > self.player_rect.x:
                self.bx_pos = self.bx_pos + 50
        elif self.mouse_pos[1] >= (self.h - (self.h /8)):
            if (self.by_pos + self.level_size[1])  != self.h:
                #if self.by_pos > self.player_rect.y:
                self.by_pos = self.by_pos - 50
        elif self.mouse_pos[1] <= (self.w /8):
            if (self.by_pos)  != 0:
                #if (self.by_pos + self.level_size[1]) > self.player_rect.y:
                self.by_pos = self.by_pos + 50 
                
        
            
    
    def draw(self):
        self.screen.blit(self.background, (self.bx_pos, self.by_pos))
        
        for floor in self.space:
            pygame.draw.rect(self.background, (self.brickColor), floor)
           
              
        for wall in self.walls:
            pygame.draw.rect(self.background, (self.coldgreyColor), wall)
    
            
        pygame.draw.rect(self.background, (self.yellowColor), self.end_rect)
        
        pygame.draw.rect(self.background, (255, 255, 255,), self.player_rect, 1)
        self.background.blit(self.playerimg, ((self.player_rect.x -3), (self.player_rect.y -3)))
    
        self.screen.blit(self.mouse_image, self.mouse_pos)
        
     
    
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
        self.mouse_pos = pos
        self.player_rot = self.rotate((self.cp[0], self.cp[1]), self.mouse_pos)
             
    

            
            
s = Game()
s.main_loop(120)