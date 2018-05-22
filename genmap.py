import random

def daj_plansze():
	plansza = []
	for x in range(48):
		kolumna = []
		for y in range(27):
			kolumna.append({"znak": '.'})
		plansza.append(kolumna)

	# print(plansza[44][20])

	pozycje_przeciwnikow = []
	for i in range(10):
		udalo_sie = False
		ile_razy_prubowalem = 0
		while udalo_sie == False and ile_razy_prubowalem < 10:
			udalo_sie = True
			x = random.randint(1, 45)
			y = random.randint(1, 24)
			for pos_x, pos_y in pozycje_przeciwnikow:
				dif_x = pos_x - x
				dif_y = pos_y - y
				if(not (dif_x <= -10 or dif_x >= 10 or dif_y <= -10 or dif_y >= 10)):
					udalo_sie = False
			ile_razy_prubowalem += 1

		if ile_razy_prubowalem < 10:
			pozycje_przeciwnikow.append((x, y))
			plansza[x][y]["znak"] = 'P'

	# print("plansza1")
	# for y in range(27):
	# 	line = ""
	# 	for x in range(48):
	# 		line += plansza[x][y]["znak"]
	# 		line += plansza[x][y]["znak"]
	# 	print(line)
	# 	print(line)


	# print("plansza2")
	for los in range(20):
		pos1 = pozycje_przeciwnikow[random.randint(0, len(pozycje_przeciwnikow) - 1)]
		pos2 = pozycje_przeciwnikow[random.randint(0, len(pozycje_przeciwnikow) - 1)]
		if pos1[0] < pos2[0]:
			l = pos1[0]
			r = pos2[0]
		else:
			l = pos2[0]
			r = pos1[0]

		if pos1[1] < pos2[1]:
			u = pos1[1]
			d = pos2[1]
		else:
			u = pos2[1]
			d = pos1[1]
		for x in range(l, r+1):
			if plansza[x][u]["znak"] != "P":
				plansza[x][u]["znak"] = "S"
		for y in range(u, d+1):
			if (
				(pos1[0] == l and pos1[1] == u and pos2[0] == r and pos2[1] == d)
				or (pos2[0] == l and pos2[1] == u and pos1[0] == r and pos1[1] == d)
			):
				if plansza[r][y]["znak"] != "P":
					plansza[r][y]["znak"] = "S"
			else:
				if plansza[l][y]["znak"] != "P":
					plansza[l][y]["znak"] = "S"

	# dodajemy 20 ammo na plansze
	pozycje_ammo = []
	for id in range(20):
		x = random.randint(1, 45)
		y = random.randint(1, 24)
		if plansza[x][y]["znak"] == "P":
			id -= 1
		else:
			plansza[x][y]["znak"] = "ammo"
			pozycje_ammo.append((x, y))

	pozycje_ball = []
	done = False
	while not done:
		x = random.randint(1, 43)
		y = random.randint(1, 22)
		done = True
		for vert in range(4):
			for hor in range(4):
				if plansza[int(x + vert)][int(y + hor)]["znak"] == "P" or plansza[int(x + vert)][int(y + hor)][
					"znak"] == "ammo":
					done = False
		if done:
			plansza[x][y]["znak"] = "ball"
			pozycje_ball.append((x, y))

	pozycje_questionmark = []
	for i in range(5):
		x = random.randint(1, 47)
		y = random.randint(1, 26)
		udalo_sie = True
		if plansza[x][y]["znak"] == ".":
			for vert in range(4):
				for hor in range(4):
					if x + vert < 48 and y + hor < 27:
						try:
							if plansza[x + vert][y + hor]["znak"] == "ball":
								udalo_sie = False
						except IndexError:
							print("Wywaliło błąd dla x = " + str(x) + ", vert = " + str(vert) + ", y = " + str(
								y) + ", hor = " + str(hor))
							exit()
		if udalo_sie:
			plansza[x][y]["znak"] = "?"
			pozycje_questionmark.append((x, y))
		else:
			i -= 1

	return {"plansza": plansza, "enemies_pos": pozycje_przeciwnikow, "ammo_pos": pozycje_ammo, "ball_pos": pozycje_ball, "questionmark_pos": pozycje_questionmark}

	# for y in range(27):
	# 	line = ""
	# 	for x in range(48):
	# 		line += plansza[x][y]["znak"]
	# 		line += plansza[x][y]["znak"]
	# 	print(line)
	# 	print(line)
