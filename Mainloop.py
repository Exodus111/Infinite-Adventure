'''
Created on Dec 29, 2012

@author: aurelio
'''

# This file can be used as a base for pretty much any Pygame based game (except for the Wall class)


import pygame, math, sys, os
from pygame.locals import *

# First we intialize pygame and set up a few class variables.
class GameState(object):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):   
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(fill)
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
            # pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
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
             
    def draw_map(self, map, w, h):
        walls = []   
        x = y = 0
        for row in map:
            for col in row:
                if col == "W":
                    thatwall = pygame.Rect(x, y, w, h)
                    walls.append(thatwall)                    
                elif col == "E":
                    end_rect = pygame.Rect(x, y, w, h)
                x += 16
            y += 16
            x = 0
        
        return walls, end_rect 
    
        
            
        
