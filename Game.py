#!/usr/bin/env Python
"""
The Game file.
This is where the game mechanics will go, this file runs the game
and puts all the pieces together.
"""

import pygame, vec2d
from pygame.locals import *
from vec2d import vec2d
from Engine import *
from Entity import *
from Levelgen import *

fps = 60

class Game(Engine):
    """Infinite Adventure"""
    def __init__(self):
        self.size = (1024, 960)
        Engine.__init__(self, self.size)
        self.player = Player("images/player.png", (100, 100), (0, 0))
        self.mobgroup = pygame.sprite.LayeredDirty()
        self.mobgroup.add(self.player)
        self.tile_imgs = [line.strip() for line in open("data/tiles.txt")]
        self.npc_imgs = [line.strip() for line in open("data/npcs.txt")]
        self.level = Levelgen(self.tile_imgs)
        self.floor, self.walls = self.level.test_lvl((20, 25), 32)


    def update(self):
        self.mobgroup.update(self.walls, self.dt)
    def draw(self): 
        self.floor.draw(self.screen)
        self.walls.draw(self.screen)
        self.mobgroup.draw(self.screen)

    def user_event(self, event):
        pass
    
    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player.arrows[0] = 1
        if key in (K_a, K_LEFT):
            self.player.arrows[1] = 1
        if key in (K_s, K_DOWN):
            self.player.arrows[2] = 1
        if key in (K_d, K_RIGHT):
            self.player.arrows[3] = 1
        if key == K_ESCAPE:
            pygame.quit()
    
    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player.arrows[0] = 0
        if key in (K_a, K_LEFT):
            self.player.arrows[1] = 0
        if key in (K_s, K_DOWN):
            self.player.arrows[2] = 0
        if key in (K_d, K_RIGHT):
            self.player.arrows[3] = 0
    
    def mouse_down(self, button, pos):
        pass
    
    def mouse_up(self, button, pos):
        pass
    
    def mouse_motion(self, buttons, pos, rel):
        pass


s = Game()
s.main_loop(fps)

		
