import math
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
		self.size_x = 160
		self.size_y = 160
		self.to_be_removed = False
		self.tick_counter = 0
		self.life = 15
		self.ammo = 0
		self.is_knight = False

	def tick(self, knight, move, map_view, my_map):
		if self.life <= 0:
			self.to_be_removed = True
		moveto = [0,0]
		if (self.x*80 - knight.x - map_view[0])**2 + (self.y*80 - knight.y - map_view[1])**2 < 1000**2:
			moveto[0] = knight.x+80+map_view[0] - self.x*80
			moveto[1] = knight.y+80+map_view[1] - self.y*80
			norm = math.sqrt(moveto[0]**2 + moveto[1]**2)
			moveto[0] /= norm
			moveto[1] /= norm
			#if self.x*80 + moveto[0] < 80 or self.x*80 + moveto[0] + self.size_x > len(my_map.map)*80-85:
			#	moveto[0] = 0
			#if self.y*80 + moveto[1] < 80 or self.y*80 + moveto[1] + self.size_y > len(my_map.map[0])*80-160:
			#	moveto[1] = 0
			self.x = self.x*80
			self.y = self.y*80
			if self.tick_counter == 0 and (self.x - knight.x - map_view[0])**2 + (self.y - knight.y - map_view[1])**2 < 500**2:
				my_map.add_bullet((self.x+self.size_x/2+85*moveto[0])/80, (self.y+self.size_y/2+85*moveto[1])/80, moveto[0]/20, moveto[1]/20, 1000, 1)
			for c in my_map.collidable_objects:
				if self != c:
					moveto = c.collide(self, moveto, [0,0])
			self.x += moveto[0]
			self.y += moveto[1]
			self.x = self.x/80
			self.y = self.y/80
		self.tick_counter += 1
		self.tick_counter %= 50
		if self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view) and self.tick_counter == 0:
			knight.life -= 3;
	
	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*width
		self_y = self.y*height
		if (knight_x < self_x+self.size_x and knight_x+width > self_x and
            knight_y+height > self_y and knight_y < self_y+self.size_y):
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			return move
		if self.tick_counter == 0 and knight.is_knight:
			knight.life -= 3
		return move

class SmallMonster(object):
	def __init__(self, x, y):
		self.type = 'SmallMonster'
		self.x = x
		self.y = y
		self.size_x = 100
		self.size_y = 100
		self.to_be_removed = False
		self.tick_counter = 0
		self.life = 5
		self.ammo = 0
		self.is_knight = False

	def tick(self, knight, move, map_view, my_map):
		if self.life <= 0:
			self.to_be_removed = True
		moveto = [0,0]
		moveto[0] = knight.x+80+map_view[0] - self.x*80
		moveto[1] = knight.y+80+map_view[1] - self.y*80
		norm = math.sqrt(moveto[0]**2 + moveto[1]**2)/2.
		moveto[0] /= norm
		moveto[1] /= norm
		#if self.x*80 + moveto[0] < 80 or self.x*80 + moveto[0] + self.size_x > len(my_map.map)*80-85:
		#	moveto[0] = 0
		#if self.y*80 + moveto[1] < 80 or self.y*80 + moveto[1] + self.size_y > len(my_map.map[0])*80-160:
		#	moveto[1] = 0
		self.x = self.x*80
		self.y = self.y*80
		for c in my_map.collidable_objects:
			if self != c:
				moveto = c.collide(self, moveto, [0,0])
		self.x += moveto[0]
		self.y += moveto[1]
		self.x = self.x/80
		self.y = self.y/80
		self.tick_counter += 1
		self.tick_counter %= 25
		if self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view) and self.tick_counter == 0:
			knight.life -= 3;
	
	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*width
		self_y = self.y*height
		if (knight_x < self_x+self.size_x and knight_x+width > self_x and
            knight_y+height > self_y and knight_y < self_y+self.size_y):
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			return move
		if self.tick_counter == 0 and knight.is_knight:
			knight.life -= 3
		return move
		#return [-move[0]/10., -move[1]/10.]


class Tree(object):
	def __init__(self, x, y):
		self.type = 'Tree'
		self.x = x
		self.y = y
		self.size_x = 120
		self.size_y = 160
		self.evil = False
		self.to_be_removed = False
		self.counter = 0

	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*80
		self_y = self.y*80
		if (knight_x < self_x+self.size_x and knight_x+width > self_x and
            knight_y+height > self_y and knight_y < self_y+self.size_y):
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			return move
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, [move[0], 0], map_view):
			if move[0]==0:
				move[0] = 5
			return [move[0], 0]
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, [0, move[1]], map_view):
			if move[1]==0:
				move[1] = 5
			return [0, move[1]]
		return [-move[0]/10., -move[1]/10.]

class Ball(object):
	def __init__(self, x, y):
		self.type = 'Ball'
		self.x = x
		self.y = y
		self.size_x = 200
		self.size_y = 200
		self.size_r = 200
		self.to_be_removed = False

	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*80 + self.size_r/2
		self_y = self.y*80 + self.size_r/2
		if (knight_x - self_x) * (knight_x - self_x) + (knight_y - self_y) * (knight_y - self_y) < self.size_r*self.size_r:
			return True
		return False

	def collide(self, knight, move, map_view):
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			return move
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, [move[0], 0], map_view):
			if move[0]==0:
				move[0] = 5
			return [move[0], -move[1]/5.]
		if not self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, [0, move[1]], map_view):
			if move[1]==0:
				move[1] = 5
			return [-move[0]/5, move[1]]
		return [-move[0]/5., -move[1]/5.]

class Ammo(object):
	def __init__(self, x, y):
		self.type = 'Ammo'
		self.x = x
		self.y = y
		self.size_x = 50
		self.size_y = 50
		self.size_r = 50
		self.to_be_removed = False

	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*80 + self.size_r/2
		self_y = self.y*80 + self.size_r/2
		if (knight_x - self_x+width/2) * (knight_x - self_x+width/2) + (knight_y+height/2 - self_y) * (knight_y - self_y+height/2) < self.size_r*self.size_r:
			return True
		return False

	def collide(self, knight, move, map_view):
		if self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view) and knight.is_knight:
			knight.ammo += 5
			self.to_be_removed = True
		return move

class Bullet(object):
	def __init__(self, x, y, vx, vy, life, dmg):
		self.type = 'Bullet'
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.size_x = 50
		self.size_y = 50
		self.size_r = 50
		self.dmg = dmg
		self.number_of_ticks = 0
		self.lifetime = life
		self.to_be_removed = False

	def tick(self, knight, move, map_view, my_map):
		self.x += self.vx
		self.y += self.vy
		if self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			knight.life -= self.dmg;
			self.to_be_removed = True
		for c in my_map.collidable_objects:
			if self != c and self.doesCollide(c.x*80, c.y*80, c.size_x, c.size_y, [0,0], [0,0]):
				if c.type == 'Monster' or c.type == 'SmallMonster' or c.type == 'ShootingMonster':
					c.life -= self.dmg
					if c.life <= 0:
						c.to_be_removed = True
					self.to_be_removed = True
		self.number_of_ticks += 1
		if self.number_of_ticks > self.lifetime:
			self.to_be_removed = True

	def doesCollide(self, x, y, width, height, move, map_view):
		knight_x = x + map_view[0] + move[0]
		knight_y = y + map_view[1] + move[1]
		self_x = self.x*80 + self.size_r/2
		self_y = self.y*80 + self.size_r/2
		if (knight_x - self_x + width/2) * (knight_x - self_x + width/2) + (knight_y+height/2 - self_y) * (knight_y - self_y+height/2) < self.size_r*self.size_r:
			return True
		return False

	def collide(self, knight, move, map_view):
		if self.doesCollide(knight.x, knight.y, knight.size_x, knight.size_y, move, map_view):
			knight.life -= 2;
			self.to_be_removed = True
		return move

class Knight(object):
	def __init__(self, x, y, size_x, size_y):
		self.type = 'Knight'
		self.x = x
		self.y = y
		self.size_x = size_x
		self.size_y = size_y
		self.life = 100
		self.to_be_removed = False
		self.ammo = 0
		self.is_knight = True

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
		self.monsters += [SmallMonster(pos_x+3, pos_y) for pos_x, pos_y in dane_o_planszy["enemies_pos"]]
		self.tickable_objects = self.monsters[:]
		# self.monsters += [Ammo(5+i*5, i*5) for i in range(5)]
		self.monsters += [Ammo(pos_x, pos_y) for pos_x, pos_y in dane_o_planszy["ammo_pos"]]
		t1 = [(23 - 3.625, 10), (27, 10), (23 - 3.625, 14), (27, 14)]
		trees_positions = t1
		self.trees = [Tree(pos_x, pos_y) for pos_x, pos_y in trees_positions]
		self.trees[0].evil = True
		self.trees[2].evil = True
		# self.trees += [Ball(10, 10)]
		self.trees += [Ball(pos_x, pos_y) for pos_x, pos_y in dane_o_planszy["ball_pos"]]
		self.collidable_objects = self.trees + self.monsters
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
		# self.quest_marks = [quest.Question((i*5, i*5)) for i in range(5)]
		self.quest_marks = []
		for x, y in dane_o_planszy["questionmark_pos"]:
			self.quest_marks.append(quest.Question((x, y)))

	def draw_question_marks(self, screen, map_view):
		for mark in self.quest_marks:
			mark.draw_mark(screen, map_view)
	
	def add_bullet(self, x, y, vx, vy, life=100, dmg=2):
		b = Bullet(x, y, vx, vy, life, dmg)
		self.monsters.append(b)
		self.collidable_objects.append(b)
		self.tickable_objects.append(b)
