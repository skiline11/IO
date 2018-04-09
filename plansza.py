import pygame
import math
import time
import os.path


el_horizontal = 16
el_vertical = 9


def create_map():
	color_grass = (100, 204, 0)
	color_stone = (156, 156, 156)
	color_monster = (255, 0, 0)
	color_end_of_map = (0, 0, 0)
	colors = {"grass": color_grass, "stone": color_stone, "monster": color_monster, "end_of_map": color_end_of_map}

	# mapa pełna kamieni
	my_map = [
		[
			{
				"color": colors["grass"]
			} for y in range(27)
		] for x in range(48)
	]

	# dodaje przeciwnikow
	e1 = [(6, 2), (40, 2), (6, 23), (40, 23)]
	e2 = [(17, 3), (29, 3), (17, 22), (29, 22), (4, 12), (42, 12)]
	enemies_positions = e1 + e2
	for pos_x, pos_y in enemies_positions:
		for x in range(2):
			for y in range(2):
				my_map[pos_x + x][pos_y + y]["color"] = colors["monster"]

	#dodaje kamienie
	s1 = []
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
	for y in range(27):
		for x in [0, 47]:
			my_map[x][y]["color"] = colors["end_of_map"]

	return my_map



# tworzę okienko i rysuję na nim mapę
def create_background(screen, width, height, image_knight):
	global my_map, el_horizontal, el_vertical
	background = pygame.Surface((width, height))

	id_color = 0
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
				background,
				el["color"],
				pygame.Rect(int(x) * el_size[0] - x_remainder, int(y) * el_size[1] - y_remainder, el_size[0], el_size[1])
			)
	return background
	

# obsługuję klawiaturę i poruszam się rycerzem po mapie z uwzględnieniem że nie da się wyjść poza mapę
def game_input():
	move_val = 5
	global move, knight_pos, height, width, clock, el_size, is_alive, my_map
	map_movable_area = 0.1
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
				if event.key == pygame.K_RIGHT:
					move[0] = move_val
				if event.key == pygame.K_LEFT:
					move[0] = -move_val
				if event.key == pygame.K_UP:
					move[1] = -move_val
				if event.key == pygame.K_DOWN:
					move[1] = move_val
	else:
		clock.tick(120)
	if game_input.times_pressed > 0:

		# jeśli znajdujemu się wystarczająco daleko od brzegów planszy to nie będziemy przesówać jej widoku
		# tylko przesuniemy się rycerzem
		if ((knight_pos[0] + move[0] <= width *(1-map_movable_area) - el_size[0] and
			knight_pos[0] + move[0] >= width * map_movable_area) or
			(knight_pos[0] + move[0] <= width * map_movable_area and
			 map_view[0]==0 and knight_pos[0] + move[0] >= 0) or
			(knight_pos[0] + move[0] >= width *(1-map_movable_area) - el_size[0] and 
			 map_view[0]==len(my_map)*el_size[0]-width and knight_pos[0] + move[0] <= width - el_size[0])
			):
			knight_pos[0] += move[0]
		elif len(my_map)*el_size[0]-width >= map_view[0] + move[0] >= 0:
			map_view[0] += move[0]
			
		if ((knight_pos[1] + move[1] <= height*(1-map_movable_area) - el_size[1] and 
			 knight_pos[1] + move[1] >= height*map_movable_area) or
			(knight_pos[1] + move[1] <= height*map_movable_area and 
			 map_view[1]==0 and knight_pos[1] + move[1] >= 0) or
			(knight_pos[1] + move[1] >= height*(1-map_movable_area) - el_size[1] and 
			 map_view[1]==len(my_map[0])*el_size[1]-height and knight_pos[1] + move[1] <= height - el_size[1])):
				knight_pos[1] += move[1]
		elif len(my_map[0])*el_size[1]-height >= map_view[1] + move[1] >= 0:
			map_view[1] += move[1]
		

game_input.times_pressed = 0

def game_draw():
	global screen, background, knight_pos, screen, width, height, image_knight
	background = create_background(screen, width, height, image_knight)
	screen.blit(background, (0, 0))
	screen.blit(image_knight, (knight_pos[0] , knight_pos[1]))
	pygame.display.flip()

def start_game():
	global my_map, image_knight, global_state
	global_state = 1
	# my_map = create_background_table()
	my_map = create_map()
	image_knight = pygame.image.load(os.path.join("rycerz_clear.png"))

# 16:9 --> 80px * x

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

map_view = [50, 50]
knight_pos = [200, 200]
knight_pos_real = [0, 0]
move = [0, 0]
el_size = (width / el_horizontal, height / el_vertical)


is_alive = True
global_state = 0

start_game()

while is_alive:
	if global_state == 0: #menu
		menu_input()
		menu_draw()
		continue
	if global_state == 1: # ingame
		game_input()
		game_draw()
		continue
