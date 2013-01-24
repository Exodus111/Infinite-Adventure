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
        self.sgidarkgray = (85, 85, 85)
        self.yellowColor = (255, 255, 0)
        
        # Setting up some class variables for the game map, (background surface).
        self.level_size = (6400, 6400)
        self.background = pygame.Surface(self.level_size).convert()
        self.bx_pos, self.by_pos = (0,0)
        self.cp = (0,0)
        self.background.fill(self.blackColor)      
        self.blocksize = 32
      
        # Here we quickly set up an image file for the mouse cursor (making sure to convert it and keep transparency)
        self.mouse_image = pygame.image.load("Red_Sights.png").convert_alpha()
        self.mouse_pos = (0, 0)
        
        # Here I load up the player, and the variables necessary for movement and rotation.
        self.player = Player()
        
        npcrect = pygame.Rect(500, 200, 32, 32)
        npcimage = pygame.image.load("Greendot.png").convert_alpha()
        self.npc1 = NPC(npcimage, npcrect, 10)
        
        #roomTiles, wallTiles = self.generate_room(self.blocksize, self.level_size)
        #self.walls = wallTiles
        #self.allsprites = pygame.sprite.RenderUpdates((wallTiles, roomTiles))
        
        
        roomTiles, wallTiles = self.test_room(self.blocksize)
        self.t_rooms = [roomTiles]
        self.t_walls = [wallTiles]
        self.walls = self.collision_list(self.t_walls, self.t_rooms)
        self.allsprites = pygame.sprite.RenderPlain((self.t_walls, self.t_rooms))
        
        self.playerimg = self.player.image
        
        
    # the update method. This one is called in the game_loop (from the engine) but it must be run in this file.    
    def update(self):
        
        # Here I find the player location on the screen. (since the player is actually moving around on the background surface) 
        
        
        # Movement for the player.
        self.player_move(self.player.dir, self.cp, (self.w, self.h), self.walls, self.player.rect, self.player.speed)
        # This method call ensures the player image does not deform under rotation
        # IMPORTANT: the player image MUST be a square (equal sides).
        
        
        
        self.entities = pygame.sprite.RenderPlain((self.player))
        # Temp out of drift: self.npc_track(self.player.rect, self.walls, self.npc1.npcmove, self.npc1.rect, self.npc1.speed)
    
    # The draw function. This is where things are actually drawn to screen.
    # Its called in the engines mainloop, but must be run in this file.            
    def draw(self):
        
        # Here we draw the mouse pointer image to the screen (NOT the background)
        
        
        self.allsprites.update()
        self.allsprites.draw(self.background) # Here we draw the map onto the background surface.
        self.entities.draw(self.background)
       
        
        
        self.screen.blit(self.background, (self.bx_pos, self.by_pos))
        self.screen.blit(self.mouse_image, self.mouse_pos)
        
        
        pygame.display.update()
        #self.allsprites.clear(self.screen, self.background)
        
        #Temp out of order  self.background.blit(self.npc1.image, (self.npc1.rect.x, self.npc1.rect.y))
        
        
        # Here we draw the mouse pointer image to the screen (NOT the background)
    
        
     
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