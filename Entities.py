'''
Created on Jan 19, 2013

@author: aurelio
'''
import pygame
from pygame.locals import *

class Player(pygame.sprite.DirtySprite):  
    # Here I load up the player, and the variables necessary for movement and rotation.
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
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

class GameSurface(pygame.sprite.DirtySprite):
    def __init__(self, levelsize, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(levelsize).convert()
        self.rect = pygame.Rect(pos, levelsize)
        self.image.fill(color)
        self.dirty = 2
        self.levelsize = levelsize
        
      

class Room(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, block, fg, wg, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        self.number = num
        tiles, walls = self.sprite_map(block)
        self.tiles, self.walls = self.wall_collide(tiles, walls)
        fg.add(self.tiles)
        wg.add(self.walls)
        
    def wall_collide(self, tiles, walls):
        pygame.sprite.groupcollide(walls, tiles, True, False)
        return tiles, walls
    
    def dirty_sprite(self, group):
        for i in group:
            i.dirty = 1    
        
    # Here we make the rooms with floor tiles and wall tiles.
    def sprite_map(self, block):
        surf = self.image
        row = ((self.rect.right - self.rect.left) / block)
        col = ((self.rect.bottom - self.rect.top) / block)
        fx = self.rect.left
        fy = self.rect.top
        wx = (self.rect.left - (block))
        wy = (self.rect.top - (block))
        
        room_tiles = pygame.sprite.LayeredDirty()
        wall_tiles = pygame.sprite.LayeredDirty()
        for part in xrange(col):
            for i in xrange(row):
                i = Tile(surf, block, 2)
                i.rect.left = fx
                i.rect.top = fy
                room_tiles.add(i)
                fx += block
                
            fy += block
            fx = self.rect.left
        
        
        for part in range(col + 2):
            for i in range(row + 2):
                i = Tile(surf, block, 1)
                i.rect.x = wx
                i.rect.y = wy
                wall_tiles.add(i)
                wx += block
                
            wy += block
            wx = (self.rect.left - block)
                
        return room_tiles, wall_tiles



        
class Tile(pygame.sprite.DirtySprite): # The Tile sprite, this is one block in every room or wall, and we chose which tile we want.
    def __init__(self, surf, blocksize, select):
        pygame.sprite.DirtySprite.__init__(self)
        self.tile_select(blocksize, select)
        self.dirty = 1
        self.area = surf
    
    def tile_select(self, blocksize, select):
        if select == 1:
            self.image = pygame.image.load("wall_64.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 2:
            self.image = pygame.image.load("wood_64.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
        