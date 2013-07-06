"""
A Pygame Engine.
Can be used to run any Tile based 2d Pygame game.
"""

import os, sys
import pygame
from pygame.locals import *

class Engine(object):
    """The mainloop class for a Pygame"""
    def __init__(self, size=(640,480)):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.dt = 0.0

    def main_loop(self, fps=0):
        while True:
            pygame.display.set_caption("Infinite Adventure. FPS: %i" % self.clock.get_fps())
            self.event_handler()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)
            timer = self.clock.get_rawtime()
            self.dt += float(timer)/1000
 			
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

    
    def update(self): 
        pass
    
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

class Tile(pygame.sprite.DirtySprite):
    """The class used to make the Tiles for walls and floors"""
    def __init__(self, img, pos, number):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.number = number