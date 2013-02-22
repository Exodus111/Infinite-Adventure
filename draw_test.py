"""
Testing some Draw mechanics
"""
import pygame, random
from pygame.locals import *
from random import randint
from vec2d import vec2d

pygame.init()
size = (640, 480)
screen = pygame.display.set_mode(size)
background = pygame.Surface(size)
clock = pygame.time.Clock()
running = True

pos_a = vec2d(size[0]/2, size[1]/2)
pos_b = vec2d(randint(0, size[0]), randint(0, size[1]))
vector1 = pos_a - pos_b
vector1.angle += 90
vector1.length = vector1.length/20
vector2 = pos_a - vector1
vector3 = pos_a + vector1
vector1.length = vector1.length*6
vector4 = pos_b + vector1
vector5 = pos_b - vector1


myRect1 = pygame.Rect(vector2.x, vector2.y, 5, 5)
myRect2 = pygame.Rect(vector3.x, vector3.y, 5, 5)
myRect3 = pygame.Rect(vector4.x, vector4.y, 5, 5)
myRect4 = pygame.Rect(vector5.x, vector5.y, 5, 5)

myList = [vector2.inttup(), vector3.inttup(), vector4.inttup(), vector5.inttup()]
delta = 0

while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	pygame.draw.rect(background, (0, 255, 0), myRect1, 2)
	pygame.draw.rect(background, (255, 255, 255), myRect2, 2)
	pygame.draw.rect(background, (255, 255, 255), myRect3, 2)
	pygame.draw.rect(background, (255, 255, 255), myRect4, 2)
	pygame.draw.aalines(background, (255, 255, 255), True, myList)
	screen.blit(background, (0,0))
	timer = clock.get_rawtime()
	delta += float(timer)/100
	print int(delta)
	clock.tick(60)
	pygame.display.update()

