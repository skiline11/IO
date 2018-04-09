import pygame
import math
import time
import os.path


el_horizontal = 16
el_vertical = 9

# Na razie tworzę sobie taką szachownicę, trzeba będzie wymyśleć jakieś mapki
def create_background_table():
	color_grass = (100, 204, 0)
	color_stone = (156, 156, 156)

	color_grass2 = (255, 204, 0)
	color_stone2 = (255, 156, 156)
	colors = [color_grass, color_stone, color_grass2, color_stone2]

	background_table = [
		(
			[{"color" : colors[2+(x + y)%2]} for x in range(el_horizontal)]+
			[{"color" : colors[(x + y)%2]} for x in range(el_horizontal)]
		) for y in range(el_vertical)
	]
	background_table += [
		(
			[{"color" : colors[(1+x + y)%2]} for x in range(el_horizontal)]+
			[{"color" : colors[2+(1+x + y)%2]} for x in range(el_horizontal)]
		) for y in range(el_vertical)
	]
	
	return background_table


# tworzę okienko i rysuję na nim mapę
def create_background(screen, width, height, image_knight):
	global background_table, el_horizontal, el_vertical
	background = pygame.Surface((width, height))

	id_color = 0
	x_offset = int(map_view[0]/el_size[0])
	y_offset = int(map_view[1]/el_size[1])
	x_remainder = map_view[0]%el_size[0]
	y_remainder = map_view[1]%el_size[1]
	

	for x in range(el_horizontal+1):
		for y in range(el_vertical+1):
			if y+y_offset >= len(background_table):
				continue
			if x+x_offset >= len(background_table[y+y_offset]):
				continue
			el = background_table[y+y_offset][x+x_offset]
			pygame.draw.rect(
				background,
				el["color"],
				pygame.Rect(int(x) * el_size[0] - x_remainder, int(y) * el_size[1] - y_remainder, el_size[0], el_size[1])
			)
	return background
	

# obsługuję klawiaturę i poruszam się rycerzem po mapie z uwzględnieniem że nie da się wyjść poza mapę
def game_input():
	move_val = 5
	global move, knight_pos, height, width, clock, el_size, is_alive
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
		knight_pos_real[0]
		if (width *(1-map_movable_area) - el_size[0] >= knight_pos[0] + move[0] >= width *map_movable_area):
			knight_pos[0] += move[0]
		else:
			print("map_move_x")
		#else if( >= map_view[0] + move[0] >= 0):
		#	map_view[0] += move[0]; 
			
		if (height*(1-map_movable_area) - el_size[1] >= knight_pos[1] + move[1] >= height*map_movable_area):
			knight_pos[1] += move[1]
		else:
			print("map_move_y")

game_input.times_pressed = 0

def game_draw():
	global screen, background, knight_pos, screen, width, height, image_knight
	background = create_background(screen, width, height, image_knight)
	screen.blit(background, (0, 0))
	screen.blit(image_knight, (knight_pos[0] , knight_pos[1]))
	pygame.display.flip()

def start_game():
	global background_table, image_knight, global_state
	global_state = 1
	background_table = create_background_table()
	image_knight = pygame.image.load(os.path.join("rycerz_clear.png"))

# 16:9 --> 80px * x

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

map_view = [50,50]
knight_pos = [200, 200]
knight_pos_real = [0,0]
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
