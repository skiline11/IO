import pygame
import math
import time
import os.path
import colors
from gui import Button


el_horizontal = 16
el_vertical = 9
framerate = 60
PLAY_MODE = 1
MENU_MODE = 0
menu_obj = []


def create_map():
	global enemies_positions

	color_grass = (100, 204, 0)
	color_stone = (156, 156, 156)
	color_monster = (255, 0, 0)
	color_end_of_map = (0, 0, 0)
	colors = {"grass": color_grass, "stone": color_stone, "monster": color_monster, "end_of_map": color_end_of_map}

	# mapa pełna kamieni
	my_map = [
		[
			{
				"color": colors["grass"],
				"solid": False
			} for y in range(27)
		] for x in range(48)
	]

	# dodaje przeciwnikow
	for pos_x, pos_y in enemies_positions:
		for x in range(2):
			for y in range(2):
				my_map[pos_x + x][pos_y + y]["color"] = colors["monster"]
				my_map[pos_x + x][pos_y + y]["solid"] = True


	#dodaje kamienie
	# pionowe
	for y in range(4, 23): # bez 24
		for x in [6, 23, 40]:
			my_map[x][y]["color"] = colors["stone"]
			my_map[x + 1][y]["color"] = colors["stone"]
	#poziome
	for x in range(6, 42): # bez 42
		my_map[x][12]["color"] = colors["stone"]
		my_map[x][13]["color"] = colors["stone"]
	for x in range(19, 29):
		for y in [3, 22]:
			my_map[x][y]["color"] = colors["stone"]
			my_map[x][y + 1]["color"] = colors["stone"]

	#koniec planszy
	for x in range(48):
		for y in [0, 26]:
			my_map[x][y]["color"] = colors["end_of_map"]
			my_map[x][y]["solid"] = True
	for y in range(27):
		for x in [0, 47]:
			my_map[x][y]["color"] = colors["end_of_map"]
			my_map[x][y]["solid"] = True

	return my_map


# tworzę okienko i rysuję na nim mapę
def create_background(screen, width, height, image_knight):
	global el_horizontal, el_vertical
	new_background = pygame.Surface((width, height))

	x_offset = int(map_view[0]/el_size[0])
	y_offset = int(map_view[1]/el_size[1])
	x_remainder = map_view[0]%el_size[0]
	y_remainder = map_view[1]%el_size[1]

	for x in range(el_horizontal+1):
		for y in range(el_vertical+1):
			if x+x_offset >= len(my_map):
				continue
			if y+y_offset >= len(my_map[x+x_offset]):
				continue
			el = my_map[x+x_offset][y+y_offset]
			pygame.draw.rect(
				new_background,
				el["color"],
				pygame.Rect(int(x) * el_size[0] - x_remainder, int(y) * el_size[1] - y_remainder, el_size[0], el_size[1])
			)
	return new_background


def init_menu():
	global screen, width, height, image_menu
	button_width = 200
	button_height = 100
	horizontal = width / 2 - button_width / 2 - 77
	vertical = height / 2 - button_height / 2 + 250
	menu_obj.append(Button((horizontal, vertical), (button_width, button_height), colors.Colors.BLACK, colors.Colors.RED, start_game, "PLAY"))
	image_menu = pygame.image.load(os.path.join("img/menu.jpg"))
	pygame.mixer.music.load('sounds/soundtrack.mp3')
	pygame.mixer.music.play(-1)

def menu_draw():
	global screen, image_menu

	screen.fill(colors.Colors.WHITE)
	screen.blit(image_menu, (0, 0))
	for obj in menu_obj:
		obj.render(screen)

	pygame.display.flip()


def menu_input():
	global is_alive, clock
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
			is_alive = False
		if event.type == pygame.QUIT:
			is_alive = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: # Left click
				for button in Button.all:
					if button.is_active:
						button.pressed()
						button.is_active = False
						break
	clock.tick(framerate)


# obsługuję klawiaturę i poruszam się rycerzem po mapie z uwzględnieniem że nie da się wyjść poza mapę
def game_input():
	move_val = 10
	global move, knight_pos, height, width, clock, el_size, is_alive, my_map, global_state
	global exit_enter_sound_effect, sound_effect_delay
	map_movable_area_x = 1.0/16
	map_movable_area_y = 1.0/9
	event_array = pygame.event.get()
	if event_array:
		for event in event_array:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
				is_alive = False
			if event.type == pygame.QUIT:
				is_alive = False
			if event.type == pygame.KEYUP:
				game_input.times_pressed -= 1
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					move[0] = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					move[1] = 0
			if event.type == pygame.KEYDOWN:
				game_input.times_pressed += 1
				if event.key == pygame.K_ESCAPE:
					exit_enter_sound_effect.play()
					pygame.time.wait(sound_effect_delay)
					global_state = MENU_MODE
				if event.key == pygame.K_RIGHT:
					move[0] = move_val
				if event.key == pygame.K_LEFT:
					move[0] = -move_val
				if event.key == pygame.K_UP:
					move[1] = -move_val
				if event.key == pygame.K_DOWN:
					move[1] = move_val

	real_knight_pos = [0, 0]
	real_knight_pos[0] = knight_pos[0] + map_view[0]
	real_knight_pos[1] = knight_pos[1] + map_view[1]

	if game_input.times_pressed > 0:
		print("tutaj")
		# jeśli znajdujemu się wystarczająco daleko od brzegów planszy to nie będziemy przesówać jej widoku
		# tylko przesuniemy się rycerzem
		print(real_knight_pos)
		cur_el_x_front = int((real_knight_pos[0]) / el_size[0])
		cur_el_x_end = int((real_knight_pos[0] + el_size[0] - 1) / el_size[0])
		next_el_y = int((real_knight_pos[1] + el_size[1] + move[1]) / el_size[1])
		prev_el_y = int((real_knight_pos[1] + move[1]) / el_size[1])

		cur_el_y_top = int((real_knight_pos[1]) / el_size[1])
		cur_el_y_bottom = int((real_knight_pos[1] + el_size[1] - 1) / el_size[1])
		next_el_x = int((real_knight_pos[0] + el_size[0] + move[0]) / el_size[0])
		prev_el_x = int((real_knight_pos[0] + move[0]) / el_size[0])

		if move[0] != 0:
			print("poziomo")
			if (my_map[next_el_x][cur_el_y_top]["solid"] or my_map[next_el_x][cur_el_y_bottom]["solid"]) and move[
				0] > 0:
				move[0] = (next_el_x - 1) * el_size[0] - real_knight_pos[0]
			if (my_map[prev_el_x][cur_el_y_top]["solid"] or my_map[prev_el_x][cur_el_y_bottom]["solid"]) and move[
				0] < 0:
				move[0] = (prev_el_x + 1) * el_size[0] - real_knight_pos[0]

			if ((knight_pos[0] + move[0] <= width * (1 - map_movable_area_x) - el_size[0] and
							 knight_pos[0] + move[0] >= width * map_movable_area_x) or
					(knight_pos[0] + move[0] <= width * map_movable_area_x and
							 map_view[0] == 0 and knight_pos[0] + move[0] >= 0) or
					(knight_pos[0] + move[0] >= width * (1 - map_movable_area_x) - el_size[0] and
							 map_view[0] == len(my_map) * el_size[0] - width and knight_pos[0] + move[0] <= width -
						el_size[0])):
				knight_pos[0] += move[0]
			elif len(my_map) * el_size[0] - width >= map_view[0] + move[0] >= 0:
				map_view[0] += move[0]

		if move[1] != 0:
			print("pionowo")
			if (my_map[cur_el_x_front][next_el_y]["solid"] or my_map[cur_el_x_end][next_el_y]["solid"]) and move[1] > 0:
				move[1] = (next_el_y - 1) * el_size[1] - real_knight_pos[1]
			if (my_map[cur_el_x_front][prev_el_y]["solid"] or my_map[cur_el_x_end][prev_el_y]["solid"]) and move[1] < 0:
				move[1] = (prev_el_y + 1) * el_size[1] - real_knight_pos[1]

			if ((knight_pos[1] + move[1] <= height * (1 - map_movable_area_y) - el_size[1] and
							 knight_pos[1] + move[1] >= height * map_movable_area_y) or
					(knight_pos[1] + move[1] <= height * map_movable_area_y and
							 map_view[1] == 0 and knight_pos[1] + move[1] >= 0) or
					(knight_pos[1] + move[1] >= height * (1 - map_movable_area_y) - el_size[1] and
							 map_view[1] == len(my_map[0]) * el_size[1] - height and knight_pos[1] + move[1] <= height -
						el_size[1])):
				knight_pos[1] += move[1]
			elif len(my_map[0]) * el_size[1] - height >= map_view[1] + move[1] >= 0:
				map_view[1] += move[1]
		

game_input.times_pressed = 0


def draw_monsters():
	global monsters, monster_view, map_view
	for monster in monsters:
		if map_view[0] - (2 * el_size[0]) <= monster.x * el_size[0] <= map_view[0] + width and map_view[1] - (2 * el_size[1]) <= monster.y * el_size[1] <= map_view[1] + height:
			pos = (monster.x * el_size[0] - map_view[0], monster.y * el_size[1] - map_view[1])
			screen.blit(monster.image[int(monster_view)], pos)


def draw_trees():
	global trees, tree_view, map_view, monsters, screen, monsters
	for tree in trees:
		print("rys drzewo")
		if map_view[0] - (3 * el_size[0]) <= tree.x * el_size[0] <= map_view[0] + width and map_view[1] - (4 * el_size[1]) <= tree.y * el_size[1] <= map_view[1] + height:
			print("rysujemy --------------------")
			pos = (tree.x * el_size[0] - map_view[0], tree.y * el_size[1] - map_view[1])
			screen.blit(tree.image[int(tree_view)], pos)
			print("Po narysowaniu  na pos = " + str(tree.x) + ", " + str(el_size[0]) + ", " + str(map_view[0]) + "!!!!!")
			print(str)


def game_draw():
	global screen, background, knight_pos, screen, width, height, image_knight, monster_view, tree_view
	background = create_background(screen, width, height, image_knight)
	screen.blit(background, (0, 0))
	screen.blit(image_knight, (knight_pos[0], knight_pos[1]))
	draw_monsters()
	draw_trees()
	monster_view += 0.125
	tree_view += 0.25
	if monster_view >= 2.0:
		monster_view = 0
	if tree_view >= 8.0:
		tree_view = 0
	pygame.display.flip()


class Monster(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = [pygame.image.load(os.path.join("img/monster/monster_" + str(id) + ".png")) for id in range(1, 3)]


class Tree(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = [pygame.image.load(os.path.join("img/tree/v2_tree-" + str(id) + ".png")) for id in range(8)]


def start_game():
	global my_map, image_knight, global_state, knight_pos, monsters, map_view, move
	global exit_enter_sound_effect, sound_effect_delay
	exit_enter_sound_effect.play()
	pygame.time.wait(sound_effect_delay)
	my_map = create_map()
	image_knight = pygame.image.load(os.path.join("img/rycerz_clear.png"))
	map_view = [16*el_size[0], 9*el_size[1]]
	knight_pos = [7.5*el_size[0], 3.5*el_size[1]]
	move = [0, 0]
	global_state = PLAY_MODE

# 16:9 --> 80px * x

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

el_size = (width / el_horizontal, height / el_vertical)


e1 = [(6, 2), (40, 2), (6, 23), (40, 23)]
e2 = [(17, 3), (29, 3), (17, 22), (29, 22), (4, 12), (42, 12)]
enemies_positions = e1 + e2
monsters = [Monster(pos_x, pos_y) for pos_x, pos_y in enemies_positions]
monster_view = 0.0

t1 = [(23 - 3.625, 10), (27, 10), (23 - 3.625, 14), (27, 14)]
trees_positions = t1
trees = [Tree(pos_x, pos_y) for pos_x, pos_y in trees_positions]
tree_view = 0.0

exit_enter_sound_effect = pygame.mixer.Sound("sounds/enter_exit_sound.wav")
sound_effect_delay = 400

is_alive = True
global_state = MENU_MODE

init_menu()

while is_alive:
	dt = clock.tick(framerate)
	if global_state == 0: #menu
		menu_input()
		menu_draw()
		continue
	if global_state == 1: # ingame
		game_input()
		game_draw()
		continue
