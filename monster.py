import pygame
import utils
import game_data
import bar_indicator

class Monster(pygame.sprite.DirtySprite):
	def __init__(self, monster_type, path):
		super().__init__()
		self.type = monster_type
		self.damage, self.coin, self.life_max, self.velocity, self.animation_speed \
			= game_data.monsters_stat[monster_type]
		self.life = self.life_max
		self.path = path
		self.path_counter = 1
		self.frame = 0
		self.image = game_data.monsters_images[monster_type][0]
		self.rect = pygame.Rect(path[0], (self.image.get_width(), self.image.get_height()))
		self.bar_indicator = bar_indicator.BarIndicator((50, 5))
		self.bar_indicator.set_value(self.life, self.life_max)
		self.frozen = 0

	def action(self):
		if self.life <= 0:
			return False, False

		if self.rect.center == self.path[self.path_counter]:
			self.path_counter += 1
			if self.path_counter == len(self.path):
				return False, True

		if self.frozen > 0:
			self.frozen -= 1
			return True, False

		delta = utils.line_move(self.rect.center, self.path[self.path_counter], self.velocity)
		self.rect = self.rect.move(*delta)
		self.frame += self.animation_speed
		self.image = game_data.monsters_images[self.type][int(self.frame) % 2]
		self.dirty = 1
		self.bar_indicator.set_rect((self.rect.x, self.rect.y - 5))
		return True, False

	def hurt(self, value):
		self.life -= value
		self.bar_indicator.set_value(self.life, self.life_max)

	def freeze(self, value):
		self.frozen = value
		surf = game_data.effects[0][1]
		new_image = self.image.copy()
		new_image.blit(surf, (0, 0))
		self.image = new_image
		self.dirty = 1