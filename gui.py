import pygame
import game_data


class Mouse_trigger:
	def __init__(self):
		self.rect = None

	def hover_on(self):
		pass

	def hover_off(self):
		pass

	def on_click(self):
		pass


class RulesButton(pygame.sprite.DirtySprite, Mouse_trigger):
	def __init__(self, position):
		super().__init__()
		self.image = game_data.buttons[1][3]
		self.rect = pygame.Rect(position, (50, 50))


class LevelButton(pygame.sprite.DirtySprite, Mouse_trigger):
	def __init__(self, level, position):
		super().__init__()
		self.level = level
		self.image = None
		self.rect = pygame.Rect(position, (50, 50))
		self.font = pygame.font.Font("freesansbold.ttf", 25)
		self.draw_level()

	def draw_level(self):
		self.image = game_data.buttons[1][2].copy()
		text = self.font.render(str(self.level), True, (199, 180, 20))
		offset = 8 + (34 - text.get_width()) // 2
		self.image.blit(text, (offset, 12))

	def hover_on(self):
		rect = pygame.Rect((0, 0), (50, 50))
		pygame.draw.rect(self.image, (199, 180, 20), rect, 1)
		self.dirty = 1

	def hover_off(self):
		self.draw_level()
		self.dirty = 1


class MenuButton(pygame.sprite.DirtySprite, Mouse_trigger):
	def __init__(self, position):
		super().__init__()
		self.image = game_data.buttons[0][3]
		self.rect = pygame.Rect(position, (50, 50))


class ReloadButton(pygame.sprite.DirtySprite, Mouse_trigger):
	def __init__(self):
		super().__init__()
		self.image = game_data.buttons[0][2]
		self.rect = pygame.Rect((60, 5), (50, 50))


class UpgradeButton(pygame.sprite.DirtySprite):
	def __init__(self, position, building_type, target, image):
		super().__init__()
		self.type = building_type
		self.target = target
		self.base_image = image
		self.rect = pygame.Rect(position, (50, 50))
		self.font = pygame.font.Font("freesansbold.ttf", 10)
		cost = 50 * (target.level + 1)
		text = self.font.render("-" + str(cost) + "$", True, (199, 180, 20))
		offset = 8 + (34 - text.get_width()) // 2
		self.image = self.base_image.copy()
		self.image.blit(text, (offset, 33))


class SellButton(pygame.sprite.DirtySprite):
	def __init__(self, position, target):
		super().__init__()
		self.target = target
		self.base_image = game_data.buttons[1][1]
		self.rect = pygame.Rect(position, (50, 50))
		self.font = pygame.font.Font("freesansbold.ttf", 10)
		cost = 50 * (target.level - 1)
		text = self.font.render("+" + str(cost) + "$", True, (199, 180, 20))
		offset = 8 + (34 - text.get_width()) // 2
		self.image = self.base_image.copy()
		self.image.blit(text, (offset, 33))


class PauseButton(pygame.sprite.DirtySprite, Mouse_trigger):
	def __init__(self, position):
		super().__init__()
		pause = game_data.buttons[0][0]
		play = game_data.buttons[0][1]
		self.pictures = (pause, play)
		self.image = pause
		self.rect = pygame.Rect(position, (50, 50))
		self.frame = 0

	def on_click(self):
		self.frame += 1
		self.image = self.pictures[self.frame % 2]
		self.dirty = 1


class ScoreBoard(pygame.sprite.DirtySprite):
	def __init__(self, image, position):
		super().__init__()
		self.base_image = image
		self.image = image
		self.rect = pygame.Rect(position, (image.get_width(), image.get_height()))
		self.font = pygame.font.Font("freesansbold.ttf", 25)

	def update_score(self, score):
		text = self.font.render(score, True, (199, 180, 20))
		offset = self.base_image.get_width() - 35 - text.get_width()
		self.image = self.base_image.copy()
		self.image.blit(text, (offset, 13))
		self.dirty = 1


class GUI:
	def __init__(self, screen, size):
		self.screen = screen
		width, height = size
		self.size = size
		self.sprites = pygame.sprite.LayeredDirty()
		self.hovered = None
		self.grid = [None] * width
		for x in range(width):
			self.grid[x] = [None] * height

	def set_background(self, image):
		self.sprites.clear(self.screen, image)

	def update(self):
		pygame.display.update(self.sprites.draw(self.screen))

	def add(self, sprite, send_back=False):
		layer = self.sprites.get_bottom_layer() - 1 if send_back else None
		self.sprites.add(sprite, layer=layer)

		if isinstance(sprite, Mouse_trigger):
			x, y = sprite.rect.x, sprite.rect.y
			for j in range(x, x + sprite.rect.width):
				for i in range(y, y + sprite.rect.height):
					self.grid[j][i] = sprite

	def remove(self, sprite):
		self.sprites.remove(sprite)
		if isinstance(sprite, Mouse_trigger):
			x, y = sprite.rect.x, sprite.rect.y
			for j in range(x, x + sprite.rect.width):
				for i in range(y, y + sprite.rect.height):
					self.grid[j][i] = None

		# resolve opacity bug
		if self.hovered is not None:
			self.hovered.dirty = 1

	def get_sprite(self, x, y):
		return self.grid[x][y]

	def on_mouse_motion(self, x, y):
		if not 0 <= x < self.size[0] or not 0 <= y < self.size[1]:
			return None

		sprite: Mouse_trigger = self.grid[x][y]
		if self.hovered is sprite:
			return
		if self.hovered is not None:
			self.hovered.hover_off()

		self.hovered = sprite
		if sprite is not None:
			sprite.hover_on()


class RulesGUI(GUI):
	def __init__(self):
		background = pygame.image.load("assets/rules.png")
		size = background.get_width(), background.get_height()
		screen = pygame.display.set_mode(size)
		super().__init__(screen, size)
		self.set_background(background)
		self.add(MenuButton((17, 38)))


class MenuGUI(GUI):
	def __init__(self):
		background = pygame.image.load("assets/menu.png")
		size = background.get_width(), background.get_height()
		screen = pygame.display.set_mode(size)
		super().__init__(screen, size)
		self.set_background(background)
		self.add(RulesButton((245, 195)))

		for lvl in range(game_data.n_level):
			self.add(LevelButton(lvl + 1, (64+lvl*60, 100)))


class GameGUI(GUI):
	def __init__(self, level):
		level_background = pygame.image.load(game_data.maps[level]).convert()
		size = level_background.get_width(), level_background.get_height()
		screen = pygame.display.set_mode(size)
		super().__init__(screen, size)
		self.set_background(level_background)
		self.add(MenuButton((5, 5)))
		self.add(ReloadButton())

		w = size[0] - 55
		self.add(PauseButton((w, 5)))
		w -= 90
		self.score_coin = ScoreBoard(game_data.scores_image[2][0], (w, 5))
		w -= 90
		self.score_wave = ScoreBoard(game_data.scores_image[1][0], (w, 5))
		w -= 90
		self.score_life = ScoreBoard(game_data.scores_image[0][0], (w, 5))
		self.add(self.score_coin)
		self.add(self.score_wave)
		self.add(self.score_life)
		self.building_buttons = []

	def result_screen(self, victory):
		fontr = pygame.font.Font("freesansbold.ttf", 100)
		fontt = pygame.font.Font("freesansbold.ttf", 20)
		todo = fontt.render("Click to continue...", True, (0, 0, 0))
		if victory:
			result = fontr.render("VICTORY !", True, (199, 180, 20))
		else:
			result = fontr.render("DEFEAT !", True, (150, 0, 0))
		sh, sw = self.screen.get_height(), self.screen.get_width()
		rh, rw = result.get_height(), result.get_width()
		th, tw = todo.get_height(), todo.get_width()
		dxr, dyr = (sw - rw) // 2, (sh - rh) // 2
		dxt, dyt = (sw - tw) // 2, dyr + 100
		self.screen.blit(result, (dxr, dyr))
		self.screen.blit(todo, (dxt, dyt))
		pygame.display.flip()

	def make_building_type_buttons(self, building):
		cx, cy = building.rect.center
		pos = [(cx - 55, cy - 55), (cx + 5, cy - 55), (cx - 55, cy + 5), (cx + 5, cy + 5)]
		for t in range(4):
			button = UpgradeButton(pos[t], t, building, game_data.buttons[2][t])
			self.building_buttons.append(button)
			self.sprites.add(button)

	def make_building_upgrade_button(self, building):
		cx, cy = building.rect.center
		button = UpgradeButton((cx - 55, cy - 55), building.type, building, game_data.buttons[1][0])
		self.building_buttons.append(button)
		self.sprites.add(button)

	def make_building_sell_button(self, building):
		cx, cy = building.rect.center
		sell = SellButton((cx + 5, cy - 55), building)
		self.building_buttons.append(sell)
		self.sprites.add(sell)

	def remove_building_buttons(self):
		for button in self.building_buttons:
			self.sprites.remove(button)
		self.building_buttons = []

	def get_sprite(self, x, y):
		for button in self.building_buttons:
			if button.rect.collidepoint(x, y):
				return button
		return self.grid[x][y]
