"""
This file handles the NPC behavior
"""

import random
from vec2d import vec2d
from raycasting import Raycasting as Ray

class Behavior(object):
    """Behavior class for NPCs"""
    conversations = {}
    def __init__(self, mob, faction=1):
        self.faction = faction
        self.stats = {}
        self.timers = {}
        self.direction = vec2d(0,0)
        self.directions = {}
        self.path = []
        self.mob = mob
        self.mobgroups = mob.groups()
        self.target = None
        self.dt = 0.0

    def timer(self, name, delay):
        if name not in self.timers.keys():
            self.timers[name] = 0.0
        if self.timers[name] < self.dt:
            self.timers[name] = self.dt + delay
            return True
        else:
            return False

    def update(self, dt):
        self.dt = dt
        self.patrol()
        #self.wall_check()

    def wall_check(self):
        if self.timer("wallchk", 3):
            self.directions = self.look_around(self.mob.pos.inttup(), 32)
            for key in self.directions:
                card = self.directions[key]
                if card != []:
                    if key == "north":
                        self.mob.dir.y *= -1
                    elif key == "south":
                        self.mob.dir.y *= -1
                    if key == "east":
                        self.mob.dir.x *= -1
                    elif key == "west":
                        self.mob.dir.x *= -1

    def look_for_enemy(self):
        if self.faction == 1:
            for npc in self.grouplist:
                if npc.type == "player":
                    self.target = npc

    def look_around(self, pos, dist):
        ray = Ray(pos, (1,1))
        col_sphere = ray.checklength(self.mob.collision.current_quad)
        if col_sphere < 80:
            westpoint = (pos[0] - dist, pos[1])
            west = self._raycast(pos, westpoint)
            eastpoint = (pos[0] + dist, pos[1])
            east = self._raycast(pos, eastpoint)
            southpoint = (pos[0], pos[1] + dist)
            south = self._raycast(pos, southpoint)
            northpoint = (pos[0], pos[1] - dist)
            north = self._raycast(pos, northpoint)
            col_sphere = False
            return {"west":west, "east":east, "south":south, "north":north}
        else:
            return {}

    def _raycast(self, pos, tar):
        ray = Ray(pos, tar)
        return ray.cast(self.mob.collision.current_floor.walls, 5)

    def patrol(self):
        if self.timer("patrol", 5) or self.mob.collided:
            if self.path == [] or self.mob.collided:
                self.path = []
                pos = self.mob.pos
                self.path.append(pos.inttup())
                for step in xrange(5, 15):
                    while True:
                        self.direction.x = random.randrange(-1, 2)
                        self.direction.y = random.randrange(-1, 2)
                        if self.direction.inttup() != (0,0):
                            break
                    self.direction.length = random.randint(100, 400)
                    pos = pos + self.direction
                    self.path.append(pos.inttup())
        self.move_path()

    def move_path(self):
        if self.path != []:
            step = vec2d(self.path[0])
            dist = self.mob.pos.get_distance(step)
            if dist < 5:
                if len(self.path) > 1:
                    self.mob.move_to(self.path[1])
                self.path.pop(0)






