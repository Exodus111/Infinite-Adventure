'''
Created on Dec 29, 2012

@author: aurelio
'''

# This file can be used as a base for pretty much any Pygame based game (except for the Wall class)


import pygame, math, sys, os
from pygame.locals import *

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
            pygame.display.flip()
            self.clock.tick(fps)
            
            
# Rotates any object, to face any other object.        
    def rotate(self, pos1, pos2):  
        angle = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        angle = angle * (180/ math.pi)
        angle = (angle) % 360
        return angle
    
    def rotate_image(self, image, angle):
        img_rect = image.get_rect()
        img_rotd = pygame.transform.rotate(image, angle)
        img_rect.center = img_rotd.get_rect().center
        img_rotd = img_rotd.subsurface(img_rect).copy()
        return img_rotd
    
# This function is also run in the mainloop, lots of code will go here, but mostly in child classes.
    def update(self): 
        pass
    
# This function is also called by the main loop, and will also mostly be run by child classes.
    def draw(self): 
        pass
    
    
    def player_move(self, dir, screenpos, screensize, walls, player_rect, player_speed):
        if dir[0] == 1:
            if screenpos[1] > (screensize[1]/50):    
                player_rect.y -= player_speed
                self.collision(walls, player_rect, "UP")
        if dir[1] == 1:
            if screenpos[0] > (screensize[0]/50):
                player_rect.x -= player_speed
                self.collision(walls, player_rect, "LEFT")
        if dir[2] == 1:
            if screenpos[1] < (screensize[1] - (screensize[1]/50)):
                player_rect.y += player_speed
                self.collision(walls, player_rect, "DOWN")
        if dir[3] == 1:
            if screenpos[0] < (screensize[0] - (screensize[0]/50)):
                player_rect.x += player_speed
                self.collision(walls, player_rect, "RIGHT")
    
# Rectangle based collision detection. Requires a list of all rectangles to check collision on, 
# the rect object to check and a string for collision.
    def collision(self, walls, rect, direction):
        for wall in walls:
            if rect.colliderect(wall):
                if direction == "UP":
                    rect.top = wall.bottom
                if direction == "LEFT":
                    rect.left = wall.right
                if direction == "DOWN":
                    rect.bottom = wall.top
                if direction == "RIGHT":
                    rect.right = wall.left
                    
    # We are using two surfaces, one for the screen and one for the map (so I can scroll the game)
        # So I needed a method to find the location of an object on the surface to screen.
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
    
    
    def next_level(self, playerrect, endzonerect):
        if playerrect.colliderect(endzonerect) == True:
            self.lvlnum += 1 
            self.generate = True
    
    def map_generate(self, lvlnum, lvlfile, blocksize, player_rect):
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
    
    
    def draw_map(self, map, w, h):
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
             
   
    
        
            
        
