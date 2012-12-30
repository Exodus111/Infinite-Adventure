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
        self.walls, self.end_rect = self.draw_map(level1, 32, 32)
        
        self.mouse_image = pygame.image.load("Red_Sights.png")
        self.mouse_pos = (0, 0)
        
        self.player_rect = pygame.Rect(132, 132, 38, 38)
        self.player_image = pygame.image.load("Arrow_cursor.png")
        self.player_moveUp, self.player_moveLeft, self.player_moveDown, self.player_moveRight = False, False, False, False
        self.player_rot = 90
        
    def collision(self, walls, rect, direction):
        for wall in walls:
            if rect.colliderect(wall):
                if direction == "UP":
                    rect.top = wall.bottom
                if direction == "LEFT":
                    rect.left = wall.right
                if direction == "DOWN":
                    rect.bottom = wall.top
                if direction == "RIGHT":
                    rect.right = wall.left
                
                    
        
        
    def update(self):
        if self.player_moveUp == True:
            self.player_rect.y -= 5
            self.collision(self.walls, self.player_rect, "UP")
        if self.player_moveLeft == True:
            self.player_rect.x -= 5
            self.collision(self.walls, self.player_rect, "LEFT")
        if self.player_moveDown == True:
            self.player_rect.y += 5
            self.collision(self.walls, self.player_rect, "DOWN")
        if self.player_moveRight == True:
            self.player_rect.x += 5
            self.collision(self.walls, self.player_rect, "RIGHT")
        
        self.playerimg = self.rotate_image(self.player_image, (self.player_rot + 90))
        
            
    
    def draw(self):
        self.screen.fill(self.brickColor)        
        for wall in self.walls:
            pygame.draw.rect(self.screen, (self.coldgreyColor), wall)
        pygame.draw.rect(self.screen, (self.yellowColor), self.end_rect)
        
        pygame.draw.rect(self.screen, (255, 255, 255), self.player_rect)
        self.screen.blit(self.playerimg, ((self.player_rect.x -3), (self.player_rect.y -3)))
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
        self.player_rot = self.rotate((self.player_rect.x, self.player_rect.y), self.mouse_pos)
       
    

            
            
s = Game()
s.main_loop(60)