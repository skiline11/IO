import pygame
import colors

pygame.init()


def mouse_over(pos, size):
	mouse_pos = pygame.mouse.get_pos()
	if pos[0] < mouse_pos[0] < pos[0] + size[0] and pos[1] < mouse_pos[1] < pos[1] + size[1]:
		return True
	else:
		return False


class Font:
	Default = pygame.font.SysFont("Verdana", 20)
	Small = pygame.font.SysFont("Verdana", 15)
	Medium = pygame.font.SysFont("Verdana", 40)
	Large = pygame.font.SysFont("Verdana", 60)
	Scanner = pygame.font.SysFont("Verdana", 30)


class Button:
	all = []

	def __init__(self, pos, size, color, hicol, func, text="EMPTY", font=Font.Default):
		self.text = text
		self.left = pos[0]
		self.top = pos[1]
		self.width = size[0]
		self.height = size[1]
		self.is_active = False
		self.event_handler = func

		# Unhighlightened button
		self.normal = pygame.Surface((self.width, self.height), pygame.HWSURFACE|pygame.SRCALPHA)
		self.normal.fill(color)
		rendered_txt = font.render(text, True, colors.Colors.BLACK)
		text_rect = rendered_txt.get_rect()
		self.normal.blit(rendered_txt, (self.width / 2 - text_rect[2] / 2, self.height / 2 - text_rect[3] / 2))

		# Highlightened button
		self.active = pygame.Surface((self.width, self.height), pygame.HWSURFACE | pygame.SRCALPHA)
		self.active.fill(hicol)
		self.active.blit(rendered_txt, (self.width / 2 - text_rect[2] / 2, self.height / 2 - text_rect[3] / 2))

		Button.all.append(self)

	def render(self, to, pos=(0, 0)):
		if mouse_over((self.left + pos[0], self.top + pos[1]), (self.width, self.height)):
			to.blit(self.active, (self.left + pos[0], self.top + pos[1]))
			self.is_active = True
		else:
			to.blit(self.normal, (self.left + pos[0], self.top + pos[1]))
			self.is_active = False

	def pressed(self):
		self.event_handler()
