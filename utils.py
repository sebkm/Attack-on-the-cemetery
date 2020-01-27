import pygame
import math


def line_move(src, dst, velocity):
	"""return vx, vy such that src[0] + vx, src[1] + vy is at least velocity closer to dst"""

	xi, yi = src
	xj, yj = dst
	vx = min(velocity, abs(xi - xj))
	vy = min(velocity, abs(yi - yj))
	vx = vx if xi < xj else -vx
	vy = vy if yi < yj else -vy
	return vx, vy


def distance(src, dst):
	"""return the Euclidean distance between src and dst"""

	return math.sqrt(abs(dst[0] - src[0]) ** 2 + abs(dst[1] - src[1]) ** 2)


def angle(src, dst):
	"""return the angle between src and dst assuming (0, 0) is the top left corner"""

	centerX, centerY = dst
	x, y = src
	return -math.degrees(math.atan2(y - centerY, x - centerX))


def load_sprite_sheet(name, sprite_size):
	"""return a list of Surfaces
	name designate a sprite sheet
	each Surface from the returned list is of size sprite_size
	"""

	sprite_sheet = pygame.image.load(name).convert_alpha()
	w = sprite_sheet.get_width()
	h = sprite_sheet.get_height()
	n, m = sprite_size
	ni = h // m
	nj = w // n
	images = [None] * ni

	for i in range(ni):
		images[i] = [None] * nj
		for j in range(nj):
			rect = pygame.Rect((j * n, i * m), sprite_size)
			image: pygame.Surface = pygame.Surface(sprite_size).convert_alpha()
			image.fill(255)
			image.blit(sprite_sheet, (0, 0), rect)
			images[i][j] = image
	return images
