'''
Created on Jan 19, 2013

@author: aurelio
'''
import pygame, random
from pygame.locals import *
from vec2d import vec2d
import Mainloop

class Player(pygame.sprite.DirtySprite):  
    # Here I load up the player, and the variables necessary for movement and rotation.
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.dirty = 1
        self.rot = 0
        self.speed = 15
        self.dir = [0, 0, 0, 0]
        self.ident = "Player"
                
                

class Mob(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.npcmove = [0, 0, 0, 0]
        self.ident = "Mob"
        self.target = vec2d(0,0)
        self.pos = vec2d(0,0)
        self.room = 0
        self.walls = None
        self.npcmove = [0,0,0,0]
        self.counter = 0
        self.dir = 0

    def select(self, num):
        if num == 1:
            self.image = pygame.image.load("mob_green.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 10
            self.num = num
        elif num == 2:
            self.image = pygame.image.load("mob_red.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 10
            self.num = num
        elif num == 3:
            self.image = pygame.image.load("mob_yellow.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 10
            self.num = num
        elif num == 4:
            self.image = pygame.image.load("mob_orange.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 10
            self.num = num
        elif num == 5:
            self.image = pygame.image.load("mob_pink.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 15
            self.num = num
        elif num == 6:
            self.image = pygame.image.load("mob_white.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.speed = 20
            self.num = num

    def move(self, rooms):
        for room in rooms:
            if self.rect.colliderect(room.rect):
                self.room = room
        self.rect.centerx, self.rect.centery = self.pos[0], self.pos[1]

    def run(self, rooms, time):
        self.dirty = 1
        self.patrol(time)
        #self.track()
        self.move(rooms)

    def patrol(self, time):

        if self.room != 0:
            self.counter += time
            if self.counter > random.randint(400, 500):
                self.target = vec2d(random.randint(self.room.rect.left, self.room.rect.right), 
                    random.randint(self.room.rect.top, self.room.rect.bottom))
                self.dir = self.target - self.pos
                if self.dir.length > 3:
                    self.dir.length = 5
                self.counter = 0
        
            self.pos += self.dir

          # Here the NPC will track its target. (Usually the player) 
    def track(self, target):
        if self.rect.x + 500 > target.rect.x:
            if self.rect.x - 500 < target.rect.x:
                if self.rect.y + 500 > target.rect.y:
                    if self.rect.y - 500 < target.rect.y:
                        if self.rect.y > target.rect.y:
                            self.npcmove[0] = 1 #UP
                            self.npcmove[2] = 0
                        elif self.rect.y < target.rect.y:
                            self.npcmove[2] = 1 #DOWN
                            self.npcmove[0] = 0
                        if self.rect.x > target.rect.x:
                            self.npcmove[1] = 1 #LEFT
                            self.npcmove[3] = 0
                        elif self.rect.x < target.rect.x:
                            self.npcmove[3] = 1 #RIGHT
                            self.npcmove[1] = 0


     # movement for the NPC with collision detection.                   
    def movement(self, walls):
        if self.npcmove[0] == 1:
            self.rect.y -= self.speed
            self.collision(walls, "UP")
        if self.npcmove[1] == 1:
            self.rect.x -= self.speed
            self.collision(walls, "LEFT")
        if self.npcmove[2] == 1:
            self.rect.y += self.speed
            self.collision(walls, "DOWN")
        if self.npcmove[3] == 1:
            self.rect.x += self.speed
            self.collision(walls, "RIGHT")

    # Rectangle based collision detection. Requires a list of all rectangles to check collision on, 
# the rect object to check and a string for collision.
    def collision(self, rooms, direction):
        
        for i in rooms:
            if self.rect.colliderect(i.rect) == True:
                self.room = i
                for wall in i.walls:
                    if self.rect.colliderect(wall.rect) == True:
                        if direction == "UP":
                            self.rect.top = wall.rect.bottom
                        if direction == "LEFT":
                            self.rect.left = wall.rect.right
                        if direction == "DOWN":
                            self.rect.bottom = wall.rect.top
                        if direction == "RIGHT":
                            self.rect.right = wall.rect.left


class GameSurface(pygame.sprite.DirtySprite):
    def __init__(self, levelsize, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(levelsize).convert()
        self.rect = pygame.Rect(pos, levelsize)
        self.image.fill(color)
        self.dirty = 2
        self.levelsize = levelsize
        
      

class Room(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, block, fg, wg, num, ident):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        self.ident = ident
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
                i = Tile(surf, block, 3)
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
            self.image = pygame.image.load("stone.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 2:
            self.image = pygame.image.load("wood_64.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
        