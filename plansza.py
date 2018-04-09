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
def handle_keyboard():
	global move, knight_pos, height, width, times_pressed, clock, size
	is_end_of_game = False
	event_array = pygame.event.get()
	if event_array :
		for event in event_array:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT):
				exit()
			if event.type == pygame.QUIT:
				is_end_of_game = True
			if event.type == pygame.KEYUP:
				times_pressed -= 1
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					move[0] = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					move[1] = 0
			if event.type == pygame.KEYDOWN:
				times_pressed += 1
				if event.key == pygame.K_RIGHT:
					move[0] = 1
				if event.key == pygame.K_LEFT:
					move[0] = -1
				if event.key == pygame.K_UP:
					move[1] = -1
				if event.key == pygame.K_DOWN:
					move[1] = 1
				if width - size[0] > knight_pos[0] + move[0] >= 0 and height - size[1] > knight_pos[1] + move[1] >= 0 :
					knight_pos[0] += move[0]
					knight_pos[1] += move[1]
					print("pos = " + str(knight_pos))
	else :
		clock.tick(120)
		if times_pressed > 0:
			if width - size[0] > knight_pos[0] + move[0] >= 0 and height - size[1] > knight_pos[1] + move[1] >= 0 :
				knight_pos[0] += move[0]
				knight_pos[1] += move[1]
	return is_end_of_game
	

# 16:9 --> 80px * x
clock = pygame.time.Clock()
background_table = create_background_table()
pygame.init()
width = 1280
height = 720
image_knight = pygame.image.load(os.path.join("rycerz_clear.png"))

#tworzymy okno o zadanych wymiarach
screen = pygame.display.set_mode((width, height))
#rysujemy tlo
background = create_background(screen, width, height, image_knight)
knight_pos = [0, 0]
move = [0, 0]
size = (width / 16, height / 9)
is_end_of_game = False
times_pressed = 0

while not is_end_of_game:
	is_end_of_game = handle_keyboard()
	screen.blit(background, (0, 0))
	screen.blit(image_knight, (knight_pos[0] , knight_pos[1]))
	pygame.display.flip()
	
