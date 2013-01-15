'''
Created on Jan 8, 2013

@author: aurelio
'''
import pygame, sys, os, random
from pygame.locals import *

class main():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1024, 960))
        
        background = pygame.Surface((6400, 6400))
        background = background.convert()
        background.fill((250, 250, 250))
        kx = ky = 0
        self.background = background
        pygame.display.flip()
        
        clock = pygame.time.Clock()
        
        blocksize = 64
        size = 2
        
        player = Player(screen)
        
        roomTiles, wallTiles = self.generate_room(blocksize)
        list = [wallTiles, roomTiles]
        allsprites = pygame.sprite.LayeredDirty((list, player))

        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        ky += 50
                    elif event.key == K_a:
                        kx += 50
                    elif event.key == K_s:
                        ky -= 50
                    elif event.key == K_d:
                        kx -= 50 
            
            allsprites.update()
            allsprites.draw(background)
            screen.blit(background, (kx,ky))
            pygame.display.update()
            allsprites.clear(screen, background)
            
    def direction(self, rect, rooms, block, run):
        size = self.background.get_size()
        print size[0]
        print size [1]
        dir = [1, 1, 1, 1]
        if rooms != []:
            if rect.centerx + (block*18) > size[0]: #checking right
                dir[0] = 0 
            else: 
                r, l, u, d = self.room_checker(rect, rooms, block, "right")
                if r == False:
                    dir[0] = 0    
                else:
                    dir[0] = 1
            if rect.centerx - (block*18) < (size[0] - size[0]): #checking left
                dir[1] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "left")
                if l == False:
                    dir[1] = 0
                else:
                    dir[1] = 1
                
            if rect.centery - (block*18) < (size[1] - size[1]): #checking up
                dir[2] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "up")
                if u == False:
                    dir[2] = 0
                else:
                    dir[2] = 1
            if rect.centery + (block*18) > size[1]: #checking down
                dir[3] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "down")
                if d == False:
                    dir[3] = 0
                else:
                    dir[3] = 1
            
        print dir
        if dir[0] == 1: # moving right
            x = (rect.x + rect.width + (block*2))
            y = rect.y
            run = True
        elif dir[1] == 1: # moving left
            x = (rect.x -(block*2))
            y = rect.y
            run = True
        elif dir[2] == 1: # moving up
            x = rect.x
            y = (rect.y - (block*2))
            run = True
        elif dir[3] == 1: # moving down
            x = rect.x
            y = (rect.y + rect.height +(block*2))
            run = True
        elif dir == [0, 0, 0, 0]: # end of loop
            x = rect.x
            y = rect.y
            run = False
        
        return x, y, dir, run
                      
    def room_checker(self, rect, rooms, block, dir):
        right = left = up = down = True
        for i in rooms:
            if dir == "right":
                if rect.right < i.left: #right
                    if (rect.right + (block*28)) > i.left:
                        if (rect.top + (block*4)) < i.bottom and (rect.bottom + (block*4)) > i.top: 
                                right = False
            if dir == "left":
                if rect.left > i.right: #left
                    if (rect.left - (block*28)) < i.right:
                        if (rect.top + (block*4)) < i.bottom and (rect.bottom + (block*4)) > i.top: 
                                left = False
            
            if dir == "up":
                if rect.top > i.bottom: #up
                    if (rect.top - (block*28)) < i.bottom:
                        if (rect.left - (block*4)) < i.right and (rect.right + (block*4)) > i.left: 
                                up = False
            
            if dir == "down":
                if rect.bottom < i.top: #down
                    if (rect.bottom + (block*28)) > i.top:
                        if (rect.left - (block*4)) < i.right and (rect.right + (block*4)) > i.left: 
                                down = False
            
        return right, left, up, down
            

                            
    # Generates a room rectangle of random size.        
    def generate_room(self, block):
        run = True
        x = block
        y = block
        rooms = []
        walls = []
        rects = []
        dir = [0, 0, 0, 0]
        
        while run == True:
            hw = random.randrange((block*4), (block*12), block)
            hh = random.randrange((block*4), (block*12), block)
            
            rw = random.randrange((block*8), (block*24), block)
            rh = random.randrange((block*8), (block*24), block)
            if dir[0] == 1:#right
                hh = block*2
            elif dir[1] == 1:#left
                hh = block*2
                x -= hw
            elif dir[2] == 1:#up
                hw = block*2
                y -= hh
            elif dir[3] == 1:#down
                hw = block*2
            myhall = pygame.Rect(x, y, hw, hh)
            x, y, dir, run = self.direction(myhall, rects, block, run)
            if dir[0] == 1:
                pass
            elif dir[1] == 1:#left
                x -= rw
            elif dir[2] == 1:#up
                y -= rh
            myrect = pygame.Rect(x, y, rw, rh)
            x, y, dir, run = self.direction(myrect, rects, block, run)
            rects.append(myhall)
            rects.append(myrect)
            room_tiles, wall_tiles = self.sprite_map(myhall, block)
            rooms.append(room_tiles)
            walls.append(wall_tiles)
            room_tiles, wall_tiles = self.sprite_map(myrect, block)
            rooms.append(room_tiles)
            walls.append(wall_tiles)
        return rooms, walls
    
    # Takes a room rectangle and adds floor tiles and wall tiles as sprites
    def sprite_map(self, rect, block):
        surf = rect
        row = ((surf.right - surf.left) / block)
        col = ((surf.bottom - surf.top) / block)
        fx = surf.left
        fy = surf.top
        wx = (surf.left - block)
        wy = (surf.top - block)
        
        room_tiles = []
        wall_tiles = []
        for part in range(col):
            for i in range(row):
                i = Tile(surf, block, 3)
                i.rect.left = fx
                i.rect.top = fy
                room_tiles.append(i)
                fx += block
                
            fy += block
            fx = surf.left
            
        for part in range(col + 2):
            for i in range(row + 2):
                i = Tile(surf, block, 1)
                i.rect.x = wx
                i.rect.y = wy
                wall_tiles.append(i)
                wx += block
                
            wy += block
            wx = (surf.left - block)
            
        return room_tiles, wall_tiles
        
        
    
    
                    
class Player(pygame.sprite.DirtySprite):
    def __init__(self, screen):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.area = screen
        self.dirty = 1
        
        

class Tile(pygame.sprite.DirtySprite):
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
            self.image = pygame.image.load("wood.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
        
if __name__ == '__main__':
    main()    
            
