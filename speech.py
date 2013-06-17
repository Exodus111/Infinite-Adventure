"""
The speech of NPCs.
"""

from pygame.locals import *

class Speech(object):
	"""Speech class for NPC's"""
	def __init__(self, typeof, mob):
		self.typeof = typeof
		self.mob = mob
		self.shout = pygame.font.SysFont("arial", 15)
		self.message = None

	def update(self, dt):
		pass

	def draw(self):
		self.shout.render(self.message, True, (255, 255, 0))
		


