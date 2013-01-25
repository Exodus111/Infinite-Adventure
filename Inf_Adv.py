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
from Entities import *

# This is the main class of the game, it inherits from the "engine" class, the __init__ method loads most of the game assets. 
class Game(Engine):
    def __init__(self):
        # First I load my chosen screen size and use it to override the default one, while initializing the engine.
        self.w = 1240
        self.h = 960 
        Engine.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        
        # Some colors, these will change.
        self.blackColor = (0, 0, 0)
        white_color = (255, 255, 255)
        self.sgidarkgray = (85, 85, 85)
        self.yellowColor = (255, 255, 0)
        
        # Setting up some class variables for the game map, (background surface).
        self.level_size = (4800, 4800)
        self.background = pygame.Surface(self.level_size).convert()
        self.bx_pos, self.by_pos = (0,0)
        self.cp = (0,0)
        self.background.fill(white_color)      
        self.blocksize = 32
      
        # Here we quickly set up an image file for the mouse cursor (making sure to convert it and keep transparency)
        self.mouse_image = pygame.image.load("Red_Sights.png").convert_alpha()
        self.mouse_pos = (0, 0)
        
        # Here I load up the player, and the variables necessary for movement and rotation.
        self.player = Player()
        self.player.rect.center = (500, 900)
        
        npcrect = pygame.Rect(500, 200, 32, 32)
        npcimage = pygame.image.load("Greendot.png").convert_alpha()
        self.npc1 = NPC(npcimage, npcrect, 10)
        
       
        
        
        fgroup = pygame.sprite.Group()
        wgroup = pygame.sprite.Group()
        
        #self.rooms = Room((self.blocksize*20), (self.blocksize*20), 50, 50, self.blocksize, fgroup, wgroup)
        self.rooms = self.generate_room(self.blocksize, self.level_size, fgroup, wgroup)
        
        pygame.sprite.groupcollide(wgroup, fgroup, True, False)
        self.allsprites = pygame.sprite.LayeredUpdates(wgroup, fgroup)
        
        
        self.playerimg = self.player.image
        
        
    # the update method. This one is called in the game_loop (from the engine) but it must be run in this file.    
    def update(self):
        
       
        
        # Movement for the player.
        self.player_move(self.player.dir, self.cp, (self.w, self.h), self.rooms, self.player, self.player.speed)
        self.allsprites.add(self.player)
        
        # Temp out of drift: self.npc_track(self.player.rect, self.walls, self.npc1.npcmove, self.npc1.rect, self.npc1.speed)
    
    # The draw function. This is where things are actually drawn to screen.
    # Its called in the engines mainloop, but must be run in this file.            
    def draw(self):
        
        
        
        
        self.allsprites.update()
        self.allsprites.draw(self.background) # Here we draw the map onto the background surface.
        self.screen.blit(self.background, (self.bx_pos, self.by_pos))
        self.screen.blit(self.mouse_image, self.mouse_pos) # Here we draw the mouse pointer image to the screen (NOT the background)
        pygame.display.update()
        
        #Temp out of order  self.background.blit(self.npc1.image, (self.npc1.rect.x, self.npc1.rect.y))  
     
    # An event method giving us all key down presses.
    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player.dir[0] = 1
        if key in (K_a, K_LEFT):
            self.player.dir[1] = 1
        if key in (K_s, K_DOWN):
            self.player.dir[2] = 1
        if key in (K_d, K_RIGHT):
            self.player.dir[3] = 1
        if key == K_ESCAPE:
            pygame.quit()

    # An event method giving us all key up presses. 
    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player.dir[0] = 0
        if key in (K_a, K_LEFT):
            self.player.dir[1] = 0
        if key in (K_s, K_DOWN):
            self.player.dir[2] = 0
        if key in (K_d, K_RIGHT):
            self.player.dir[3] = 0
    
        
    # Two event Methods for the mouse keys (down and up). buttons are 1=left , 2=middle, 3=right. 
    def mouse_down(self, button, pos):
        pass
    
    def mouse_up(self, button, pos):
        pass
    
    # Event method for mouse motion.
    def mouse_motion(self, buttons, pos, rel):
        self.mouse_pos = pos
        
        # Here we scroll the map using the mouse pointer.
        self.bx_pos, self.by_pos = self.map_scroll(self.mouse_pos, self.w, self.h, self.level_size, self.cp, self.blocksize, self.bx_pos, self.by_pos)
        # Here we call the method to rotate the mouse.
        self.cp = self.find_player(self.player.rect.x, self.player.rect.y, self.bx_pos, self.by_pos)
        self.player.rot = self.rotate((self.cp[0], self.cp[1]), self.mouse_pos)
        self.player.image = self.rotate_image(self.playerimg, (self.player.rot))
                  
# This runs the game once we run this file. The number is fps.            
s = Game()
s.main_loop(60)