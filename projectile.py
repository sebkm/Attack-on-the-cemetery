import pygame
import utils
import game_data


class Projectile(pygame.sprite.DirtySprite):
	def __init__(self, target, damage):
		super().__init__()
		self.velocity = game_data.projectile_speed
		self.target = target
		self.damage = damage
		self.reached = False
		self.image = None
		self.rect = None
		self.type = None

	def action(self, monsters):
		if self.reached:
			return False

		self.dirty = 1
		self.set_orientation()  # orient before moving for better visual effect
		dst = self.target.rect.center
		delta = utils.line_move(self.rect.center, dst, self.velocity)
		self.rect = self.rect.move(*delta)

		if self.rect.center == dst:
			self.hurt(monsters)
			self.reached = True
		return True

	def hurt(self, monsters):
		pass

	def set_orientation(self):
		src = self.rect.center
		dst = self.target.rect.center
		pos = self.rect.x, self.rect.y
		angle = utils.angle(src, dst)
		self.image = pygame.transform.rotate(game_data.projectile_images[self.type][0], angle)
		self.rect = pygame.Rect(pos, (self.image.get_width(), self.image.get_height()))


class Arrow(Projectile):
	def __init__(self, position, target, damage):
		super().__init__(target, damage)
		self.type = 0
		image_source = game_data.projectile_images[self.type][0]
		self.rect = pygame.Rect(position, (image_source.get_width(), image_source.get_height()))
		self.set_orientation()

	def hurt(self, monsters):
		self.target.hurt(self.damage)


class FireBall(Projectile):
	def __init__(self, position, target, damage):
		super().__init__(target, damage)
		self.type = 1
		image_source = game_data.projectile_images[self.type][0]
		self.rect = pygame.Rect(position, (image_source.get_width(), image_source.get_height()))
		self.set_orientation()

	def hurt(self, monsters):
		src = self.rect.center
		for monster in monsters:
			dist = utils.distance(src, monster.rect.center)
			if dist <= game_data.explosion_radius:
				monster.hurt(self.damage)
		self.image = game_data.effects[0][0]
		self.rect = self.target.rect.copy()
		self.dirty = 1


class IceBall(Projectile):
	def __init__(self, position, target, damage):
		super().__init__(target, damage)
		self.type = 2
		image_source = game_data.projectile_images[self.type][0]
		self.rect = pygame.Rect(position, (image_source.get_width(), image_source.get_height()))
		self.set_orientation()

	def hurt(self, monsters):
		self.target.hurt(self.damage)
		self.target.freeze(game_data.frozen_duration)