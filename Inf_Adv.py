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
class Game(Engine):
    def __init__(self):
        # First I load my chosen screen size and use it to override the default one, while initializing the engine.
        self.w = 1240
        self.h = 960 
        Engine.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        
        # Some colors, these will change.
        self.blackColor = (0, 0, 0)
        self.sgidarkgray = (85, 85, 85)
        self.yellowColor = (255, 255, 0)
        
        # Setting up some class variables for the game map, (background surface).
        self.level_size = (3200, 3200)
        self.background = pygame.Surface(self.level_size).convert()
        self.bx_pos, self.by_pos = (0,0)
        self.cp = (0,0)
        self.background.fill(self.blackColor)      
        # Then I load the first lvl from the external file.
        # And call the map creation method from the engine.
        level1 = [line.strip() for line in open('level_1.txt')]
        level2 = [line.strip() for line in open('level_2.txt')]
        level3 = [line.strip() for line in open('level_3.txt')]
        level4 = [line.strip() for line in open('level_4.txt')]
        level5 = [line.strip() for line in open('level_5.txt')]
        self.blocksize = 64
        self.generate = True
        self.lvlnum = 1
        self.lvls = [level1, level2, level3, level4, level5]
        # Here we quickly set up an image file for the mouse cursor (making sure to convert it and keep transparency)
        self.mouse_image = pygame.image.load("Red_Sights.png").convert_alpha()
        self.mouse_pos = (0, 0)
        
        # Here I load up the player, and the variables necesary for movement and rotation.
        self.player_rect = pygame.Rect(132, 132, 38, 38)
        self.player_image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.player_rot = 90
        self.player_move = [0,0,0,0]
        
        self.player = Player(self.player_rect, self.player_rot, 15 )
        
        npcrect = pygame.Rect(500, 200, 32, 32)
        npcimage = pygame.image.load("Greendot.png").convert_alpha()
        self.npc1 = NPC(npcimage, npcrect, 10)
        
    def next_level(self, playerrect, endzonerect):
        if self.generate == False:
            if playerrect.colliderect(endzonerect) == True:
                self.lvlnum += 1 
                self.generate = True
    
    def map_generate(self, generate, lvlnum, lvlfile, blocksize):
        if generate == True:
            if lvlnum == 1:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[0], blocksize, blocksize)
                self.player_rect.x = self.start_rect.x
                self.player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
            elif lvlnum == 2:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[1], blocksize, blocksize)
                self.player_rect.x = self.start_rect.x
                self.player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
            elif lvlnum == 3:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[2], blocksize, blocksize)
                self.player_rect.x = self.start_rect.x
                self.player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
            elif lvlnum == 4:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[3], blocksize, blocksize)
                self.player_rect.x = self.start_rect.x
                self.player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
            elif lvlnum == 5:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[4], blocksize, blocksize)
                self.player_rect.x = self.start_rect.x
                self.player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
            
        
    # the update method. This one is called in the game_loop (from the engine) but it must be run in this file.    
    def update(self):
        self.map_generate(self.generate, self.lvlnum, self.lvls, self.blocksize)
        self.next_level(self.player_rect, self.end_rect)
        
        # Here I find the player location on the screen. (since the player is actually moving around on the background surface) 
        self.cp = self.find_player(self.player_rect.x, self.player_rect.y, self.bx_pos, self.by_pos)
        
        # Movement for the player.
        self.player.player_move(self.player_move, self.cp, (self.w, self.h), self.walls)

        # This method call ensures the player image does not deform under rotation
        # IMPORTANT: the player image MUST be a square (equal sides).
        self.playerimg = self.rotate_image(self.player_image, (self.player_rot + 90))
        
        # Here we scroll the map using the mouse pointer.
        if self.mouse_pos[0] >= (self.w - (self.w /8)):
            if (self.bx_pos + self.level_size[0])  >= self.w + self.blocksize:
                if self.cp[0] > self.blocksize: 
                    self.bx_pos -= 50
        elif self.mouse_pos[0] <= (self.w /8):
            if self.bx_pos  < -self.blocksize:
                if self.cp[0] < (self.w - self.blocksize):
                    self.bx_pos += 50
        elif self.mouse_pos[1] >= (self.h - (self.h /8)):
            if (self.by_pos + self.level_size[1])  >= self.h + self.blocksize:
                if self.cp[1] > self.blocksize:
                    self.by_pos -= 50
        elif self.mouse_pos[1] <= (self.h /8):
            if (self.by_pos)  < -self.blocksize:
                if self.cp[1] < (self.h - self.blocksize):
                    self.by_pos += 50 
    
        self.npc1.npc_move(self.player_rect, self.walls)
    
    # The draw function. This is where things are actually drawn to screen.
    # Its called in the engines mainloop, but must be run in this file.            
    def draw(self):
        # Here we blit background surface to the screen.
        self.screen.blit(self.background, (self.bx_pos, self.by_pos))
        
        # Here we draw the map onto the background surface.
        for floor in self.space:
            pygame.draw.rect(self.background, (self.blackColor), floor)
        for wall in self.walls:
            pygame.draw.rect(self.background, (self.sgidarkgray), wall)    
        pygame.draw.rect(self.background, (self.yellowColor), self.end_rect)
        pygame.draw.rect(self.background, (200, 200, 255), self.start_rect)
        
        
        self.background.blit(self.npc1.image, (self.npc1.rect.x, self.npc1.rect.y))
        # Here we draw the player, and the player image to the background.
        pygame.draw.rect(self.background, (255, 255, 255,), self.player_rect, -1)
        self.background.blit(self.playerimg, ((self.player_rect.x -3), (self.player_rect.y -3)))
        
        # Here we draw the mouse pointer image to the screen (NOT the background)
        self.screen.blit(self.mouse_image, self.mouse_pos)
    
        
     
    # An event method giving us all key down presses.
    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player_move[0] = 1
        if key in (K_a, K_LEFT):
            self.player_move[1] = 1
        if key in (K_s, K_DOWN):
            self.player_move[2] = 1
        if key in (K_d, K_RIGHT):
            self.player_move[3] = 1
        if key == K_ESCAPE:
            pygame.quit()

    # An event method giving us all key up presses. 
    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player_move[0] = 0
        if key in (K_a, K_LEFT):
            self.player_move[1] = 0
        if key in (K_s, K_DOWN):
            self.player_move[2] = 0
        if key in (K_d, K_RIGHT):
            self.player_move[3] = 0
    
        
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
             
    
class Player(Engine):
    
    # Here I load up the player, and the variables necessary for movement and rotation.
    def __init__(self, rect, rot, speed ):
        self.player_rect = rect
        self.player_rot = rot
        self.player_speed = speed
    
    
    def player_move(self, dir, screenpos, screensize, walls):
        player_rect = self.player_rect
        if dir[0] == 1:
            if screenpos[1] > (screensize[1]/50):    
                player_rect.y -= self.player_speed
                self.collision(walls, player_rect, "UP")
        if dir[1] == 1:
            if screenpos[0] > (screensize[0]/50):
                player_rect.x -= self.player_speed
                self.collision(walls, player_rect, "LEFT")
        if dir[2] == 1:
            if screenpos[1] < (screensize[1] - (screensize[1]/50)):
                player_rect.y += self.player_speed
                self.collision(walls, player_rect, "DOWN")
        if dir[3] == 1:
            if screenpos[0] < (screensize[0] - (screensize[0]/50)):
                player_rect.x += self.player_speed
                self.collision(walls, player_rect, "RIGHT")
                
                

class NPC(Engine):
    def __init__(self, image, rect, speed):
        self.image = image
        self.rect = rect
        self.speed = speed
        self.npcmove = [0, 0, 0, 0]
        
    def npc_move(self, target, walls):
        if self.rect.x + 500 > target.x:
            if self.rect.x - 500 < target.x:
                if self.rect.y + 500 > target.y:
                    if self.rect.y - 500 < target.y:
                        if self.rect.y > target.y:
                            self.npcmove[0] = 1 #UP
                            self.npcmove[2] = 0
                        elif self.rect.y < target.y:
                            self.npcmove[2] = 1 #DOWN
                            self.npcmove[0] = 0
                        if self.rect.x > target.x:
                            self.npcmove[1] = 1 #LEFT
                            self.npcmove[3] = 0
                        elif self.rect.x < target.x:
                            self.npcmove[3] = 1 #RIGHT
                            self.npcmove[1] = 0
                        self.movement(walls)
                        
    def movement(self, walls):
        if self.npcmove[0] == 1:
            self.rect.y -= self.speed
            self.collision(walls, self.rect, "UP")
        if self.npcmove[1] == 1:
            self.rect.x -= self.speed
            self.collision(walls, self.rect, "LEFT")
        if self.npcmove[2] == 1:
            self.rect.y += self.speed
            self.collision(walls, self.rect, "DOWN")
        if self.npcmove[3] == 1:
            self.rect.x += self.speed
            self.collision(walls, self.rect, "RIGHT")
                            
                                 
        
        
    
    

            
# This runs the game once we run this file. The number is fps.            
s = Game()
s.main_loop(60)