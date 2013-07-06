from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform
 
class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))
         
        self.pos= vec2d(400, 300)
        self.target= vec2d(300,300)
         
    def update(self):
        dir= self.target- self.pos
         
        if dir.length>3:
            dir.length= 3
            self.pos += dir
         
         
    def keyUp(self, key):
        pass
         
    def mouseUp(self, button, pos):
        #I messed up a bit here in the video. Old line was
        #self.target= pos
        #pos here is a TUPLE. But we want self.target to be a vec2d
        #so instead first create vec2d object from the tuple, then assign
        self.target= vec2d(pos)
         
    def mouseMotion(self, buttons, pos, rel):
        pass
         
    def draw(self):
        self.screen.fill((255,255,255))
         
        pygame.draw.circle(self.screen, (255,0,0), self.target.inttup(), 30, 1)
         
        pygame.draw.circle(self.screen, (0,0,0), self.pos.inttup(), 21)
        pygame.draw.circle(self.screen, (200,200,255), self.pos.inttup(), 20)
         
         
s = Starter()
s.mainLoop(40)