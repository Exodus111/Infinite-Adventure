"""
This is a test program for the Raycasting.py program I made for pygame.
The program performs a basic test of all three types of Rays with visual representation.
"""

import os, pygame
from raycasting import Raycasting
from pygame.locals import *
from vec2d import vec2d

class Main(object):
    def __init__(self, size):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.surf = pygame.Surface(self.size)
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont("arial", 20)
        self.text1 = self.myfont.render("Press 1, 2 or 3 to pick a Ray", True, (0,0,0))
        self.text2 = self.myfont.render("Left Mouse Button for point A", True, (0,0,0))
        self.text3 = self.myfont.render("Right Mouse Button for point B", True, (0,0,0))
        self.txt1_rect = pygame.Rect(50, 10, 20, 20)
        self.txt2_rect = pygame.Rect(50, 30, 20, 20)
        self.txt3_rect = pygame.Rect(50, 50, 20, 20)

        self.running = True
        self.stage = 1
        self.ray1 = Raycasting((200, 320), (500, 50))
        self.ray2 = Raycasting((200, 320), (200, 50))
        self.ray3 = Raycasting((200, 320), (300, 50))

        self.make_wall(10) # Set the Number to any amount of tiles you want in the wall

    def main_loop(self, fps=0):
        while self.running:
            pygame.display.set_caption("Raytest. FPS: %i" % self.clock.get_fps())
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.key_down(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event.button, event.pos)

    def key_down(self, key):
        if key == K_1:
            self.stage = 1
        elif key == K_2:
            self.stage = 2
        elif key == K_3:
            self.stage = 3

    def mouse_down(self, button, pos):
        if self.stage == 1:
            if button == 1:
                self.ray2.pos = vec2d(pos)
            elif button == 3:
                self.ray2.target = vec2d(pos)
        elif self.stage == 2:
            if button == 1:
                self.ray3.pos = vec2d(pos)
            elif button == 3:
                self.ray3.target = vec2d(pos)
        elif self.stage == 3:
            if button == 1:
                self.ray1.pos = vec2d(pos)
            elif button == 3:
                self.ray1.target = vec2d(pos)

    def update(self):
        self.points = self.ray1.cast(self.wallgroup, 5, True)
        self.points2 = self.ray3.cast(self.wallgroup)
        self.dot = self.ray2.collisionany(self.wallgroup)
        self.dotrect = pygame.Rect(5, 5, 5, 5)
        self.rectangles = []
        if self.points != []:
            for point in self.points:
                rectangle = pygame.Rect(5, 5, 5, 5)
                rectangle.center = point
                self.rectangles.append(rectangle)

        self.rectangles2 = []
        if self.points2 != []:
            for point in self.points2:
                rectangle = pygame.Rect(5, 5, 5, 5)
                rectangle.center = point
                self.rectangles2.append(rectangle)


        self.myLine = self.ray1.draw_ray()
        self.myLine2 = self.ray2.draw_ray()
        self.myLine3 = self.ray3.draw_ray()

    def draw(self):
        self.wallgroup.draw(self.surf)
        self.surf.blit(self.text1, self.txt1_rect)
        self.surf.blit(self.text2, self.txt2_rect)
        self.surf.blit(self.text3, self.txt3_rect)

        pygame.draw.line(self.surf, (255, 0, 255), self.myLine[0], self.myLine[1])
        pygame.draw.line(self.surf, (255, 0, 255), self.myLine2[0], self.myLine2[1])
        pygame.draw.line(self.surf, (255, 0, 255), self.myLine3[0], self.myLine3[1])

        if self.dot != []:
            self.dotrect.center = self.dot[0]
            pygame.draw.rect(self.surf, (255, 255, 0), self.dotrect)

        if self.rectangles != []:
            for recta in self.rectangles:
                pygame.draw.rect(self.surf, (255, 255, 0), recta)

        if self.rectangles2 != []:
            for recta in self.rectangles2:
                pygame.draw.rect(self.surf, (255, 255, 0), recta)

        self.screen.blit(self.surf, (0,0))
        self.surf.fill((255, 255, 255))

    def make_wall(self, size):
        self.wallgroup = pygame.sprite.LayeredDirty()
        x = y = 200
        num = 1
        for wall in xrange(size):
            wall = Tile((x,y), num)
            self.wallgroup.add(wall)
            x += 32
            num += 1


class Tile(pygame.sprite.DirtySprite):
    """The class used to make the Tiles for the wall"""
    def __init__(self, pos, number):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.image = pygame.image.load("images/stone.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.number = number

game = Main((640, 480))
game.main_loop(60)


