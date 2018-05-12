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


def draw_text(screen, x, y, text):
	rendered_txt = Font.Default.render(text, True, colors.Colors.WHITE)
	text_rect = rendered_txt.get_rect()
	screen.blit(rendered_txt, (x, y))


class Button:
	# TODO modifiable font color
	def __init__(self, pos, size, color, hicol, func, text="EMPTY", font=Font.Default):
		self.text = text
		self.left = pos[0]
		self.top = pos[1]
		self.width = size[0]
		self.height = size[1]
		self.is_active = False
		self.event_handler = func

		# Unhighlightened button
		self.normal = pygame.Surface((self.width, self.height), pygame.HWSURFACE | pygame.SRCALPHA)
		self.normal.fill(color)
		rendered_txt = font.render(text, True, colors.Colors.WHITE)
		text_rect = rendered_txt.get_rect()
		self.normal.blit(rendered_txt, (self.width / 2 - text_rect[2] / 2, self.height / 2 - text_rect[3] / 2))

		# Highlightened button
		self.active = pygame.Surface((self.width, self.height), pygame.HWSURFACE | pygame.SRCALPHA)
		self.active.fill(hicol)
		self.active.blit(rendered_txt, (self.width / 2 - text_rect[2] / 2, self.height / 2 - text_rect[3] / 2))

	def render(self, to, pos=(0, 0)):
		if mouse_over((self.left + pos[0], self.top + pos[1]), (self.width, self.height)):
			to.blit(self.active, (self.left + pos[0], self.top + pos[1]))
			self.is_active = True
		else:
			to.blit(self.normal, (self.left + pos[0], self.top + pos[1]))
			self.is_active = False

	def pressed(self):
		self.event_handler()


class Text:
	def __init__(self, text, font=Font.Default, color=colors.Colors.WHITE, bg=None):
		self.text = text
		self.font = font
		self.color = color
		self.left = 0
		self.top = 0
		self.bg = bg

		bitmap = font.render(text, True, color)
		self.bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
		if bg is not None:
			self.bitmap.fill(bg)
		self.bitmap.blit(bitmap, (0, 0))

	def render(self, surface, pos, size):
		words = [word.split(' ') for word in self.text.splitlines()]
		space = self.font.size(' ')[0]  # The width of a space.
		max_width, max_height = surface.get_size()
		x, y = pos
		self.bitmap = pygame.Surface(size, pygame.SRCALPHA | pygame.HWSURFACE)
		if self.bg is not None:
			self.bitmap.fill(self.bg)
		for line in words:
			for word in line:
				word_surface = self.font.render(word, True, self.color)
				word_width, word_height = word_surface.get_size()
				if x + word_width >= max_width or x + word_width >= size[0]:  # New line.
					x = pos[0]
					y += word_height
				self.bitmap.blit(word_surface, (x, y))
				x += word_width + space
			x = pos[0]  # Reset the x.
			y += word_height  # Start on new row.

		surface.blit(self.bitmap, pos)
