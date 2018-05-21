import pygame
import os.path
from colors import Colors
from genmap import daj_plansze
import question as quest


class Monster(object):
	def __init__(self, x, y):
		self.type = 'Monster'
		self.x = x
		self.y = y
	
	def doesCollide(self, knight, move, map_view):
		knight_x = knight.x + map_view[0] + move[0]
		knight_y = knight.y + map_view[1] + move[1]
		self_x = self.x*knight.size_x
		self_y = self.y*knight.size_y
		if (knight_x < self_x+knight.size_x*2 and knight_x+knight.size_x > self_x and
            knight_y+knight.size_y > self_y and knight_y < self_y+knight.size_y*2):
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight, move, map_view):
			return move
		#knight.life -= 2
		#return [-move[0]/10., -move[1]/10.]


class Tree(object):
	def __init__(self, x, y):
		self.type = 'Tree'
		self.x = x
		self.y = y
		self.size_x = 60
		self.size_y = 80

	def doesCollide(self, knight, move, map_view):
		knight_x = knight.x + map_view[0] + move[0]
		knight_y = knight.y + map_view[1] + move[1]
		self_x = self.x*knight.size_x
		self_y = self.y*knight.size_y
		if (knight_x < self_x+self.size_x*2 and knight_x+knight.size_x > self_x and
            knight_y+knight.size_y > self_y and knight_y < self_y+self.size_y*2):
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight, move, map_view):
			return move
		if not self.doesCollide(knight, [move[0], 0], map_view):
			if move[0]==0:
				move[0] = 5
			return [move[0], 0]
		if not self.doesCollide(knight, [0, move[1]], map_view):
			if move[1]==0:
				move[1] = 5
			return [0, move[1]]
		return [-move[0]/10., -move[1]/10.]

class Ball(object):
	def __init__(self, x, y):
		self.type = 'Ball'
		self.x = x
		self.y = y
		self.size_r = 200

	def doesCollide(self, knight, move, map_view):
		knight_x = knight.x + map_view[0] + move[0]
		knight_y = knight.y + map_view[1] + move[1]
		self_x = self.x*knight.size_x + self.size_r/2
		self_y = self.y*knight.size_y + self.size_r/2
		if (knight_x - self_x) * (knight_x - self_x) + (knight_y - self_y) * (knight_y - self_y) < self.size_r*self.size_r:
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight, move, map_view):
			return move
		if not self.doesCollide(knight, [move[0], 0], map_view):
			if move[0]==0:
				move[0] = 5
			return [move[0], 0]
		if not self.doesCollide(knight, [0, move[1]], map_view):
			if move[1]==0:
				move[1] = 5
			return [0, move[1]]
		return [-move[0]/10., -move[1]/10.]

class Knight(object):
	def __init__(self, x, y, size_x, size_y):
		self.type = 'Knight'
		self.x = x
		self.y = y
		self.size_x = size_x
		self.size_y = size_y
		self.life = 10

	def get_pos(self):
		pos = (self.x, self.y)
		return pos


class Map(object):
	def __init__(self):
		# print('test')
		self.map = [
			[
				{
					"color": Colors.GRASS,
					"solid": False
				} for y in range(27)
			] for x in range(48)
		]
		dane_o_planszy = daj_plansze()

		# e1 = [(6, 2), (40, 2), (6, 23), (40, 23)]
		# e2 = [(17, 3), (29, 3), (17, 22), (29, 22), (4, 12), (42, 12)]
		# enemies_positions = e1 + e2
		self.monsters = [Monster(pos_x, pos_y) for pos_x, pos_y in dane_o_planszy["enemies_pos"]]
		#
		t1 = [(23 - 3.625, 10), (27, 10), (23 - 3.625, 14), (27, 14)]
		trees_positions = t1
		self.trees = [Tree(pos_x, pos_y) for pos_x, pos_y in trees_positions]
		self.trees += [Ball(10, 10)]
		# dodaje kamienie
		# pionowe

		for x in range(47):
			for y in range(26):
				if dane_o_planszy["plansza"][x][y]["znak"] == "S":
					for delta_x in range(2):
						for delta_y in range(2):
							self.map[x + delta_x][y + delta_y]["color"] = Colors.STONE

		#
		# dodaje przeciwnikow
		for pos_x, pos_y in dane_o_planszy["enemies_pos"]:
			for delta_x in range(2):
				for delta_y in range(2):
					self.map[pos_x + delta_x][pos_y + delta_y]["color"] = Colors.MONSTER
					#self.map[pos_x + delta_x][pos_y + delta_y]["solid"] = True
			# for x in range(2):
			# 	for y in range(2):
			# 		self.map[pos_x + x][pos_y + y]["color"] = Colors.MONSTER
			# 		self.map[pos_x + x][pos_y + y]["solid"] = True
		# #poziome
		# for x in range(6, 42): # bez 42
		# 	self.map[x][12]["color"] = Colors.STONE
		# 	self.map[x][13]["color"] = Colors.STONE
		# for x in range(19, 29):
		# 	for y in [3, 22]:
		# 		self.map[x][y]["color"] = Colors.STONE
		# 		self.map[x][y + 1]["color"] = Colors.STONE
		#
		#koniec planszy
		for x in range(48):
			for y in [0, 26]:
				self.map[x][y]["color"] = Colors.END_OF_MAP
				self.map[x][y]["solid"] = True
		for y in range(27):
			for x in [0, 47]:
				self.map[x][y]["color"] = Colors.END_OF_MAP
				self.map[x][y]["solid"] = True

		# qeust_marks
		self.quest_marks = [quest.Question((i*5, i*5)) for i in range(5)]

	def draw_question_marks(self, screen, map_view):
		for mark in self.quest_marks:
			mark.draw_mark(screen, map_view)
