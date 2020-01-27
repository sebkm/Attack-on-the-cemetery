import pygame
import projectile
import gui
import game_data
import utils
import bar_indicator


class Building(pygame.sprite.DirtySprite, gui.Mouse_trigger):
	def __init__(self, position):
		super().__init__()
		self.type = None
		self.level = 0
		self.level_max = 3
		self.damage, self.radius, self.reload_time = 0, 50, 0
		self.reload = 0
		self.position = position
		self.base_image = game_data.new_building_image
		self.image = self.base_image
		self.rect = pygame.Rect(position, (75, 75))
		self.bar_indicator = None

	def action(self, monsters):
		if self.type is None:
			return None

		if self.reload > 0:
			self.reload -= 1
			self.bar_indicator.set_value(self.reload_time - self.reload, self.reload_time)
			return None

		best, target = float("inf"), None
		src = self.rect.center
		for monster in monsters:
			dist = utils.distance(src, monster.rect.center)
			if dist < best:
				best, target = dist, monster

		if target is not None and best <= self.radius:
			if self.type == 0 or self.type == 1:
				p = projectile.Arrow(self.position, target, self.damage)
			elif self.type == 2:
				p = projectile.FireBall(self.position, target, self.damage)
			else:  # self.type == 3
				p = projectile.IceBall(self.position, target, self.damage)
			self.reload = self.reload_time
			return p
		return None

	def upgrade(self):
		self.hover_off()
		self.reload = 0
		self.damage, self.radius, self.reload_time = \
			game_data.buildings_stat[self.type][self.level]
		self.base_image = game_data.buildings_images[self.type][self.level]
		self.image = self.base_image
		self.level += 1

		if self.bar_indicator is None:
			self.bar_indicator = bar_indicator.BarIndicator((75, 10))
			self.bar_indicator.set_rect((self.rect.x, self.rect.y - 10))
		self.bar_indicator.set_value(self.reload_time, self.reload_time)

	def sell(self):
		self.hover_off()
		self.type = None
		self.level = 0
		self.damage, self.radius, self.reload_time = 0, 50, 0
		self.reload = 0
		self.base_image = game_data.new_building_image
		self.image = self.base_image

	def hover_on(self):
		r = self.radius
		d = r * 2
		new_pos = self.rect.centerx - r, self.rect.centery - r
		bx, by = r - self.base_image.get_width() // 2, r - self.base_image.get_height() // 2
		surf = pygame.Surface((d, d)).convert_alpha()
		surf.fill(255)
		pygame.draw.circle(surf, (199, 180, 20, 75), (r, r), r)
		surf.blit(self.base_image, (bx, by))
		self.image = surf
		self.rect = pygame.rect.Rect(new_pos, (d, d))
		self.dirty = 1

	def hover_off(self):
		self.image = self.base_image
		self.rect = pygame.Rect(self.position, (75, 75))
		self.dirty = 1
