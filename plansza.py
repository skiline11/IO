import pygame
import math
import time
import os.path
import os
import copy
from colors import Colors
from gui import Button, draw_text, Text
from objects import Monster, Tree, Knight, Map
import pickle
import question as quest
import game as gm


el_horizontal = 16
el_vertical = 9
framerate = 60
PLAY_MODE = 1
MENU_MODE = 0
MENU_LOAD_MODE = 2
menu_obj = []
menu_savegame_buttons = []
collidable_objects = []

sprites = {}
sprites['Monster'] = [pygame.image.load(os.path.join("img/monster/monster_" + str(id) + ".png")) for id in range(1, 3)]
sprites['Tree'] = [pygame.image.load(os.path.join("img/tree/v2_tree-" + str(id) + ".png")) for id in range(8)]
sprites['Knight'] = [pygame.image.load(os.path.join("img/knight/rycerz_clear.png"))]


# tworzę okienko i rysuję na nim mapę
def create_background(screen, width, height):
	global el_horizontal, el_vertical
	new_background = pygame.Surface((width, height))

	x_offset = int(map_view[0]/el_size[0])
	y_offset = int(map_view[1]/el_size[1])
	x_remainder = map_view[0]%el_size[0]
	y_remainder = map_view[1]%el_size[1]

	for x in range(el_horizontal+1):
		for y in range(el_vertical+1):
			if x+x_offset >= len(my_map.map):
				continue
			if y+y_offset >= len(my_map.map[x+x_offset]):
				continue
			el = my_map.map[x+x_offset][y+y_offset]
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
	horizontal = width / 2 - (button_width*2+50) / 2 - 100
	vertical = height / 2 - button_height / 2 + 250
	menu_obj.append(Button((horizontal, vertical), (button_width, button_height), Colors.BLACK, Colors.RED, start_game, "PLAY"))
	menu_obj.append(Button((horizontal+300, vertical), (button_width, button_height), Colors.BLACK, Colors.RED, go_to_load_menu, "LOAD"))
	image_menu = pygame.image.load(os.path.join("img/menu.jpg"))
	pygame.mixer.music.load('sounds/soundtrack.mp3')
	pygame.mixer.music.play(-1)


def menu_draw():
	global screen, image_menu, go_to_menu_mode

	screen.blit(image_menu, (0, 0))
	for obj in menu_obj:
		obj.render(screen)

	if go_to_menu_mode == True:
		go_to_menu_mode = False

	''' #TEXT RENDERING TEST
	text = Text(
		"This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
        "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
        "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
        "text will disappear underneath the surface", bg=Colors.BLUE)
	text.render(screen, (20,20), (400, 400))'''

	pygame.display.flip()


def menu_input():
	global is_alive, clock, go_to_play_mode, menu_buttons, menu_obj
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
			is_alive = False
		if event.type == pygame.QUIT:
			is_alive = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: # Left click
				for button in menu_obj:
					if button.is_active:
						button.pressed()
						go_to_play_mode = True
						button.is_active = False
						break
	clock.tick(framerate)


def menu_load_draw():
	global screen, image_menu_load, menu_savegame_buttons, go_to_menu_mode

	screen.blit(image_menu, (0, 0))
	for obj in menu_savegame_buttons:
		obj.render(screen)
	if go_to_menu_mode == False:
		pygame.display.flip()

def load_game_file(f):
	global knight, my_map, map_view, move, global_state, go_to_play_mode, collidable_objects
	with open('./savedgames/'+f, 'rb') as pickle_file:
		game_save = pickle.load(pickle_file)
		knight = game_save[0]
		my_map = game_save[1]
		map_view = game_save[2]
	exit_enter_sound_effect.play()
	pygame.time.wait(sound_effect_delay)
	collidable_objects = my_map.monsters
	move = [0, 0]
	global_state = PLAY_MODE
	go_to_play_mode = True


def save_game_file(f):
	with open(f, 'wb') as pickle_file:
		game_save = [knight, my_map, map_view]
		pickle.dump(game_save, pickle_file)

def go_to_menu():
	global go_to_menu_mode, global_state
	exit_enter_sound_effect.play()
	pygame.time.wait(sound_effect_delay)
	global_state = MENU_MODE

def go_to_load_menu():
	global global_state
	exit_enter_sound_effect.play()
	pygame.time.wait(sound_effect_delay)
	global_state = MENU_LOAD_MODE

def menu_load_input():
	global is_alive, clock, go_to_menu_mode, go_to_play_mode, menu_savegame_buttons, global_state

	if menu_load_input.how_many_frames_since_last_refresh > 30:
		vert = 50
		menu_savegame_buttons = [Button((25, vert), (500, 30), Colors.BLACK, Colors.RED, go_to_menu, "Menu główne")]
		vert += 40
		for file in os.listdir("./savedgames"):
			if file.endswith(".txt"):
				menu_savegame_buttons.append(Button((25, vert), (500, 30), Colors.BLACK,
											Colors.RED, lambda b_f=file: load_game_file(b_f), os.path.splitext(file)[0]))
				vert += 40
		menu_load_input.how_many_frames_since_last_refresh = 0
	menu_load_input.how_many_frames_since_last_refresh += 1

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
			is_alive = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			go_to_menu()
		if event.type == pygame.QUIT:
			is_alive = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: # Left click
				for button in menu_savegame_buttons:
					if button.is_active:
						button.pressed()
						go_to_play_mode = True
						button.is_active = False
						break
	clock.tick(framerate)
menu_load_input.how_many_frames_since_last_refresh = 60


# obsługuję klawiaturę i poruszam się rycerzem po mapie z uwzględnieniem że nie da się wyjść poza mapę
def game_input():
	move_val = 10
	global knight
	global move, height, width, clock, el_size, is_alive, my_map, global_state
	global exit_enter_sound_effect, sound_effect_delay, go_to_menu_mode
	global screen
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
				if event.key == pygame.K_RETURN:
					save_game_file('./savedgames/test.txt')
			if event.type == pygame.KEYDOWN:
				game_input.times_pressed += 1
				if event.key == pygame.K_ESCAPE:
					exit_enter_sound_effect.play()
					pygame.time.wait(sound_effect_delay)
					for y in range(int(height/20)):
						screen.blit(image_menu, (0, y*20 - height))
						pygame.display.flip()
						pygame.time.wait(1)
					global_state = MENU_MODE
					go_to_menu_mode = True
				if event.key == pygame.K_RIGHT:
					move[0] = move_val
				if event.key == pygame.K_LEFT:
					move[0] = -move_val
				if event.key == pygame.K_UP:
					move[1] = -move_val
				if event.key == pygame.K_DOWN:
					move[1] = move_val

	real_knight_pos = [0, 0]
	real_knight_pos[0] = knight.x + map_view[0]
	real_knight_pos[1] = knight.y + map_view[1]

	if game_input.times_pressed > 0:
		# print("tutaj")
		# jeśli znajdujemu się wystarczająco daleko od brzegów planszy to nie będziemy przesówać jej widoku
		# tylko przesuniemy się rycerzem
		# print(real_knight_pos)
		cur_el_x_front = int((real_knight_pos[0]) / el_size[0])
		cur_el_x_end = int((real_knight_pos[0] + el_size[0] - 1) / el_size[0])
		next_el_y = int((real_knight_pos[1] + el_size[1] + move[1]) / el_size[1])
		prev_el_y = int((real_knight_pos[1] + move[1]) / el_size[1])

		cur_el_y_top = int((real_knight_pos[1]) / el_size[1])
		cur_el_y_bottom = int((real_knight_pos[1] + el_size[1] - 1) / el_size[1])
		next_el_x = int((real_knight_pos[0] + el_size[0] + move[0]) / el_size[0])
		prev_el_x = int((real_knight_pos[0] + move[0]) / el_size[0])

		if move[0] != 0 or move[1] != 0:
			for col in collidable_objects:
				move = col.collide(knight, move, map_view)


		if move[0] != 0:
			# print("poziomo")
			if (my_map.map[next_el_x][cur_el_y_top]["solid"] or my_map.map[next_el_x][cur_el_y_bottom]["solid"]) and move[
				0] > 0:
				move[0] = (next_el_x - 1) * el_size[0] - real_knight_pos[0]
			if (my_map.map[prev_el_x][cur_el_y_top]["solid"] or my_map.map[prev_el_x][cur_el_y_bottom]["solid"]) and move[
				0] < 0:
				move[0] = (prev_el_x + 1) * el_size[0] - real_knight_pos[0]

			if ((knight.x + move[0] <= width * (1 - map_movable_area_x) - el_size[0] and
							 knight.x + move[0] >= width * map_movable_area_x) or
					(knight.x + move[0] <= width * map_movable_area_x and
							 map_view[0] == 0 and knight.x + move[0] >= 0) or
					(knight.x + move[0] >= width * (1 - map_movable_area_x) - el_size[0] and
							 map_view[0] == len(my_map.map) * el_size[0] - width and knight.x + move[0] <= width -
						el_size[0])):
				knight.x += move[0]
			elif len(my_map.map) * el_size[0] - width >= map_view[0] + move[0] >= 0:
				map_view[0] += move[0]

		if move[1] != 0:
			# print("pionowo")
			if (my_map.map[cur_el_x_front][next_el_y]["solid"] or my_map.map[cur_el_x_end][next_el_y]["solid"]) and move[1] > 0:
				move[1] = (next_el_y - 1) * el_size[1] - real_knight_pos[1]
			if (my_map.map[cur_el_x_front][prev_el_y]["solid"] or my_map.map[cur_el_x_end][prev_el_y]["solid"]) and move[1] < 0:
				move[1] = (prev_el_y + 1) * el_size[1] - real_knight_pos[1]

			if ((knight.y + move[1] <= height * (1 - map_movable_area_y) - el_size[1] and
							 knight.y + move[1] >= height * map_movable_area_y) or
					(knight.y + move[1] <= height * map_movable_area_y and
							 map_view[1] == 0 and knight.y + move[1] >= 0) or
					(knight.y + move[1] >= height * (1 - map_movable_area_y) - el_size[1] and
							 map_view[1] == len(my_map.map[0]) * el_size[1] - height and knight.y + move[1] <= height -
						el_size[1])):
				knight.y += move[1]
			elif len(my_map.map[0]) * el_size[1] - height >= map_view[1] + move[1] >= 0:
				map_view[1] += move[1]


game_input.times_pressed = 0


def draw_monsters():
	global my_map, monster_view, map_view, screen
	for monster in my_map.monsters:
		if map_view[0] - (2 * el_size[0]) <= monster.x * el_size[0] <= map_view[0] + width and map_view[1] - (2 * el_size[1]) <= monster.y * el_size[1] <= map_view[1] + height:
			pos = (monster.x * el_size[0] - map_view[0], monster.y * el_size[1] - map_view[1])
			screen.blit(sprites[monster.type][int(monster_view)], pos)


def draw_trees():
	global my_map, tree_view, map_view, monsters, screen, monsters
	for tree in my_map.trees:
		# print("rys drzewo")
		if map_view[0] - (3 * el_size[0]) <= tree.x * el_size[0] <= map_view[0] + width and map_view[1] - (4 * el_size[1]) <= tree.y * el_size[1] <= map_view[1] + height:
			# print("rysujemy --------------------")
			pos = (tree.x * el_size[0] - map_view[0], tree.y * el_size[1] - map_view[1])
			screen.blit(sprites[tree.type][int(tree_view)], pos)
			# print("Po narysowaniu  na pos = " + str(tree.x) + ", " + str(el_size[0]) + ", " + str(map_view[0]) + "!!!!!")


def game_draw():
	global knight
	global screen, background, width, height, monster_view, tree_view, map_view, my_map
	global go_to_play_mode, go_to_menu_mode
	background = create_background(screen, width, height)
	screen.blit(background, (0, 0))
	screen.blit(sprites[knight.type][0], (knight.x, knight.y))
	draw_monsters()
	draw_trees()
	my_map.draw_question_marks(screen, map_view)

	draw_text(screen, 2, 0, 'Remaining HP: ' + str(knight.life) + '/100')
	if knight.life < 1:
		print('The player died!')
		go_to_menu()

	monster_view += 0.125
	tree_view += 0.25
	if monster_view >= 2.0:
		monster_view = 0
	if tree_view >= 8.0:
		tree_view = 0

	# print("go to play mode = " + str(go_to_play_mode))
	if go_to_play_mode == True:
		# print("................z true")
		go_to_play_mode = False

		# wyświetlam animację znikania menu
		for y in range(int(height / 20)):
			screen.blit(background, (0, 0))
			screen.blit(sprites[knight.type][0], (knight.x, knight.y))
			draw_monsters()
			draw_trees()
			my_map.draw_question_marks(screen, map_view)


			screen.blit(image_menu, (0, y * (-20.0)))
			pygame.display.flip()
			pygame.time.wait(1)
	elif go_to_menu_mode == False:
		# print("................z false")
		pygame.display.flip()


def start_game():
	global my_map, global_state, monsters, map_view, move, width, height, collidable_objects
	global exit_enter_sound_effect, sound_effect_delay, go_to_play_mode, knight
	exit_enter_sound_effect.play()
	pygame.time.wait(sound_effect_delay)
	my_map = Map()
	collidable_objects = my_map.monsters
	map_view = [16*el_size[0], 9*el_size[1]]
	move = [0, 0]
	knight = Knight(7.5*el_size[0], 3.5*el_size[1], el_size[0], el_size[1])
	global_state = PLAY_MODE
	go_to_play_mode = True

# 16:9 --> 80px * x

pygame.init()


width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

el_size = (width / el_horizontal, height / el_vertical)



# e1 = [(6, 2), (40, 2), (6, 23), (40, 23)]
# e2 = [(17, 3), (29, 3), (17, 22), (29, 22), (4, 12), (42, 12)]
# enemies_positions = e1 + e2
# monsters = [Monster(pos_x, pos_y) for pos_x, pos_y in enemies_positions]
monster_view = 0.0

# t1 = [(23 - 3.625, 10), (27, 10), (23 - 3.625, 14), (27, 14)]
# trees_positions = t1
# trees = [Tree(pos_x, pos_y) for pos_x, pos_y in trees_positions]
tree_view = 0.0

exit_enter_sound_effect = pygame.mixer.Sound("sounds/enter_exit_sound.wav")
sound_effect_delay = 400

is_alive = True
global_state = MENU_MODE

#potrzebuję tych zmiennych do wyświetlania animacji pojawiania się i znikania menu
go_to_play_mode = False
go_to_menu_mode = False

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
	if global_state == 2: # load screen
		menu_load_input()
		menu_load_draw()
		continue
