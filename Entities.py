'''
Created on Jan 19, 2013

@author: aurelio
'''
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):  
    # Here I load up the player, and the variables necessary for movement and rotation.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(132, 132, 38, 38)
        self.image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.dirty = 1
        self.rot = 90
        self.speed = 15
        self.dir = [0, 0, 0, 0]
                
                

class NPC(pygame.sprite.Sprite):
    def __init__(self, image, rect, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = rect
        self.dirty = 1
        self.speed = speed
        self.npcmove = [0, 0, 0, 0]
        
class Tile(pygame.sprite.Sprite): # The Tile sprite, this is one block in every room or wall, and we chose which tile we want.
    def __init__(self, surf, blocksize, select):
        pygame.sprite.Sprite.__init__(self)
        self.tile_select(blocksize, select)
        self.dirty = 2
        self.area = surf
    
    def tile_select(self, blocksize, select):
        if select == 1:
            self.image = pygame.image.load("stone.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 2:
            self.image = pygame.image.load("wood.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
        