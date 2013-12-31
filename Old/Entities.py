'''
Created on Jan 19, 2013

@author: aurelio
'''
import pygame, random
from pygame.locals import *
from vec2d import vec2d
import Mainloop

class Entity(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.rooms = "rooms"
        self.state = "NORMAL"
        self.shout = pygame.font.SysFont("arial", 15)
        self.speech = "What ..?"

    def health_bar(self, pos, health):
        health_bar_x = pos.x - 7
        health_bar_y = pos.y - self.image_h / 2 - 6
        self.screen.fill(pygame.Color("red"), 
                            (health_bar_x, health_bar_y, 15, 4))
        self.screen.fill(pygame.Color("green"), 
                            (health_bar_x, health_bar_y, self.health, 4))

    def feared(timer, dt):
        pass


    def movement(self):
        pass

    def set_collide(self, rooms):
        self.rooms = rooms

    def collision(self, sprite, direction):
        
        for i in self.rooms:
            if sprite.rect.colliderect(i.rect) == True:
                for wall in i.walls:
                    if sprite.rect.colliderect(wall.rect) == True:
                        if direction == "UP":
                            sprite.rect.top = wall.rect.bottom
                        if direction == "LEFT":
                            sprite.rect.left = wall.rect.right
                        if direction == "DOWN":
                            sprite.rect.bottom = wall.rect.top
                        if direction == "RIGHT":
                            sprite.rect.right = wall.rect.left
                        if sprite.ident == "Player":
                            if wall.ident == "Exit":
                                sprite.nextlevel = True

    def shout_spell(self, spell):
        self.mssg = self.shout.render(spell, True, (255, 255, 0))
        self.cast_time = self.time + 1.0
        self.state = "SHOUTING"

        

class Player(Entity):  
    # Here I load up the player, and the variables necessary for movement and rotation.
    def __init__(self):
        Entity.__init__(self)
        # Sprite info
        self.dirty = 1
        self.image = pygame.image.load("player.png").convert_alpha()
        self.base_img = self.image
        self.rect = self.image.get_rect()
        
        # Movement info
        self.pos = vec2d(0,0)
        self.rot = 0
        self.speed = 15
        self.dir = [0, 0, 0, 0]
        self.nextlevel = False

        # Player info
        self.ident = "Player"
        self.xp = 0
        self.level = 1

        # HP and Mana
        self.hp = self.level * 100
        self.mana = self.level * 100
        self.max_hp = self.level * 100
        self.max_mana = self.level * 100

        # Timers
        self.time = 0.0
        self.mana_timer = 0.0
        self.health_timer = 0.0
        self.dmg_timer = 0.0
        self.cast_time = 0.0


    def drink_potion(self, potions):
        for pot in potions:
            if pot.rect.colliderect(self.rect):
                print "Potion picked up"
                
                if pot.name == "Health Potion":
                    self.hp += pot.strength
                elif pot.name == "Mana Potion":
                    self.mana += pot.strength
                elif pot.name == "Power Potion":
                    pass

    def level_init(self):
        self.leveldict = {}
        lvl = self.level
        req_xp = 100 * 2**(lvl - 1)

        for i in xrange(20):
            a = lvl
            b = req_xp
            self.leveldict[a] = b
            lvl += 1
            req_xp *= 2

    def check_lvl(self):
        current_xp = self.xp
        current_lvl = self.level
        temp_lvl = 0
        for i in self.leveldict:
            if current_xp > self.leveldict[i]:
                temp_lvl = i + 1
        if temp_lvl > current_lvl:
            self.upgrade(temp_lvl)
            self.level_init()

    def upgrade(self, lvl):
        dif = lvl - self.level
        if dif == 0:
            pass
        else:
            print "Congratualtions, you have leveled up"
            print "You are now level: ", lvl
            self.level = lvl
            self.max_hp += (dif * 100 * 0.2)
            self.max_mana += (dif * 100 * 0.3)
            self.hp = self.max_hp
            self.mana = self.max_mana
        

    def update(self, time):
        self.time = time
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery
        self.mssg_rect = (self.rect.x - 15, self.rect.y - 15)
        if self.state == "SHOUTING":
            if self.cast_time < self.time:
                self.state = "NORMAL"
        if self.hp <= 0:
            print "You are DEAD!"
            self.state = "DEAD"
            self.kill()
        self.regen()

    def regen(self):
        if self.mana < self.max_mana:
            if self.mana_timer < self.time:
                self.mana_timer = self.time + 1.0
                self.mana += 1
        if self.hp < self.max_hp:
            if self.health_timer < self.time:
                self.health_timer = self.time + 5.0
                self.hp += 1   


    def damage(self, dmg):
        if self.dmg_timer < self.time:
            self.hp -= dmg
            print "You where hit for", dmg
            self.dmg_timer = self.time + 1.0



    # Movement and collision detection calls for the player 
    def move(self, dir, screenpos, screensize):
        if dir[0] == 1:
            if screenpos[1] > (screensize[1]/50):    
                self.rect.y -= self.speed
                self.collision(self, "UP")
        if dir[1] == 1:
            if screenpos[0] > (screensize[0]/50):
                self.rect.x -= self.speed
                self.collision(self, "LEFT")
        if dir[2] == 1:
            if screenpos[1] < (screensize[1] - (screensize[1]/50)):
                self.rect.y += self.speed
                self.collision(self, "DOWN")
        if dir[3] == 1:
            if screenpos[0] < (screensize[0] - (screensize[0]/50)):
                self.rect.x += self.speed
                self.collision(self, "RIGHT")
                


class Mob(Entity):
    def __init__(self, init_pos, init_dir, player):
        Entity.__init__(self)
        self.dirty = 1
        self.player_pos = player.pos
        self.bg = None
        self.npcmove = [0, 0, 0, 0]
        self.ident = "Mob"
        self.pos = vec2d(init_pos)
        self.pos_old = self.pos
        self.dir = vec2d(init_dir).normalized()
        self.room = 0
        self.walls = None
        self.npcmove = [0,0,0,0]
        self.counter = 0
        self.lvl = 1
        self.max_hp = self.lvl * 100
        self.hp = self.max_hp
        self.time = 0
        self.xp = 25
        self.dot_effect = False

        # Speech stuff
        self.speech_timer = 0
        self.speech_hurt = ["Ouch!", "AAAHG!", "You Bastard! That hurt", "What the...!"]


    def upgrade(self, lvl):
        dif = lvl - self.lvl
        if dif != 0:
            self.lvl = lvl
            self.max_hp += (dif * 100 * 0.2)
            self.hp = self.max_hp
            self.xp = 25 * 2**(self.lvl - 1)

    def shouting(self):
        if self.speech == "dmg":
            speech = random.choice(self.speech_hurt)
            self.mssg = self.shout.render(speech, True, (255, 255, 0))
            self.speech_timer = self.time + 1.0
            self.state = "SHOUTING"
            self.speech = None

        if self.speech_timer <= self.time:
            if self.speech_timer != 0:
                self.state = "NORMAL"
                self.speech_timer = 0


    def update(self, time):
        self.time = time
        self.mssg_rect = (self.rect.x - 32, self.rect.y - 20)
        self.text = [self.name, "Level: %s" % (self.lvl), "Speed: %s" % (self.speed), self.intelligence]
        self.shouting()
        

    def select_stage(self, player):
        playerlevel = player.level

        if playerlevel <= 1:
            num = 1
            self.select_mob(num)
        elif playerlevel == 2:
            num = 1
            self.select_mob(num)

        elif playerlevel == 3:
            num = 1
            self.select_mob(num)

        elif playerlevel == 4:
            num = 1
            self.select_mob(num)

        elif playerlevel >= 5:
            num = 1
            self.select_mob(num)

    def select_mob(self, num):  
        if num == 1:
            self.image = pygame.image.load("mob_green.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 3
            self.num = num
            self.name = "Green Mob"
            self.intelligence = "This mob is pretty stupid."
            self.rotate_img()
        elif num == 2:
            self.image = pygame.image.load("mob_red.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 3
            self.num = num
            self.name = "Red Mob"
            self.intelligence = "This mob is of average intelligence."
            self.rotate_img()
        elif num == 3:
            self.image = pygame.image.load("mob_yellow.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 3
            self.num = num
            self.name = "Yellow Mob"
            self.intelligence = "This mob is intelligent."
            self.rotate_img()
        elif num == 4:
            self.image = pygame.image.load("mob_orange.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 3
            self.num = num
            self.name = "Orange Mob"
            self.intelligence = "This mob is really smart."
            self.rotate_img()
        elif num == 5:
            self.image = pygame.image.load("mob_pink.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 5
            self.num = num
            self.name = "Pink Mob"
            self.intelligence = "This mob is a genius."
            self.rotate_img()
        elif num == 6:
            self.image = pygame.image.load("mob_white.png").convert_alpha()
            self.base_image = self.image
            self.rect = self.image.get_bounding_rect()
            self.rect.center = self.pos.inttup()
            self.speed = 5
            self.num = num
            self.name = "White Mob"
            self.intelligence = "This mob is unfathomable."
            self.rotate_img()

    def damage(self, dmg):
        min_d = int(dmg[0])
        max_d = int(dmg[1])
        dmg_taken = random.randint(min_d, max_d)
        self.hp -= dmg_taken
        self.speech = "dmg"

    def dotted(self, dmg, start, stop):
        self.damage(dmg)
        self.dot_effect = True
        self.dotdmg = dmg
        self.dotter = start + 1
        self.dotstop = stop



    def move(self, dt):
        self.rect.center = self.pos.inttup()

        if self.dot_effect == True:
            if dt >= self.dotter:
                self.damage(self.dotdmg)
                if self.dotter <= self.dotstop:
                    self.dotter += 1
                else:
                    self.dot_effect = False


    def health_bar(self):
        self.health = int(30 / self.max_hp * self.hp)
        health_bar_x = self.pos.x - 15
        health_bar_y = self.pos.y - 15
        if (self.lvl * 100) != self.hp:
            redbar = pygame.Rect(health_bar_x, health_bar_y, 30, 4)
            greenbar = pygame.Rect(health_bar_x, health_bar_y, self.health, 4)
        else:
            redbar = pygame.Rect(0, 0, 0, 0)
            greenbar = pygame.Rect(0, 0, 0, 0)

        return redbar, greenbar 

    def run(self, rooms, mobs, player, dt):
        self.dirty = 1
        self.player = player
        if self.hp <= 0:
            player.xp += self.xp
            player.check_lvl()
            self.state = "DEAD"
            self.kill()
        for room in rooms:
            if self.rect.colliderect(room.rect):
                self.room = room
        self.patrol()
        self.collide()
        self.move(dt)
        #self.track()
        self.collide_other(mobs)
        self.collide_player()
        

    def collide(self):
        for wall in self.room.walls:
            if self.rect.colliderect(wall):
                shove = vec2d(wall.rect.center) - self.pos
                shove.length = self.speed
                self.pos -= shove
                self.dir.x *= -1
                self.dir.y *= -1
                self.rotate_img()

    def collide_other(self, mobs):
        for mob in mobs:
            for mob2 in mobs:
                if mob != mob2:
                    dist = mob.pos.get_distance(mob2.pos)
                    if dist < 32:
                        overlap = 32 - dist
                        shove = mob2.pos - mob.pos
                        shove.length = overlap/2
                        mob2.pos += shove
                        mob.pos -= shove

    def collide_player(self):
        dist = self.pos.get_distance(self.player.pos)
        if dist < 32:
            overlap = 32 - dist
            shove = self.player.pos - self.pos
            shove.length = overlap
            self.pos -= shove
            self.player.damage((self.lvl * 20))
            

    def rotate(self, angle):
        self.dir.rotate(angle)
        self.rotate_img()

    def rotate_img(self):
        self.image = pygame.transform.rotate(self.base_image, -self.dir.angle)

    def patrol(self):
        if self.room != 0:
            move = vec2d(self.dir.x * self.speed * 60, self.dir.y * self.speed * 60)
            if move.length > self.speed:
                move.length = self.speed
            self.pos += move
            self.counter += 5
            if self.counter > random.randint(600, 1000):
                angle = 45 * random.randint(-4, 4)
                self.rotate(angle)
                self.counter = 0
                
    # Here the NPC will track its target. (Usually the player) 
    def track(self, target):
        if self.rect.x + 500 > target.rect.x:
            if self.rect.x - 500 < target.rect.x:
                if self.rect.y + 500 > target.rect.y:
                    if self.rect.y - 500 < target.rect.y:
                        pass


     # movement for the NPC with collision detection.                   
    def movement(self):
        if self.npcmove[0] == 1:
            self.rect.y -= self.speed
            self.collision(self.rect, "UP")
        if self.npcmove[1] == 1:
            self.rect.x -= self.speed
            self.collision(self.rect, "LEFT")
        if self.npcmove[2] == 1:
            self.rect.y += self.speed
            self.collision(self.rect, "DOWN")
        if self.npcmove[3] == 1:
            self.rect.x += self.speed
            self.collision(self.rect, "RIGHT")


class GameSurface(pygame.sprite.DirtySprite):
    def __init__(self, levelsize, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(levelsize).convert()
        self.rect = pygame.Rect(pos, levelsize)
        self.image.fill(color)
        self.dirty = 2
        self.levelsize = levelsize
        
      

class Room(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, block, fg, wg, num, ident):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = pygame.Rect(x, y, w, h)
        self.ident = ident
        self.number = num
        tiles, walls = self.sprite_map(block)
        self.tiles, self.walls = self.wall_collide(tiles, walls)
        fg.add(self.tiles)
        wg.add(self.walls)
        
    def wall_collide(self, tiles, walls):
        pygame.sprite.groupcollide(walls, tiles, True, False)
        return tiles, walls
    
    def dirty_sprite(self, group):
        for i in group:
            i.dirty = 1    
        
    # Here we make the rooms with floor tiles and wall tiles.
    def sprite_map(self, block):
        surf = self.image
        row = ((self.rect.right - self.rect.left) / block)
        col = ((self.rect.bottom - self.rect.top) / block)
        fx = self.rect.left
        fy = self.rect.top
        wx = (self.rect.left - (block))
        wy = (self.rect.top - (block))
        column_wall = col + 2
        row_wall = row + 2
        
        room_tiles = pygame.sprite.LayeredDirty()
        wall_tiles = pygame.sprite.LayeredDirty()
        for part in xrange(col):
            for i in xrange(row):
                i = Tile(surf, block, 3)
                i.rect.left = fx
                i.rect.top = fy
                room_tiles.add(i)
                fx += block
                
            fy += block
            fx = self.rect.left
        
        x = 1
        vorh = 0
        for part in xrange(col + 2):
            for i in xrange(row + 2):
                i = Tile(surf, block, 1)
                i.rect.x = wx
                i.rect.y = wy
                if x == 1:
                    i.ident = "Corner"
                elif x == row_wall:
                    i.ident = "Corner"
                elif x == (row_wall * column_wall - row_wall + 1):
                    i.ident = "Corner"
                elif x == (row_wall * column_wall):
                    i.ident = "Corner"
                elif vorh == (row_wall - 1):
                    i.ident = "Horizontal Wall"
                elif vorh == 0:
                    i.ident = "Horizontal Wall"
                wall_tiles.add(i)
                wx += block
                x += 1
                vorh += 1
                
            wy += block
            wx = (self.rect.left - block)
            vorh = 0
                
        return room_tiles, wall_tiles



        
class Tile(pygame.sprite.DirtySprite): # The Tile sprite, this is one block in every room or wall, and we chose which tile we want.
    def __init__(self, surf, blocksize, select):
        pygame.sprite.DirtySprite.__init__(self)
        self.tile_select(blocksize, select)
        self.dirty = 1
        self.area = surf
    
    def tile_select(self, blocksize, select):
        if select == 1:
            self.image = pygame.image.load("stone.jpg").convert()
            self.ident = "Vertical Wall"
            self.rect = self.image.get_rect()
        elif select == 2:
            self.image = pygame.image.load("door_32.jpg").convert()
            self.rect = self.image.get_rect()
            self.ident = "Exit"
        elif select == 3:
            self.image = pygame.image.load("blacktile.jpg").convert()
            self.ident = "Floor"
            self.rect = self.image.get_rect()
        