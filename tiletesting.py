'''
Created on Jan 8, 2013

@author: aurelio
This is a testfile to try out auto generated maps in the game Infinite Adventures.
There is some procedural work here, but for the most part this a very simple approach.
Move with W'A'S'D
'''
import pygame, sys, os, random
from pygame.locals import *

# This is the main class that runs the code gameloop and contains all the Definitions.
class main():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1024, 960))
        size = (8192, 8192)
        background = pygame.Surface(size)
        background = background.convert()
        background.fill((250, 250, 250))
        kx = ky = 0
        pygame.display.flip()
        
        clock = pygame.time.Clock()
        
        blocksize = 32  # This is important as it sets the base blocks all the maps are based on.
        
        player = Player(screen) # I added a playersprite, but it does nothing.
        
        #roomTiles, wallTiles = self.generate_room(blocksize, size)# This generates the map into two lists of sprites.
        
        #list = [wallTiles, roomTiles] # Here I put both lists into another, the position is important, as the second placement will override the first.
        
        fgroup = pygame.sprite.Group()
        wgroup = pygame.sprite.Group()
        
        #testroom = Room((blocksize*20), (blocksize*20), 50, 50, blocksize, fgroup, wgroup)
        
        self.generate_room(blocksize, size, fgroup, wgroup)
        print len(wgroup)
        print len(fgroup)
        #wallremove = pygame.sprite.groupcollide(wgroup, fgroup, True, False)
        #print len(wgroup)
        allsprites = pygame.sprite.LayeredUpdates(wgroup, fgroup)
        
        run = 1
        
        while run == 1:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = 0
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        ky += 150
                    elif event.key == K_a:
                        kx += 150
                    elif event.key == K_s:
                        ky -= 150
                    elif event.key == K_d:
                        kx -= 150 
            
            
            allsprites.update()
            
        
            allsprites.draw(background) # Here we draw the map onto the background surface.
            
            screen.blit(background, (kx,ky))
            pygame.display.update()
            allsprites.clear(screen, background)
            
            
    def direction(self, rect, rooms, block, run, surf): #This methods checks each direction to see if there is space for another room there.
        size = surf
        dir = [1, 1, 1, 1]
        if rooms != []:
            if rect.centerx + (block*40) > size[0]: #checking right
                dir[0] = 0 
            else: 
                r, l, u, d = self.room_checker(rect, rooms, block, "right")
                if r == False:
                    dir[0] = 0    
                else:
                    dir[0] = 1
            if rect.centerx - (block*40) < (size[0] - size[0]): #checking left
                dir[1] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "left")
                if l == False:
                    dir[1] = 0
                else:
                    dir[1] = 1
                
            if rect.centery - (block*40) < (size[1] - size[1]): #checking up
                dir[2] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "up")
                if u == False:
                    dir[2] = 0
                else:
                    dir[2] = 1
            if rect.centery + (block*40) > size[1]: #checking down
                dir[3] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "down")
                if d == False:
                    dir[3] = 0
                else:
                    dir[3] = 1
            
        print dir # Them we add the required distance to the X/Y coords. (we still need the size of the next Rect for left and up)
        if dir[0] == 1: # moving right
            x = (rect.x + rect.width)
            y = rect.y
            run = True
        elif dir[1] == 1: # moving left
            x = rect.x
            y = rect.y
            run = True
        elif dir[2] == 1: # moving up
            x = rect.x
            y = rect.y
            run = True
        elif dir[3] == 1: # moving down
            x = rect.x
            y = (rect.y + rect.height)
            run = True
        elif dir == [0, 0, 0, 0]: # end of loop
            x = rect.x
            y = rect.y
            run = False
        
        return x, y, dir, run
                      
    def room_checker(self, rect, rooms, block, dir): # This method checks if there are any previous rectangles in the way in any direction.
        right = left = up = down = True
        for i in rooms:
            if dir == "right":
                if rect.right < i.left: #right
                    if (rect.right + (block*40)) > i.left:
                        if (rect.top + (block*8)) < i.bottom and (rect.bottom + (block*8)) > i.top: 
                                right = False
            if dir == "left":
                if rect.left > i.right: #left
                    if (rect.left - (block*40)) < i.right:
                        if (rect.top + (block*8)) < i.bottom and (rect.bottom + (block*8)) > i.top: 
                                left = False
            
            if dir == "up":
                if rect.top > i.bottom: #up
                    if (rect.top - (block*40)) < i.bottom:
                        if (rect.left - (block*8)) < i.right and (rect.right + (block*8)) > i.left: 
                                up = False
            
            if dir == "down":
                if rect.bottom < i.top: #down
                    if (rect.bottom + (block*40)) > i.top:
                        if (rect.left - (block*8)) < i.right and (rect.right + (block*8)) > i.left: 
                                down = False
            
        return right, left, up, down
            

                            
    # Generates a room rectangle of random size, and ties the other rects together.      
    def generate_room(self, block, surf, fg, wg):
        run = True
        roomx, roomy = (block*2), (block*20)
        hw = hh = rw = rh = 1000
        rooms = []
        dir = [0, 0, 0, 0]
        while run:
           
           hw = random.randrange((block*4), (block*16), block)
           hh = random.randrange((block*4), (block*16), block)
           
           hew = random.randrange((rw - rw),(rw - (block*4)), block)
           heh = random.randrange((rh - rh), (rh - (block*4)), block)
           if dir[0] == 1:#right
                hh = block*2
                roomy += heh
                
           elif dir[1] == 1:#left
                hh = block*2
                roomx -= hw
                roomy += heh
           elif dir[2] == 1:#up
                hw = block*2
                roomy -= hh
                roomx += hew
           elif dir[3] == 1:#down
                hw = block*2
                roomx += hew
           else:
               roomx += hw
         
           
           hall = Room(hw, hh, roomx, roomy, block, fg, wg)
           rooms.append(hall.rect)
           
           rw = random.randrange((block*8), (block*20), block)
           rh = random.randrange((block*8), (block*20), block)
           
           hew = random.randrange((rw - rw),(rw - (block*4)), block)
           heh = random.randrange((rh - rh), (rh - (block*4)), block)
           
           if dir[0] == 1:#right
               roomx += hw 
               roomy -= heh
           elif dir[1] == 1:#left
               roomx -= rw
               roomy -= heh
           elif dir[2] == 1:#up
               roomy -= rh
               roomx -= hew
           elif dir[3] == 1:#down
               roomy += hh
               roomx -= hew
                
           room = Room(rw, rh, roomx, roomy, block, fg, wg)
           rooms.append(room.rect)
           
           roomx, roomy, dir, run = self.direction(room.rect, rooms, block, run, surf)
               
     
        
class Room(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, block, fg, wg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        tiles, walls = self.sprite_map(block)
        tiles, walls = self.wall_collide(tiles, walls)
        fg.add(tiles)
        wg.add(walls)
        
    def wall_collide(self, tiles, walls):
        pygame.sprite.groupcollide(walls, tiles, True, False)
        return tiles, walls
        
        
    # Here we make the rooms with floor tiles and wall tiles.
    def sprite_map(self, block):
        surf = self.image
        row = ((self.rect.right - self.rect.left) / block)
        col = ((self.rect.bottom - self.rect.top) / block)
        fx = self.rect.left
        fy = self.rect.top
        wx = (self.rect.left - (block))
        wy = (self.rect.top - (block))
        
        room_tiles = pygame.sprite.Group()
        wall_tiles = pygame.sprite.Group()
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
        self.area = surf
        self.tile_select(blocksize, select)
    
    def tile_select(self, blocksize, select):
        if select == 1:
            self.image = pygame.image.load("stone.jpg").convert()
            self.rect = self.image.get_rect()
            self.area.blit(self.image, (self.rect.x, self.rect.y))
        if select == 2:
            self.image = pygame.image.load("wood.jpg").convert()
            self.rect = self.image.get_rect()
            self.area.blit(self.image, (self.rect.x, self.rect.y))
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
            self.area.blit(self.image, (self.rect.x, self.rect.y))
            
            

class Player(pygame.sprite.DirtySprite): # Here we make the rooms with floor tiles and wall tiles.
    def __init__(self, screen):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.area = screen
        
if __name__ == '__main__': # To run.
    main()    
            
