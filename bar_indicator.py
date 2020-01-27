import pygame


class BarIndicator(pygame.sprite.DirtySprite):
	def __init__(self, size):
		super().__init__()
		self.size = size
		self.image = None
		self.rect = None

	def set_value(self, val, max_val):
		filled = (self.size[0] * val) // max_val
		self.image = pygame.Surface((self.size[0], self.size[1])).convert_alpha()
		self.image.fill(255)
		pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect((0, 0), (self.size[0], self.size[1])), 1)
		if filled != 0:
			pygame.draw.rect(self.image, (0, 255, 0), pygame.Rect((1, 1), (filled - 2, self.size[1] - 2)), 0)
		self.dirty = 1

	def set_rect(self, position):
		self.rect = pygame.Rect(position, (self.size[0], self.size[1]))
		self.dirty = 1
