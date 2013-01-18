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
        size = (6400, 6400)
        background = pygame.Surface(size)
        background = background.convert()
        background.fill((250, 250, 250))
        kx = ky = 0
        pygame.display.flip()
        
        clock = pygame.time.Clock()
        
        blocksize = 32 # This is important as it sets the base blocks all the maps are based on.
        
        player = Player(screen) # I added a playersprite, but it does nothing.
        
        roomTiles, wallTiles = self.generate_room(blocksize, size)# This generates the map into two lists of sprites.
        
        
        list = [wallTiles, roomTiles] # Here I put both lists into another, the position is important, as the second placement will override the first.
        allsprites = pygame.sprite.LayeredDirty((list, player)) # Here I add the list to a DirtySprite class (does nothing atm)
        run = 1
        
        while run == 1:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = 0
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
            allsprites.draw(background) # Here we draw the map onto the background surface.
            screen.blit(background, (kx,ky))
            pygame.display.update()
            allsprites.clear(screen, background)
            
    def direction(self, rect, rooms, block, run, surf): #This methods checks each direction to see if there is space for another room there.
        size = surf
        print size[0]
        print size [1]
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
    def generate_room(self, block, surf):
        print surf[0]
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
            
            if dir[0] == 1:#right
                x += hw 
            elif dir[1] == 1:#left
                x -= rw
            elif dir[2] == 1:#up
                y -= rh
            elif dir[3] == 1:#down
                y += hh
            myrect = pygame.Rect(x, y, rw, rh)
            x, y, dir, run = self.direction(myrect, rects, block, run, surf) #Checks the directions
            rects.append(myhall)
            rects.append(myrect)
            room_tiles, wall_tiles = self.sprite_map(myhall, block)
            rooms.append(room_tiles)
            walls.append(wall_tiles)
            room_tiles, wall_tiles = self.sprite_map(myrect, block)
            rooms.append(room_tiles)
            walls.append(wall_tiles)
        return rooms, walls
    
    # Here we make the rooms with floor tiles and wall tiles.
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
        
        
    
    
                    
class Player(pygame.sprite.DirtySprite): # Here we make the rooms with floor tiles and wall tiles.
    def __init__(self, screen):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load("Arrow_cursor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.area = screen
        self.dirty = 1
        
        

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
            self.image = pygame.image.load("wood.jpg").convert()
            self.rect = self.image.get_rect()
        if select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.rect = self.image.get_rect()
        
if __name__ == '__main__': # To run.
    main()    
            
