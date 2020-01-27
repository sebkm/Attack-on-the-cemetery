import pygame
import gui


class Menu:
	def __init__(self, screen="menu"):
		if screen == "menu":
			self.menu_gui = gui.MenuGUI()
		elif screen == "rules":
			self.menu_gui = gui.RulesGUI()

	def start_menu(self):
		self.clk = pygame.time.Clock()
		while True:
			self.clk.tick(10)
			self.menu_gui.update()
			ret = self.event_check()
			if ret is not None:
				return ret

	def event_check(self):
		mp = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return "exit"
			elif event.type == pygame.MOUSEBUTTONUP:
				sprite = self.menu_gui.get_sprite(*mp)
				if isinstance(sprite, gui.LevelButton):
					return str(sprite.level - 1)
				elif isinstance(sprite, gui.RulesButton):
					return "rules"
				elif isinstance(sprite, gui.MenuButton):
					return "menu"
			elif event.type == pygame.MOUSEMOTION:
				self.menu_gui.on_mouse_motion(*mp)
		return None