import pygame
import gui
import game_data
import building
import wave


class Level:
	def __init__(self, level):
		self.game_over = False
		self.level = level
		self.pause = False
		self.life_counter, self.coin_counter = game_data.player_stat[level]
		self.wave_agent = None
		self.wave_counter = 0
		self.wave_max = len(game_data.waves[level])
		self.monsters = []
		self.projectiles = []
		self.buildings = []
		self.game_gui = gui.GameGUI(level)
		self.game_gui.score_life.update_score(str(self.life_counter))
		self.game_gui.score_coin.update_score(str(self.coin_counter))

		for pos in game_data.buildings_locations[level]:
			b = building.Building(pos)
			self.buildings.append(b)
			self.game_gui.add(b)

		self.clk = pygame.time.Clock()

	def start_level(self):
		while True:
			self.clk.tick(10)
			self.game_gui.update()
			ret = self.event_check()
			if ret is not None:
				return ret

			if self.game_over:
				self.game_gui.result_screen(self.life_counter > 0)

			if not self.pause and not self.game_over:
				self.game_actions()

	def event_check(self):
		mp = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return "exit"

			elif event.type == pygame.MOUSEBUTTONUP:
				# print(mp, ", ")
				if self.game_over:
					return "menu"
				sprite = self.game_gui.get_sprite(*mp)

				if isinstance(sprite, gui.UpgradeButton):
					cost = 50 * (sprite.target.level + 1)
					total = self.coin_counter - cost
					if total >= 0:
						self.coin_counter = total
						sprite.target.type = sprite.type
						sprite.target.upgrade()
						self.game_gui.add(sprite.target.bar_indicator)
						self.game_gui.remove_building_buttons()
						self.game_gui.score_coin.update_score(str(self.coin_counter))

				elif isinstance(sprite, gui.SellButton):
					self.coin_counter += 50 * (sprite.target.level - 1)
					sprite.target.sell()
					self.game_gui.remove(sprite.target.bar_indicator)
					self.game_gui.remove_building_buttons()
					self.game_gui.score_coin.update_score(str(self.coin_counter))

				else:
					self.game_gui.remove_building_buttons()

				if isinstance(sprite, building.Building):
					if sprite.type is None:
						self.game_gui.make_building_type_buttons(sprite)
					else:
						if sprite.level < sprite.level_max:
							self.game_gui.make_building_upgrade_button(sprite)
							self.game_gui.make_building_sell_button(sprite)
						else:
							self.game_gui.make_building_sell_button(sprite)

				elif isinstance(sprite, gui.PauseButton):
					sprite.on_click()
					self.pause = not self.pause
				elif isinstance(sprite, gui.ReloadButton):
					return self.level
				elif isinstance(sprite, gui.MenuButton):
					return "menu"

			elif event.type == pygame.MOUSEMOTION:
				self.game_gui.on_mouse_motion(*mp)
		return None

	def game_actions(self):
		if self.life_counter <= 0:
			self.game_over = True
			return

		end_of_wave = self.wave_agent is None and len(self.monsters) == 0
		if end_of_wave and self.wave_counter == self.wave_max:
			self.game_over = True
			return

		elif end_of_wave and self.wave_counter < self.wave_max:
			instructions = game_data.waves[self.level][self.wave_counter]
			self.wave_agent = wave.Wave(instructions, game_data.paths[self.level])
			self.wave_counter += 1
			self.game_gui.score_wave.update_score(str(self.wave_counter) + "/" + str(self.wave_max))

		if self.wave_agent is not None:
			active, monster = self.wave_agent.action()
			if not active:
				self.wave_agent = None
			elif monster is not None:
				self.monsters.append(monster)
				self.game_gui.add(monster, send_back=True)
				self.game_gui.add(monster.bar_indicator)

		for monster in self.monsters[:]:
			active, alive = monster.action()
			if not active:
				if alive:
					self.life_counter -= monster.damage
					self.game_gui.score_life.update_score(str(self.life_counter))
				else:
					self.coin_counter += monster.coin
					self.game_gui.score_coin.update_score(str(self.coin_counter))
				self.monsters.remove(monster)
				self.game_gui.remove(monster)
				self.game_gui.remove(monster.bar_indicator)

		for b in self.buildings:
			projectile = b.action(self.monsters)
			if projectile is not None:
				self.projectiles.append(projectile)
				self.game_gui.add(projectile)

		for projectile in self.projectiles[:]:
			active = projectile.action(self.monsters)
			if not active:
				self.projectiles.remove(projectile)
				self.game_gui.remove(projectile)
