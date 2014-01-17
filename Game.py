#!/usr/bin/env python2
"""
2.0
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
from Gui import *

fps = 60


class Game(Engine):
    """Infinite Adventure"""
    def __init__(self):
        self.size = (1024, 960)
        Engine.__init__(self, self.size)
        map_size = (5000, 5000)

        self.surf = Surfaces(map_size, self.size)

        self.player = Player("images/player.png", (self.size[0]/2, self.size[1]/2), (0, 0))
        self.mobgroup = pygame.sprite.LayeredDirty()
        self.mobgroup.add(self.player)
        self.tile_imgs = [line.strip() for line in open("data/tiles.txt")]
        self.npc_imgs = [line.strip() for line in open("data/npcs.txt")]
        self.menu_imgs = [line.strip() for line in open("data/menu.txt")]

        self.make_gui()

        self.level = Levelgen(self.tile_imgs)
        self.rooms = self.level.make_dungeon((150, 150), map_size, (8, 32), 32, 50)

        self.active_sprites = pygame.sprite.LayeredDirty()
        start_pos = self.rooms[0].nw_rect.center
        self.player.rect.center = start_pos
        self.player.screen_rect.w = self.size[0]*2
        self.player.screen_rect.h = self.size[1]*2

        for i in self.rooms:
            for s in self.rooms:
                 pygame.sprite.groupcollide(s.walls, i.floor, True, False)


    def update(self):
        # Surface
        self.surf.update_surface(self.player.pos.inttup(), self.player.speed)
        for room in self.rooms:
            self.active_sprites.add(room.walls)
            self.active_sprites.add(room.floor)
        self.active_sprites.set_clip(self.player.screen_rect)

        # Mobs
        self.mobgroup.update(self.rooms, self.dt)

        # Menues
        if self.player.level != self.player.old_level:
            text = str(self.player.level)
            old_text = str(self.player.old_level)
            self.player_menu.update(0, [text])
            if len(text) > len(old_text):
                self.player_menu.dyn_text[1].x -= 10
            self.player.old_level = self.player.level

        if self.p_menu[0] != 0.0:
            if self.p_menu[1] == True:
                count = self.dt - self.time
            else:
                count = self.time - self.dt
            if count < 1:
                self.p_menu[0] = count

    def draw(self):
        # Background
        self.active_sprites.draw(self.surf.surface)

        """ #This section is to test the Collisions visually
        pygame.draw.rect(self.surf.surface, (255, 255, 255), self.player.collide_rect, 2)
        for tile in self.player.collision.current_quad:
            pygame.draw.rect(self.surf.surface, (255, 255, 255), tile)
        """

        # Dynamic Objects
        self.mobgroup.draw(self.surf.surface)

        # Screen

        self.screen.blit(self.surf.surface, self.surf.rect)

        # Gui Menues
        if self.p_menu[0] != 0.0:
            self.player_menu.draw(self.screen, self.p_menu[0])

        # Mouse pointer

    def make_gui(self):
        # The Player Menu
        self.player_menu = Gui(self.menu_imgs[0], self.size, 1.5)
        self.player_menu.make_dynamic_text((155, 130), str(self.player.level), (255, 0, 0))
        self.player_menu.make_dynamic_text((300, 70), self.player.name, (0,0,0))
        self.player_menu.make_dynamic_text((450, 150), self.player.title, (0,0,0), 30)
        self.player_menu.make_button("exit", (50, 30), (1300, 51), "Exit")
        self.p_menu = [0.0, False]
        # Next Menu item

    def oc_menu(self, menu):
        if menu[1] == False:
            self.time = self.dt + 0.1
            return [0.1, True]
        else:
            self.time = self.dt + 1
            return [0.9, False]


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
        if key == K_o:
            self.p_menu = self.oc_menu(self.p_menu)
            if self.p_menu[1] == True:
                self.player_menu.button_color["exit"] = (0,0,0)


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
        if self.p_menu:
            if button == 1:
                if self.player_menu.button_collision("exit", pos, True):
                    self.p_menu = self.oc_menu(self.p_menu)

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, buttons, pos, rel):
        if self.p_menu:
            self.player_menu.button_collision("exit", pos)

s = Game()
s.main_loop(fps)
