#!/usr/bin/env Python
'''
Created on Dec 29, 2012

This is the game file, this is where the actual game code will be stored.
At this moment this is my experiment file, and a lot of what I do here I'll push into the Game's "engine" file once I polish them.

@author: aurelio
'''
import pygame
from pygame.locals import *
from Mainloop import *
from Entities import *
from Powers import *
from MagicEffects import *
from Inventory import *
from gui import *

fps = 30
# This is the main class of the game, it inherits from the "engine" class, the __init__ method loads most of the game assets.
class Game(Engine):
    def __init__(self):
        # First I load my chosen screen size and use it to override the default one, while initializing the engine.
        self.w = 1240
        self.h = 960
        Engine.__init__(self, size=(self.w, self.h), fill=(255, 255, 255))
        self.screen_rect = pygame.Rect(0, 0, self.w, self.h)

        # Here we set up an image file for the mouse cursor
        # (making sure to convert it and keep transparency)
        self.mouse_over = MouseOver()
        self.mouse_image = self.mouse_over.mouse_img()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_pos = (0, 0)

        self.player = Player()
        self.player.level_init()
        self.inventory = Inventory()

        self.current_level = 0
        self.game = False
        self.start_menu = StartMenu((self.w, self.h))
        self.start_menu.update()

    def game_init(self):

        # Some colors, these will change.
        blackColor = (0, 0, 0)
        white_color = (255, 255, 255)
        sgidarkgray = (85, 85, 85)
        yellowColor = (255, 255, 0)

        # Setting up the background surface (the game map).
        self.blocksize = 32
        self.background = GameSurface((8000, 8000), (0, 0), blackColor)
        self.bg = pygame.sprite.LayeredDirty(self.background)


        # Here we start making the map. (This takes the longest time to load)
        self.rooms = self.generate_levels(self.blocksize, self.background.levelsize)
        self.add_exit(self.rooms, self.blocksize)

        # Here I load up the player, and the variables necessary
        # for movement and rotation.
        self.cp = pygame.Rect(0, 0, self.player.rect.width, self.player.rect.height)
        self.player.set_collide(self.rooms)

        # Here we mage the Gui
        self.gui = GUI((self.w, self.h), self.player)
        self.player_window = PlayerWindow((self.w, self.h), self.player)
        self.power_window = PowerWindow((self.w, self.h), self.player)
        self.power_window.update()
        self.test_text = []

        # Some Timer variables.
        self.time_passed = self.clock.get_fps()
        self.cd1 = 0.0
        self.cd2 = 0.0
        self.cd3 = 0.0
        self.cd4 = 0.0

        # Then we need to set up the rooms, placing the player in the first one.
        # (and centering the screen on him)
        self.background.rect.x, self.background.rect.y = self.set_rooms(
            self.rooms, self.player, self.background.rect.x, self.background.rect.y, self.cp, self.w, self.h)

        # Time to add some mobs.
        self.mobs = self.add_mobs((random.randint(1, 10)), self.rooms, self.player, self.background)
        self.l_mobs = []

        # And we set up the players powers
        self.powergroup = pygame.sprite.LayeredDirty()
        self.b3 = False

        self.game = True


    def generate_levels(self, block, size):

        if self.current_level == 0:
            rooms = self.generate_room(block, (size[0]/4, size[1]/4))
            self.current_level += 1
        elif self.current_level == 1:
            rooms = self.generate_room(block, (size[0]/2.5, size[1]/2.5))
            self.current_level += 1
        elif self.current_level == 2:
            rooms = self.generate_room(block, (size[0]/2, size[1]/2))
            self.current_level += 1
        elif self.current_level == 3:
            rooms = self.generate_room(block, size)

        return rooms

    # the update method. This one is called in the game_loop (from the engine)
    # but it must be run in this file.
    def update(self):
        self.mouse_image = self.mouse_over.mouse_img()

        if self.game == True:
            if self.player.nextlevel == True:
                self.player.nextlevel = False
                self.game_init()

            # Updating the gui.
            self.gui.update(self.player)

            # This is the rectangle for our screen.
            self.screen_rect.topleft = (-self.background.rect.x, -self.background.rect.y)
            # We then use that rectangle to cut away anything we do not need to render.
            self.limit_rooms(self.rooms, self.screen_rect)
            self.l_mobs = self.limit_mobs(self.screen_rect, self.mobs)


            # Adding the cut down sprites to the draw group.
            self.wallsprites = self.add_rooms()

            self.mobgroup = pygame.sprite.LayeredDirty()
            self.mobgroup.add(self.player)
            self.mobgroup.add(self.l_mobs)

            self.inventory.update(self.player)

            # Movement for the player.
            self.player.move(self.player.dir, self.cp, (self.w, self.h))
            self.cp.x, self.cp.y = self.find_position(self.player.rect.x, self.player.rect.y,
                                                                self.background.rect.x, self.background.rect.y)

            # Here we scroll the map using the mouse pointer.
            self.map_move(self.background, self.cp, self.w, self.h)

            if self.b3 == True:
                self.cone.effect.fire(self.player.rect.center, self.b_pos, self.delta_time)

            self.greenbars = []
            self.redbars = []
            for mob in self.l_mobs:
                mob.run(self.rooms, self.l_mobs, self.player, self.delta_time)
                redbar, greenbar = mob.health_bar()
                self.redbars.append(redbar)
                self.greenbars.append(greenbar)
                if mob.state == "DEAD":
                    self.inventory.spawn_item(mob)

            self.mouse_over.check_mobs(self.l_mobs, self.background)
            self.mouse_over.check_tiles(self.wallsprites, self.background)
            if self.player.state == "DEAD":
                self.game = False
                self.current_level = 0
                self.start_menu.select(2)
                self.start_menu.update()

    # The draw function. This is where things are actually drawn to screen.
    # Its called in the engines mainloop, but must be run in this file.
    def draw(self):

        if self.game == True:

            # Here we clip to the clipping rectangle.
            self.wallsprites.set_clip(self.screen_rect)
            # And run the necesary updates.
            self.wallsprites.update()
            self.mobgroup.update(self.delta_time)
            self.powergroup.update(self.delta_time)

            # Now we draw things in order.
            # First we draw the levels.
            self.wallsprites.draw(self.background.image)

            # Then we draw the Player and mobs.
            self.mobgroup.draw(self.background.image)
            for mob in self.mobgroup:
                if mob.state == "SHOUTING":
                    self.background.image.blit(mob.mssg, mob.mssg_rect)

            # Then we draw the Inventory items
            self.inventory.draw(self.background.image)

            # Then we draw the powers.
            self.powergroup.draw(self.background.image)
            for power in self.powergroup:
                if power.state == "EXPLODING":
                    pygame.draw.circle(self.background.image, (255, 255, 255), power.pos.inttup(), power.radius, 1)
                elif power.state == "CONE":
                    pygame.draw.aalines(self.background.image, (255, 255, 255), True, power.vectorlist)

            # Here we draw the healthbars of the mobs.
            for bars in self.redbars:
                pygame.draw.rect(self.background.image, pygame.Color("red"), bars)
            for bars in self.greenbars:
                pygame.draw.rect(self.background.image, pygame.Color("green"), bars)


            pygame.draw.rect(self.background.image, (255, 255, 255), self.screen_rect, -1)

            # Then we draw the everything to the screen.
            self.bg.draw(self.screen)

            # Everything below this line is drawn directly to the Screen
            #  not the Background Surface

            # Then we draw the GUI.
            self.gui.draw(self.screen)
            if self.player_window.state == True:
                self.player_window.draw(self.screen)
            if self.player_window.powerstate == True:
                self.player_window.state = False
                self.power_window.draw_window(self.screen)
        else:
            self.start_menu.draw(self.screen)

        # Then we draw the mousepointer.
        self.mouse_over.draw(self.screen)
        self.screen.blit(self.mouse_image, self.mouse_pos)
        pygame.display.update()


    def user_event(self, event):
        pass

    # An event method giving us all key down presses.
    def key_down(self, key):

        if self.game == True:
            if key in (K_w, K_UP):
                self.player.dir[0] = 1
            if key in (K_a, K_LEFT):
                self.player.dir[1] = 1
            if key in (K_s, K_DOWN):
                self.player.dir[2] = 1
            if key in (K_d, K_RIGHT):
                self.player.dir[3] = 1
            if key == K_ESCAPE:
                pygame.quit()
            if key == K_2:
                if self.cd2 < self.delta_time:
                    self.ball = Powers(self.player.level, self.player.rect.center)
                    self.ball.fire_ball()
                    if self.player.mana >= self.ball.manacost:
                        self.ball.set_collision(self.rooms, self.l_mobs)
                        self.powergroup.add(self.ball.effect)
                        self.ball.effect.fire(self.player.rect.center, self.b_pos)
                        self.player.shout_spell(self.ball.name)
                        self.player.mana -= self.ball.manacost
                        self.cd2 = self.delta_time + self.ball.cooldown
                    else:
                        print "Not enough Mana"
            if key == K_3:
                if self.cd3 < self.delta_time:
                    self.cone = Powers(self.player.level, self.player.rect.center)
                    self.cone.cone_of_frost()
                    if self.player.mana >= self.cone.manacost:
                        self.b3 = True
                        self.cone.set_collision(None, self.l_mobs)
                        self.powergroup.add(self.cone.effect)
                        self.player.shout_spell(self.cone.name)
                        self.player.mana -= self.cone.manacost
                        self.cd3 = self.delta_time + self.cone.cooldown
                    else:
                        print "Not enough Mana"
            if key == K_4:
                if self.cd4 < self.delta_time:
                    self.ring = Powers(self.player.level, self.player.rect.center)
                    self.ring.ring_of_fire()
                    if self.player.mana >= self.ring.manacost:
                        self.ring.set_collision(None, self.l_mobs)
                        self.powergroup.add(self.ring.effect)
                        self.ring.effect.fire(self.player.rect.center, None)
                        self.player.shout_spell(self.ring.name)
                        self.player.mana -= self.ring.manacost
                        self.cd4 = self.delta_time + self.ring.cooldown
                    else:
                        print "Not enough Mana"
            if key == K_p:
                if self.player_window.state == False:
                    self.player_window.update()
                    self.player_window.state = True
                elif self.player_window.state == True:
                    self.player_window.state = False
            if key == K_LSHIFT:
                self.mouse_over.state = 2

    # An event method giving us all key up presses.
    def key_up(self, key):

        if self.game == True:
            if key in (K_w, K_UP):
                self.player.dir[0] = 0
            if key in (K_a, K_LEFT):
                self.player.dir[1] = 0
            if key in (K_s, K_DOWN):
                self.player.dir[2] = 0
            if key in (K_d, K_RIGHT):
                self.player.dir[3] = 0
            if key == K_3:
                self.b3 = False
                self.cone.effect.state = "DEAD"
            if key == K_LSHIFT:
                self.mouse_over.state = 1


    # Two event Methods for the mouse keys (down and up). buttons are 1=left , 2=middle, 3=right.
    def mouse_down(self, button, pos):

        if self.game == True:
            if button == 1:
                if self.player_window.state == True:
                    self.player_window.mouse_button(button)
                if self.cd1 < self.delta_time:
                    self.missile = Powers(self.player.level, self.player.rect.center)
                    self.missile.magic_missile()
                    if self.player.mana >= self.missile.manacost:
                        self.missile.set_collision(self.rooms, self.l_mobs)
                        self.powergroup.add(self.missile.effect)
                        self.missile.effect.fire(self.player.rect.center, self.b_pos)
                        self.player.shout_spell(self.missile.name)
                        self.player.mana -= self.missile.manacost
                        self.cd1 = self.delta_time + self.missile.cooldown
                    else:
                        print "Not enough Mana"
        else:
            if button == 1:
                menu_button = self.start_menu.mouse_press()
                if menu_button == 1:
                    self.player = Player()
                    self.player.level_init()
                    self.game_init()
                elif menu_button == 3:
                    self.running = False

    def mouse_up(self, button, pos):
        pass

    # Event method for mouse motion.
    def mouse_motion(self, buttons, pos, rel):
        self.mouse_pos = pos
        self.mouse_over.update_pos(pos)

        if self.game == True:
            if self.player_window.state == True:
                self.player_window.mouse_mov(pos, buttons)

            b_pos_x = pos[0] - self.background.rect.x
            b_pos_y = pos[1] - self.background.rect.y
            self.b_pos = (b_pos_x, b_pos_y)

           # Here we call the method to rotate the mouse.
            self.player.rot = self.rotate((self.cp.centerx, self.cp.centery),
                                (self.mouse_pos[0] + (self.mouse_rect.width/2),
                                self.mouse_pos[1] + (self.mouse_rect.height/2)))
            self.player.image = self.rotate_image(self.player.base_img, (self.player.rot))

            self.map_scroll(self.mouse_pos, self.w, self.h,)
        else:
            self.start_menu.mouse_mov(self.mouse_pos)

    def screen_message(self, text):
        pass

# This runs the game once we run this file. The fps is at te top of the file.
s = Game()
s.main_loop(fps)