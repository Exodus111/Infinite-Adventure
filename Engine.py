"""
2.0
A Pygame Engine.
Can be used to run any Tile based 2d Pygame game.
"""

import os, sys
import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d

class Engine(object):
    """The mainloop class for a Pygame"""
    def __init__(self, name, size=(640,480), mouseset=True):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.mouse.set_visible(mouseset)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.name = name
        self.running = True
        self.dt = 0.0

    def main_loop(self, fps=0):
        while self.running:
            pygame.display.set_caption("{} FPS: {}".format(self.name, int(self.clock.get_fps())))
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

class Surfaces(object):
    """Surface Matrice class for Pygame Surfaces"""
    def __init__(self, size, screen_size, amount=1):
        self.size = size
        self.screen_size = screen_size
        self.screen_center = (screen_size[0]/2, screen_size[1]/2)
        self.amount = amount
        self._generate_surfaces()
        self.var = 1


    def _generate_surfaces(self):
        if self.amount == 1:
            self.surface = pygame.Surface(self.size)
            self.rect = self.surface.get_rect()
        elif self.amount == 4:
            pass
        elif self.amount == 8:
            pass

    def update_surface(self, pos, speed):
        if self.amount == 1:
            centerv = vec2d(self.screen_center[0] - self.rect.x,
                            self.screen_center[1] - self.rect.y)
            playerv = vec2d(pos)
            distance = centerv.get_distance(playerv)
            if distance >= 50:
                surfv = vec2d(self.rect.topleft)
                move = playerv - centerv
                move.length = speed *(distance/50)
                surfv -= move
                self.rect.topleft = surfv.inttup()
            if self.rect.x > 0:
                self.rect.x = 0
            if self.rect.y > 0:
                self.rect.y = 0
            elif self.amount == 4:
                pass
            elif self.amount == 8:
                pass

"""
This part isn't working right.
            elif mousepos[0] > (self.screen_center[0] - 30):
                print "Moving Left"
                self.rect.x -= 15
            elif mousepos[0] < 30:
                print "Moving Right"
                self.rect.x += 15
            elif mousepos[1] > (self.screen_center[1] - 30):
                print "Moving Down"
                self.rect.y -= 15
            elif mousepos[1] < 30:
                print "Moving Up"
                self.rect.y += 15
"""




