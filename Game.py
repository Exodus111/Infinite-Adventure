#!/usr/bin/env python2
"""
2.0
The Game file.
This is where the game mechanics will go, this file runs the game
and puts all the pieces together.
"""

import pygame, random
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
        Engine.__init__(self, "Infinite Adventure", self.size, False)
        map_size = (5000, 5000)

        self.tile_imgs = [line.strip() for line in open("data/tiles.txt")]
        self.npc_imgs = [line.strip() for line in open("data/npcs.txt")]
        self.menu_imgs = [line.strip() for line in open("data/menu.txt")]

        self.surf = Surfaces(map_size, self.size)

        self.level = Levelgen(self.tile_imgs)
        self.rooms = self.level.make_dungeon((150, 150), map_size, (8, 32), 32, 50)
        self.active_sprites = pygame.sprite.LayeredDirty()
        start_pos = self.rooms[0].nw_rect.center

        self.player = Player(self.npc_imgs[0], start_pos, (0, 0))
        self.player.screen_rect.w = self.size[0]*2
        self.player.screen_rect.h = self.size[1]*2

        self.mobgroup = pygame.sprite.LayeredDirty()
        self.mobgroup.add(self.player)

        for i in self.rooms:
            for num in xrange(random.randint(0, 5)):
                num = random.randint(1, len(i.floor))
                for tile in i.floor:
                    if tile.number == num:
                        mob = Mob(self.npc_imgs[1], tile.rect.center, (0,0))
                        self.mobgroup.add(mob)
            for s in self.rooms:
                 pygame.sprite.groupcollide(s.walls, i.floor, True, False)
        for mob in self.mobgroup:
            self.player.collision.moblist.append(mob)
        self.make_gui()
        self.mousepoint = (50, 50)


    def make_gui(self):
        # The Player Menu
        temp_text = "Insert Text here"
        self.player_menu = Gui(self.menu_imgs[0], self.size, 1.5)
        self.player_menu.make_dynamic_text((155, 130), str(self.player.level), (255, 0, 0))
        self.player_menu.make_dynamic_text((300, 70), self.player.name, (0,0,0))
        self.player_menu.make_dynamic_text((450, 150), self.player.title, (0,0,0), 30)
        self.player_menu.make_dynamic_text((64, 440), temp_text, (0,0,0), 20)
        self.player_menu.make_dynamic_text((300, 500), temp_text, (0,0,0), 20)
        self.player_menu.make_button("exit", (50, 30), (1300, 51), "Exit")
        self.p_menu = [0.0, False]
        # HUD Powers buttons
        self.powers_gui = Gui(self.menu_imgs[2], self.size, 12)
        self.powers_gui.new_rect.topleft = ((self.size[0] / 22),(self.size[1] / 20 * 18))
        self.powers_gui.make_dynamic_text((18, 22), "1", (255, 0, 0))
        self.powers_gui.make_dynamic_text((78, 22), "2", (255, 0, 0))
        self.powers_gui.make_dynamic_text((138, 22), "3", (255, 0, 0))
        self.powers_gui.make_dynamic_text((198, 22), "4", (255, 0, 0))
        self.powers_gui.make_dynamic_text((258, 22), "5", (255, 0, 0))
        self.powers_gui.make_dynamic_text((318, 22), "6", (255, 0, 0))
        self.powers_gui.make_dynamic_text((378, 22), "7", (255, 0, 0))
        self.powers_gui.make_dynamic_text((438, 22), "8", (255, 0, 0))
        # Setting up the Mouse over
        self.mouseover = MouseOver(self.menu_imgs[-1])

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

    def oc_menu(self, menu):
        if menu[1] == False:
            self.time = self.dt + 0.1
            return [0.1, True]
        else:
            self.time = self.dt + 1
            return [0.9, False]


    def draw(self):
        # Background
        self.active_sprites.draw(self.surf.surface)

        """
         #This section is to test the Collisions visually
        pygame.draw.rect(self.surf.surface, (255, 255, 255), self.player.collide_rect, 2)
        for tile in self.player.collision.current_quad:
            pygame.draw.rect(self.surf.surface, (255, 255, 255), tile)
        """

        # Dynamic Objects
        self.mobgroup.draw(self.surf.surface)

        # Screen

        self.screen.blit(self.surf.surface, self.surf.rect)

        # Gui Menues
        self.powers_gui.draw(self.screen)

        if self.p_menu[0] != 0.0:
            self.player_menu.draw(self.screen, self.p_menu[0])

        # Mouse pointer
        self.mouseover.draw(self.screen)

    def user_event(self, event):
        pass

    def key_down(self, key):
        if key in (K_w, K_UP):
            self.player.arrows[0] = 1
            self.player.set_timer(self.dt)
        if key in (K_a, K_LEFT):
            self.player.arrows[1] = 1
            self.player.set_timer(self.dt)
        if key in (K_s, K_DOWN):
            self.player.arrows[2] = 1
            self.player.set_timer(self.dt)
        if key in (K_d, K_RIGHT):
            self.player.arrows[3] = 1
            self.player.set_timer(self.dt)

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
        self.mouseover.update(pos)
        self.player.rotate_player(pos, self.surf.rect.topleft)
        if self.p_menu:
            if self.player_menu.button_collision("exit", pos):
                if self.mouseover.state == 0:
                    self.mouseover.state = 1
                    self.mouseover.setup_text(["Exit sign"])
            else:
                self.mouseover.state = 0
        else:
            self.mouseover.state = 0

s = Game()
s.main_loop(fps)
