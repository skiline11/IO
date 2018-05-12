import pygame
import os
import game as gm


class Question:
	MAX = 5
	IMAGE = [pygame.image.load(os.path.join("img/question_mark/frame_" + str(i)) + "_delay-0.05s.png") for i in range(18)]
	FRAME_COUNT = 18
	ANIMATION_SLOWDOWN = 3

	def __init__(self, pos):
		self.pos = pos
		self.frame = 0
		self.anim_mod = 0

	def draw_mark(self, screen, map_view):
		if (map_view[0] - (3 * gm.el_size[0]) <= self.pos[0] * gm.el_size[0] <= map_view[0] + gm.width) and \
			(map_view[1] - (4 * gm.el_size[1]) <= self.pos[1] * gm.el_size[1] <= map_view[1] + gm.height):

				self.frame = (self.frame + self.anim_mod // Question.ANIMATION_SLOWDOWN) % Question.FRAME_COUNT
				self.anim_mod = (self.anim_mod + 1) % (Question.ANIMATION_SLOWDOWN + 1)
				pos = (self.pos[0] * gm.el_size[0] - map_view[0], self.pos[1] * gm.el_size[1] - map_view[1])
				screen.blit(Question.IMAGE[self.frame], pos)

