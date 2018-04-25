import pygame
import os.path
from colors import Colors

class Monster(object):
	def __init__(self, x, y):
		self.type = 'Monster'
		self.x = x
		self.y = y


class Tree(object):
	def __init__(self, x, y):
		self.type = 'Tree'
		self.x = x
		self.y = y


class Knight(object):
	def __init__(self, x, y):
		self.type = 'Knight'
		self.x = x
		self.y = y

	def get_pos(self):
		pos = (self.x, self.y)
		return pos

class Map(object):
	def __init__(self):
		print('test')
		self.map = [
			[
				{
					"color": Colors.GRASS,
					"solid": False
				} for y in range(27)
			] for x in range(48)
		]

		e1 = [(6, 2), (40, 2), (6, 23), (40, 23)]
		e2 = [(17, 3), (29, 3), (17, 22), (29, 22), (4, 12), (42, 12)]
		enemies_positions = e1 + e2
		self.monsters = [Monster(pos_x, pos_y) for pos_x, pos_y in enemies_positions]

		t1 = [(23 - 3.625, 10), (27, 10), (23 - 3.625, 14), (27, 14)]
		trees_positions = t1
		self.trees = [Tree(pos_x, pos_y) for pos_x, pos_y in trees_positions]

		# dodaje przeciwnikow
		for pos_x, pos_y in enemies_positions:
			for x in range(2):
				for y in range(2):
					self.map[pos_x + x][pos_y + y]["color"] = Colors.MONSTER
					self.map[pos_x + x][pos_y + y]["solid"] = True

		#dodaje kamienie
		# pionowe
		for y in range(4, 23): # bez 24
			for x in [6, 23, 40]:
				self.map[x][y]["color"] = Colors.STONE
				self.map[x + 1][y]["color"] = Colors.STONE
		#poziome
		for x in range(6, 42): # bez 42
			self.map[x][12]["color"] = Colors.STONE
			self.map[x][13]["color"] = Colors.STONE
		for x in range(19, 29):
			for y in [3, 22]:
				self.map[x][y]["color"] = Colors.STONE
				self.map[x][y + 1]["color"] = Colors.STONE

		#koniec planszy
		for x in range(48):
			for y in [0, 26]:
				self.map[x][y]["color"] = Colors.END_OF_MAP
				self.map[x][y]["solid"] = True
		for y in range(27):
			for x in [0, 47]:
				self.map[x][y]["color"] = Colors.END_OF_MAP
				self.map[x][y]["solid"] = True