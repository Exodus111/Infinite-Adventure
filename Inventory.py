"""
Inventory file
"""

import pygame, random, math
from pygame.locals import *
from Mainloop import *
from Entities import *
from Powers import *
from MagicEffects import *
from gui import *

class Inventory(pygame.sprite.DirtySprite):
	"""The inventory class for all items in the game"""
	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)
		self.drawgroup = pygame.sprite.LayeredDirty()
		self.inventory = pygame.sprite.LayeredDirty()

	def update(self, player):
		for item in self.drawgroup:
			item.dirty = 1
			if item.rect.colliderect(player.rect):
				print "Potion picked up"
				item.useage(player)
				self.drawgroup.remove(item)
				self.inventory.add(item)


	def draw(self, surf):
		self.drawgroup.draw(surf)


	def spawn_item(self, mob):
		items = self._gen_item(mob)
		for item in items:
			self.drawgroup.add(item)

	def _gen_item(self, mob):
		items = []
		potion = Potion(random.randint(1, 3), 1)
		potion.rect.center = mob.pos.inttup()
		items.append(potion)

		return items

	def add_to(self, item):
		self.inventory.add(item)
		print "Potion added"

	def remove_from(self, item):
		self.inventory.remove(item)

	def use(self):
		pass

class Potion(Inventory):
	"""docstring for Potions"""
	def __init__(self, typeof, strength, quantity=1):
		pygame.sprite.DirtySprite.__init__(self)
		self.type = typeof
		self.strength = strength
		self.dirty = 1
		self.type_of_potion(typeof)

	def type_of_potion(self, typeof):
		if typeof == 1:
			self.name = "Health Potion"
			self.image = pygame.image.load("potion_health.png").convert_alpha()
			self.rect = self.image.get_rect()
			self.strength = (random.randint(15, 50) * self.strength)
		elif typeof == 2:
			self.name = "Mana Potion"
			self.image = pygame.image.load("potion_mana.png").convert_alpha()
			self.rect = self.image.get_rect()
			self.strength = (random.randint(15, 50) * self.strength)
		elif typeof == 3:
			self.name = "Power Potion"
			self.image = pygame.image.load("potion_power.png").convert_alpha()
			self.rect = self.image.get_rect()
			self.strength = (random.randint(15, 50) * self.strength)

	def useage(self, player):
		if item.name == "Health Potion":
			player.hp += item.strength
			if player.hp > player.max_hp:
				player.hp = player.max_hp
		elif item.name == "Mana Potion":
			player.mana += item.strength
			if player.mana > player.max_mana:
				player.mana = player.max_mana
		elif item.name == "Power Potion":
			pass

		



		





