"""
An implementation of the A* pathfinding algorithm for Pygame
"""

import random
import pygame
import numpy as np
from vec2d import vec2d

class Pathfinding(object):
    """A* Path finding implementation for Pygame
        The tiles argument is a list or group of floor tiles
        with self.rect values attached. Block is the pixel size of your tiles
    """
    def __init__(self, tiles, block=32):
        self.block = block
        self.tilelist = []
        self._make_array(tiles)
        self.array_old = self.tilearray.copy()
        self.re_inst()

    def re_inst(self):
        self.nodes = {}
        self.closed_nodes = {}

    def target_is(self, target):
        self.target = (int(round(target[1]/32)), int(round(target[0]/32)))
        size = self.tilearray.shape
        xy_step = max([size[0] - self.target[0], self.target[0],
                        size[1] - self.target[1], self.target[1]])
        for step in xrange(xy_step):
            self._add2square(self.target, xy_step)
            xy_step -= 1
        self.tilearray[self.wallarray] = 0

    def find(self, start, time=500):
        start = (int(round(start[1]/32)), int(round(start[0]/32)))
        self._make_node(start, 0, "start")
        self._setup_nodes(start)
        self._close_node(start)
        ct = 0
        while True:
            node = self._find_next()
            if node == None:
                print "Target is unreachable"
                return None
                break
            elif node == self.target:
                print "FOUND"
                return self._make_path_list(node)
                break
            self._close_node(node)
            self._setup_nodes(node)
            if ct > time:
                print "TIME OUT!"
                return None
                break
            ct += 1

    def _make_array(self, tiles):
        for tile in tiles:
            tile = (int(round(tile.rect.x / self.block)), int(round(tile.rect.y / self.block)))
            self.tilelist.append(tile)
        size = self.tilelist[-1]
        size = size[1] + 3, size[0] + 2
        self.tilearray = np.ones(size, dtype=np.int16)
        for i in self.tilelist:
            self.tilearray[i[1]+1,i[0]] = 0
        self.wallarray = np.nonzero(self.tilearray)

    def _setup_nodes(self, pos):
        straight = []
        diagonal = []
        straight.append((pos[0], pos[1]-1))
        straight.append((pos[0], pos[1]+1))
        straight.append((pos[0]-1, pos[1]))
        straight.append((pos[0]+1, pos[1]))
        diagonal.append((pos[0]+1, pos[1]-1))
        diagonal.append((pos[0]-1, pos[1]-1))
        diagonal.append((pos[0]+1, pos[1]+1))
        diagonal.append((pos[0]-1, pos[1]+1))
        for direction in straight:
            self._make_node(direction, 10, pos)
        for direction in diagonal:
            self._make_node(direction, 14, pos)


    def _add2square(self, pos, step):
        left = pos[1] - step
        right = pos[1] + step + 1
        top = pos[0] - step
        bottom = pos[0] + step + 1
        if top < 0:
            top = 0
        if left < 0:
            left = 0
        self.tilearray[top:bottom, left:right] = step

    def _make_node(self, pos, h, parent):
        state = None
        if pos not in self.closed_nodes.keys():
            g = self.tilearray[pos[0], pos[1]]
            if g == 0:
                state = "wall"
            self.nodes[pos] = {"state":state,
                               "f_score":h+g,
                               "parent":parent}

    def _close_node(self, pos):
        self.closed_nodes[pos] = self.nodes[pos]["parent"]
        self.nodes.pop(pos)

    def _find_next(self):
        score = {"f_score":10000}
        x = None
        for key in self.nodes.keys():
            if self.nodes[key]["f_score"] < score["f_score"]:
                if self.nodes[key]["state"] != "wall":
                    score["f_score"] = self.nodes[key]["f_score"]
                    x = key
        return x

    def _make_path_list(self, node):
        pathlist = []
        while True:
            pathlist.append(node)
            if node in self.nodes.keys():
                node = self.nodes[node]["parent"]
            elif node in self.closed_nodes.keys():
                node = self.closed_nodes[node]
            elif node == "start":
                break
        actual_pl = []
        for tup in pathlist:
                if tup != "start":
                    tup = (tup[1]*self.block + self.block, tup[0]*self.block)
                    actual_pl.insert(0, tup)
        return actual_pl
