'''
Created on Dec 29, 2012

@author: aurelio
'''

# This file can be used as a base for pretty much any Pygame based game (except for the Wall class)


import pygame, math, sys, os, random
from pygame.locals import *
from vec2d import vec2d
from Entities import *

# First we intialize pygame and set up a few class variables.
class Engine(object):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):   
        os.environ["SDL_VIDEO_CENTERED"] = "2"
        pygame.init()
        pygame.mouse.set_visible(False)      
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = False
        self.start = True
        self.surf_dir = [False, False, False, False]
        self.temp_pos = (0,0)
        self.delta_time = 0.0
        
     
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
            elif event.type == USEREVENT:
                self.user_event(event)
        
#The mainloop runs the game, nothing that is not in here will run.
    def main_loop(self, fps=0):
        delta = 0.0 
        self.running = True
        
        while self.running:
            pygame.display.set_caption("Infinite Adventure. FPS: %i" % self.clock.get_fps())
            self.event_handler()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)
            timer = self.clock.get_rawtime()
            delta += float(timer)/1000
            self.delta_time = delta
            
    
# This function is also run in the mainloop, lots of code will go here, but mostly in child classes.
    def update(self): 
        pass
    
# This function is also called by the main loop, and will also mostly be run by child classes.
    def draw(self): 
        pass

    def user_event(self, event):
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
    
    
    # Rotates any object, to face any other object.        
    def rotate(self, pos1, pos2):  
        angle = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        angle = angle * (180/ math.pi)
        angle = (angle) % 360
        angle += 90
        return angle
   
   # Pygame rotation messes up images, this keeps em in line. 
    def rotate_image(self, image, angle):
        img_rect = image.get_rect()
        img_rotd = pygame.transform.rotate(image, angle)
        img_rect.center = img_rotd.get_rect().center
        img_rotd = img_rotd.subsurface(img_rect).copy()
        return img_rotd
                    
   
    def limit_rooms(self, rooms, screen):
        self.r_rooms = []
        for i in rooms:
            if screen.colliderect(i.rect):
                sprites = []
                for wall in i.walls:
                    sprites.append(wall)
                for floor in i.tiles:
                    sprites.append(floor)
                for sprite in sprites:
                    if screen.colliderect(sprite.rect):
                        self.r_rooms.append(sprite)

    def limit_mobs(self, screen, mobs):
        l_mobs = []
        for mob in mobs:
            if screen.colliderect(mob.rect):
                l_mobs.append(mob)
        return l_mobs                
    
    def add_rooms(self):
        all = pygame.sprite.LayeredDirty()
        for sprite in self.r_rooms:
            all.add(sprite)
        return all    
                   
    # We are using two surfaces, one for the screen and one for the map (so I can scroll the game)
        # So I needed a method to find the location of an object on the background surface to the screen surface.
        # px, py are coords for the object on the surface, and mx, my are the coords for the surface location on the screen.
    def find_position(self, px, py, mx, my):
    
        pos_x = px + mx
        pos_y = py + my

        return pos_x, pos_y
   
    # Using the mouse we scroll the map, without going away from the player.
    def map_scroll(self, mouse_pos, sw, sh):

 
        if mouse_pos[0] >= (sw - (sw /8)):#Moving Right
            self.surf_dir[1] = True
            
        elif mouse_pos[0] <= (sw /8):#Moving Left
            self.surf_dir[3] = True
         
        elif mouse_pos[1] >= (sh - (sh /8)):#Moving Down
            self.surf_dir[0] = True
            
        elif mouse_pos[1] <= (sh /8):#Moving Up
            self.surf_dir[2] = True
        
        else:
            self.center_map()


    def center_map(self):
        self.surf_dir = [False, False, False, False]


            

    def map_move(self, surf, cp, sw, sh):

        if self.surf_dir[1] == True:
            if surf.rect.x > (-surf.levelsize[0] + sw):
                if 0 < cp.x:
                    surf.rect.move_ip(-15, 0) #Moving Right
            elif surf.rect.x < (-surf.levelsize[0] + sw):
                surf.rect.x = (-surf.levelsize[0] + sw)

        if self.surf_dir[3] == True:
            if surf.rect.x < 0:
                if sw > cp.x:
                    surf.rect.move_ip(15, 0) #Moving Left
            elif surf.rect.x > 0:
                surf.rect.x = 0

        if self.surf_dir[0] == True:
            if surf.rect.y > (-surf.levelsize[1] + sh):
                if 0 < cp.y:
                    surf.rect.move_ip(0, -15) #Moving Down
                elif surf.rect.y < (-surf.levelsize[1] + sh):
                    surf.rect.y = (-surf.levelsize[1] + sh)
        if self.surf_dir[2] == True:
            if surf.rect.y < 0:
                if sh > cp.y:
                    surf.rect.move_ip(0, 15) #Moving Up
            elif surf.rect.y > 0:
                surf.rect.y = 0
            
            
    
    def set_rooms(self, rooms, player, bx, by, cp, w, h):
        FirstRoom = rooms[0]
        LastRoom = rooms[-1]
        
        f_room = []
        for i in FirstRoom.tiles:
            f_room.append((i.rect.centerx, i.rect.centery))
            
        len_froom = len(f_room)
        player.rect.centerx, player.rect.centery = f_room[random.randint(0, len_froom)]
        cp.centerx, cp.centery = self.find_position(player.rect.x, player.rect.y, bx, by)

        bx = (w/2) - cp.x
        by = (h/2) - cp.y

        return bx, by


    def add_mobs(self, num, rooms, p_lvl, surf):
        mobslist = pygame.sprite.LayeredDirty()
        for i in rooms:
            if i == rooms[0]:
                pass
            elif i.ident == "ROOM":
                temp = self.generate_mobs(num, i.rect, p_lvl, surf)
                mobslist.add(temp)
        return mobslist

    def generate_mobs(self, num, rect, p_lvl, surf):
        mobgroup = []
        for i in xrange(num):
            i = Mob((random.randint(rect.left, rect.right), random.randint(rect.top, rect.bottom)), 
                    (random.choice([-1, 1]), random.choice([-1, 1])), p_lvl)
            i.select(random.randint(1, 6))
            i.upgrade(random.randint(1, 5))
            i.bg = surf
            mobgroup.append(i)
        return mobgroup
    
    # A quick and simple level picker
    def next_level(self, playerrect, endzonerect):
        if playerrect.colliderect(endzonerect) == True:
            self.lvlnum += 1 
            self.generate = True

    
    # Below this line we start making the map:
    
    
     # Generates a room rectangle of random size, and ties the other rects together.      
    def generate_room(self, block, surf):
        fg = pygame.sprite.LayeredDirty()
        wg = pygame.sprite.LayeredDirty()
        run = True
        roomx, roomy = (block*2), (block*20)
        hw = hh = rw = rh = 266
        rooms = []
        dir = [0, 0, 0, 0]
        room_number = 0
        while run:
           
           hw = random.randrange((block*10), (block*20), block)
           hh = random.randrange((block*10), (block*20), block)
           
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
               hall = Room(hw, hh, roomx, roomy, block, fg, wg, room_number, "HALL")
               rooms.append(hall)
           
           rw = random.randrange((block*10), (block*28), block)
           rh = random.randrange((block*10), (block*28), block)
           
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
           room = Room(rw, rh, roomx, roomy, block, fg, wg, room_number, "ROOM")
           rooms.append(room)
           
           roomx, roomy, dir, run = self.direction(room.rect, rooms, block, run, surf)
        
        pygame.sprite.groupcollide(wg, fg, True, False)
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
    
             
   
    
        
            
        
