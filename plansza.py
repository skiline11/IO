import pygame
import math
import time
import os.path


# Na razie tworzę sobie taką szachownicę, trzeba będzie wymyśleć jakieś mapki
def create_background_table():
	color_grass = (100, 204, 0)
	color_stone = (156, 156, 156)
	colors = [color_grass, color_stone]

	background_table = [
		[
			{
				"coordinates" : {
					"x": x,
					"y": y
				},
				"color" : colors[(x + y)%2],
			} for x in range(16)
		] for y in range(9)
	]
	
	for x in range(16):
		for y in range(9):
			print(colors[(x+y)%2])
	return background_table


# tworzę okienko i rysuję na nim mapę
def create_background(screen, width, height, image_knight):
	background = pygame.Surface((width, height))
	id_color = 0
	x_pos = 0
	y_pos = 0
	x_size = width / 16
	y_size = height / 9

	for tab in background_table:
		for el in tab:
			pygame.draw.rect(
				background,
				el["color"],
				pygame.Rect(int(el["coordinates"]["x"]) * x_size, int(el["coordinates"]["y"]) * y_size, x_size, y_size)
			)
	return background
	

# obsługuję klawiaturę i poruszam się rycerzem po mapie z uwzględnieniem że nie da się wyjść poza mapę
def game_input():
	global move, knight_pos, height, width, clock, size, is_alive
	event_array = pygame.event.get()
	if event_array :
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
					move[0] = 1
				if event.key == pygame.K_LEFT:
					move[0] = -1
				if event.key == pygame.K_UP:
					move[1] = -1
				if event.key == pygame.K_DOWN:
					move[1] = 1
	else :
		clock.tick(120)

	if game_input.times_pressed > 0:
		if width - size[0] > knight_pos[0] + move[0] >= 0 and height - size[1] > knight_pos[1] + move[1] >= 0 :
			knight_pos[0] += move[0]
			knight_pos[1] += move[1]
		print("pos = " + str(knight_pos))


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


knight_pos = [0, 0]
move = [0, 0]
size = (width / 16, height / 9)


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
