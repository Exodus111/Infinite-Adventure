'''
Created on Dec 29, 2012

@author: aurelio
'''

# This file can be used as a base for pretty much any Pygame based game (except for the Wall class)


import pygame, math, sys, os, random
from pygame.locals import *
from Entities import *

# First we intialize pygame and set up a few class variables.
class Engine(object):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):   
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.mouse.set_visible(False)      
        self.screen = pygame.display.set_mode(size, DOUBLEBUF|HWSURFACE)
        self.clock = pygame.time.Clock()
        self.running = False
        
     
# The Event handler fires off in case of events and runs the appropriate function.        
    def event_handler(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.key_down(event.key)
            elif event.type == KEYUP:
                self.key_up(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event.button, event.pos)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)
        
#The mainloop runs the game, nothing that is not in here will run.
    def main_loop(self, fps=0): 
        self.running = True
        
        while self.running:
            pygame.display.set_caption("Infinite Adventure. FPS: %i" % self.clock.get_fps())
            self.event_handler()
            self.update()
            self.draw()
            #pygame.display.flip()
            self.clock.tick(fps)
            
    
# This function is also run in the mainloop, lots of code will go here, but mostly in child classes.
    def update(self): 
        pass
    
# This function is also called by the main loop, and will also mostly be run by child classes.
    def draw(self): 
        pass
    
    def key_down(self, key):
        pass
    
    def key_up(self, key):
        pass
    
    def mouse_down(self, button, pos):
        pass
    
    def mouse_up(self, button, pos):
        pass
    
    def mouse_motion(self, buttons, pos, rel):
        pass
    
   # Movement and collision detection calls for the player 
    def player_move(self, dir, screenpos, screensize, rooms, player, player_speed):
        if dir[0] == 1:
            if screenpos[1] > (screensize[1]/50):    
                player.rect.y -= player_speed
                self.collision(rooms, player, "UP")
        if dir[1] == 1:
            if screenpos[0] > (screensize[0]/50):
                player.rect.x -= player_speed
                self.collision(rooms, player, "LEFT")
        if dir[2] == 1:
            if screenpos[1] < (screensize[1] - (screensize[1]/50)):
                player.rect.y += player_speed
                self.collision(rooms, player, "DOWN")
        if dir[3] == 1:
            if screenpos[0] < (screensize[0] - (screensize[0]/50)):
                player.rect.x += player_speed
                self.collision(rooms, player, "RIGHT")
        
    
    # Rotates any object, to face any other object.        
    def rotate(self, pos1, pos2):  
        angle = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        angle = angle * (180/ math.pi)
        angle = (angle) % 360
        return angle
   
   # Pygame rotation messes up images, this keeps em in line. 
    def rotate_image(self, image, angle):
        img_rect = image.get_rect()
        img_rotd = pygame.transform.rotate(image, angle)
        img_rect.center = img_rotd.get_rect().center
        img_rotd = img_rotd.subsurface(img_rect).copy()
        return img_rotd
    
# Rectangle based collision detection. Requires a list of all rectangles to check collision on, 
# the rect object to check and a string for collision.
    def collision(self, rooms, sprite, direction):
        
        for i in rooms:
            if sprite.rect.colliderect(i.rect) == True:
                print i.number
                for wall in i.walls:
                    if sprite.rect.colliderect(wall.rect) == True:
                        if direction == "UP":
                            sprite.rect.top = wall.rect.bottom
                        if direction == "LEFT":
                            sprite.rect.left = wall.rect.right
                        if direction == "DOWN":
                            sprite.rect.bottom = wall.rect.top
                        if direction == "RIGHT":
                            sprite.rect.right = wall.rect.left
                      
        
       
                    
    # We are using two surfaces, one for the screen and one for the map (so I can scroll the game)
        # So I needed a method to find the location of an object on the background surface to the screen surface.
        # px, py are coords for the object on the surface, and mx, my are the coords for the surface location on the screen.
    def find_player(self, px, py, mx, my):
        
        if mx >= 0:
            player_x =  ((px - px) - mx) + px
        elif mx < 0:
            player_x = ((px - px) + mx) + px
        if my >= 0:
            player_y = ((py - py) - my) + py
        elif my < 0:
            player_y = ((py - py) + my) + py
            
        return (player_x, player_y)
   
   # Here the NPC will track its target. (Usually the player) 
    def npc_track(self, target, walls, npcmove, rect, speed):
        if rect.x + 500 > target.x:
            if rect.x - 500 < target.x:
                if rect.y + 500 > target.y:
                    if rect.y - 500 < target.y:
                        if rect.y > target.y:
                            npcmove[0] = 1 #UP
                            npcmove[2] = 0
                        elif rect.y < target.y:
                            npcmove[2] = 1 #DOWN
                            npcmove[0] = 0
                        if rect.x > target.x:
                            npcmove[1] = 1 #LEFT
                            npcmove[3] = 0
                        elif rect.x < target.x:
                            npcmove[3] = 1 #RIGHT
                            npcmove[1] = 0
                        self.npc_movement(walls, npcmove, rect, speed)
     
     # movement for the NPC with collision detection.                   
    def npc_movement(self, walls, npcmove, rect, speed):
        if npcmove[0] == 1:
            rect.y -= speed
            self.collision(walls, rect, "UP")
        if npcmove[1] == 1:
            rect.x -= speed
            self.collision(walls, rect, "LEFT")
        if npcmove[2] == 1:
            rect.y += speed
            self.collision(walls, rect, "DOWN")
        if npcmove[3] == 1:
            rect.x += speed
            self.collision(walls, rect, "RIGHT")
    
    # Using the mouse we scroll the map, without going away from the player.
    def map_scroll(self, mouse_pos, sw, sh, level_size, cp, blocksize, bx_pos, by_pos):
        if mouse_pos[0] >= (sw - (sw /8)):
            if (bx_pos + level_size[0])  >= sw + blocksize:
                if cp[0] > blocksize: 
                    bx_pos -= 5

        elif mouse_pos[0] <= (sw /8):
            if bx_pos  < -blocksize:
                if cp[0] < (sw - blocksize):
                    bx_pos += 5
            
        elif mouse_pos[1] >= (sh - (sh /8)):
            if (by_pos + level_size[1])  >= sh + blocksize:
                if cp[1] > blocksize:
                    by_pos -= 5
          
        elif mouse_pos[1] <= (sh /8):
            if (by_pos)  < -blocksize:
                if cp[1] < (sh - blocksize):
                    by_pos += 5
                    return bx_pos, by_pos
        return bx_pos, by_pos
    
    
    # A quick and simple level picker
    def next_level(self, playerrect, endzonerect):
        if playerrect.colliderect(endzonerect) == True:
            self.lvlnum += 1 
            self.generate = True
    
    # Below this line we start making the map:
    
    def test_room(self, block):
        testRoom = pygame.Rect(block, block, (block*20), (block*20))
        floor, walls = self.sprite_map(testRoom, block)
        
        return floor, walls
    
     # Generates a room rectangle of random size, and ties the other rects together.      
    def generate_room(self, block, surf, fg, wg):
        run = True
        roomx, roomy = (block*2), (block*20)
        hw = hh = rw = rh = 1000
        rooms = []
        dir = [0, 0, 0, 0]
        room_number = 0
        while run:
           
           hw = random.randrange((block*8), (block*16), block)
           hh = random.randrange((block*8), (block*16), block)
           
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
         
           if rooms != []:
               hall = Room(hw, hh, roomx, roomy, block, fg, wg, room_number)
               rooms.append(hall)
           
           rw = random.randrange((block*16), (block*40), block)
           rh = random.randrange((block*16), (block*40), block)
           
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
           
           room_number += 1     
           room = Room(rw, rh, roomx, roomy, block, fg, wg, room_number)
           rooms.append(room)
           
           roomx, roomy, dir, run = self.direction(room.rect, rooms, block, run, surf)
           
        return rooms
    
    def direction(self, rect, rooms, block, run, surf): #This methods checks each direction to see if there is space for another room there.
        size = surf
        dir = [1, 1, 1, 1]
        if rooms != []:
            if rect.centerx + (block*60) > size[0]: #checking right
                dir[0] = 0 
            else: 
                r, l, u, d = self.room_checker(rect, rooms, block, "right")
                if r == False:
                    dir[0] = 0    
                else:
                    dir[0] = 1
            if rect.centerx - (block*60) < (size[0] - size[0]): #checking left
                dir[1] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "left")
                if l == False:
                    dir[1] = 0
                else:
                    dir[1] = 1
                
            if rect.centery - (block*60) < (size[1] - size[1]): #checking up
                dir[2] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "up")
                if u == False:
                    dir[2] = 0
                else:
                    dir[2] = 1
            if rect.centery + (block*60) > size[1]: #checking down
                dir[3] = 0
            else:
                r, l, u, d = self.room_checker(rect, rooms, block, "down")
                if d == False:
                    dir[3] = 0
                else:
                    dir[3] = 1
        
        print dir    
       # Them we add the required distance to the X/Y coords. (we still need the size of the next Rect for left and up)
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
                if rect.right < i.rect.left: #right
                    if (rect.right + (block*60)) > i.rect.left:
                        if (rect.top + (block*16)) < i.rect.bottom and (rect.bottom + (block*8)) > i.rect.top: 
                                right = False
            if dir == "left":
                if rect.left > i.rect.right: #left
                    if (rect.left - (block*60)) < i.rect.right:
                        if (rect.top + (block*16)) < i.rect.bottom and (rect.bottom + (block*8)) > i.rect.top: 
                                left = False
            
            if dir == "up":
                if rect.top > i.rect.bottom: #up
                    if (rect.top - (block*60)) < i.rect.bottom:
                        if (rect.left - (block*16)) < i.rect.right and (rect.right + (block*8)) > i.rect.left: 
                                up = False
            
            if dir == "down":
                if rect.bottom < i.rect.top: #down
                    if (rect.bottom + (block*60)) > i.rect.top:
                        if (rect.left - (block*16)) < i.rect.right and (rect.right + (block*8)) > i.rect.left: 
                                down = False
            
        return right, left, up, down
    
    
    
    def collision_list(self, walls, floors):
        wall_list = walls
        for room in floors:
            for i in room:
                for rooms in wall_list:
                    for r in rooms:
                        if r.rect.colliderect(i) == True:
                            rooms.remove(r)
        return wall_list
                  
    
    
    def map_generate_old(self, lvlnum, lvlfile, blocksize, player_rect):
        if self.generate == True:
            if lvlnum == 1:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[0], blocksize, blocksize)
                player_rect.x = self.start_rect.x
                player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
                
            elif lvlnum == 2:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[1], blocksize, blocksize)
                player_rect.x = self.start_rect.x
                player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
                
            elif lvlnum == 3:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[2], blocksize, blocksize)
                player_rect.x = self.start_rect.x
                player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
               
                
            elif lvlnum == 4:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[3], blocksize, blocksize)
                player_rect.x = self.start_rect.x
                player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
                
                
            elif lvlnum == 5:
                self.walls, self.end_rect, self.space, self.start_rect = self.draw_map(lvlfile[4], blocksize, blocksize)
                player_rect.x = self.start_rect.x
                player_rect.y = self.start_rect.y
                
                self.bx_pos = - self.start_rect.x + (self.w/2)
                self.by_pos = - self.start_rect.y + (self.h/2)
                self.generate = False
    
    
    # Here we draw the map based on the Text files.
    def draw_map_old(self, map, w, h):
        walls = []
        space = []   
        x = -w
        y = 0
        for row in map:
            for col in row:
                if col == "W":
                    thatwall = pygame.Rect(x, y, w, h)
                    walls.append(thatwall)
                elif col == ".":
                    thatspace = pygame.Rect(x, y, w, h)
                    space.append(thatspace)
                elif col == "E":
                    end_rect = pygame.Rect(x, y, w, h)
                elif col == "S":
                    start_rect = pygame.Rect(x, y, w, h)
                x += w
            y += h
            x = -w
        
        return walls, end_rect, space, start_rect 
    
             
   
    
        
            
        
