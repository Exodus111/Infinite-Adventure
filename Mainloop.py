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
        space = []   
        x = -w
        y = 0
        for row in map:
            for col in row:
                if col == "W":
                    thatwall = pygame.Rect(x, y, w, h)
                    walls.append(thatwall)
                elif col == "S":
                    thatspace = pygame.Rect(x, y, w, h)
                    space.append(thatspace)
                elif col == "E":
                    end_rect = pygame.Rect(x, y, w, h)
                x += w
            y += h
            x = -w
        
        return walls, end_rect, space 
    
        
            
        
