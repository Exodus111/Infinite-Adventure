"""
A test program for my pathfinding module
"""

import pygame
from pygame.locals import *

from pathfinding import *
from Engine import *
from vec2d import vec2d

fps = 60

class PathTest(Engine):
    """Testclass for pathfinding"""
    def __init__(self):
        self.size = (1024, 960)
        super(PathTest, self).__init__("Pathtest", self.size)
        self.tile_imgs = [line.strip() for line in open("data/tiles.txt")]
        self.npc_imgs = [line.strip() for line in open("data/npcs.txt")]
        self.map = [line.strip() for line in open("data/map.txt")]
        self.block = 32
        self.floortiles = pygame.sprite.LayeredDirty()
        self.tilegroup = self.make_room()
        self.player = Entity(self.npc_imgs[0])
        self.target = Entity(self.npc_imgs[1])
        self.mobgroup = pygame.sprite.LayeredDirty()
        self.path = Pathfinding(self.floortiles, self.block)
        self.path_list = None
        self.space = False

    def make_room(self):
        tilegroup = pygame.sprite.LayeredDirty()
        x = y = num = 0
        for line in self.map:
            for letter in line:
                if letter == "W":
                    tile = Tile(self.tile_imgs[0], (x,y), num)
                elif letter == "F":
                    tile = Tile(self.tile_imgs[1], (x,y), num)
                    self.floortiles.add(tile)
                tilegroup.add(tile)
                x += self.block
                num += 1
            x = 0
            y += self.block

        return tilegroup

    def update(self):
        if self.player.pos != None:
            self.mobgroup.add(self.player)
        if self.target.pos != None:
            self.mobgroup.add(self.target)


    def draw(self):
        self.tilegroup.draw(self.screen)
        if len(self.mobgroup) > 0:
            self.mobgroup.draw(self.screen)
        if self.path_list != None:
            pygame.draw.lines(self.screen, (255, 255, 255), False, self.path_list)


    def key_down(self, key):
        if key == K_ESCAPE:
            self.running = False
        if key == K_SPACE:
            if self.space == False:
                self.space = True
                self.path_list = self.path.find(self.player.pos)
            elif self.space:
                self.space = False
                self.path.tilearray = self.path.array_old
                self.path.re_inst()
                self.path_list = None

    def mouse_down(self, button, pos):
        if button == 1:
            self.player.position(pos)
        elif button == 3:
            print pos
            self.target.position(pos)
            self.path.target_is(pos)

class Entity(pygame.sprite.DirtySprite):
    """The Entity class for both entities"""
    def __init__(self, img):
        super(Entity, self).__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.dirty = 2
        self.pos = None

    def position(self, pos):
        self.pos = pos
        self.rect.center = self.pos


s = PathTest()
s.main_loop(fps)
