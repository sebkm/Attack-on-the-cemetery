import pygame
import utils
import game_data
import level
import menu


##################
# initialisation #
##################
pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP])
pygame.display.set_caption("Attack on the cemetery")
screen = pygame.display.set_mode((1, 1))
game_data.buildings_images = utils.load_sprite_sheet("assets/buildings.png", (75, 75))
game_data.monsters_images = utils.load_sprite_sheet("assets/monsters.png", (50, 50))
game_data.projectile_images = utils.load_sprite_sheet("assets/projectiles.png", (32, 9))
game_data.effects = utils.load_sprite_sheet("assets/effects.png", (50, 50))
game_data.new_building_image = pygame.image.load("assets/building_0.png").convert_alpha()
game_data.buttons = utils.load_sprite_sheet("assets/buttons.png", (50, 50))
game_data.scores_image = utils.load_sprite_sheet("assets/scores.png", (85, 50))
pygame.mixer_music.load("assets/Wintergatan - Ondophone .mp3")

next_ui = "menu"
while True:
	if next_ui == "exit":
		break
	elif next_ui == "menu":
		game_menu = menu.Menu()
		next_ui = game_menu.start_menu()
	elif next_ui == "rules":
		game_rules = menu.Menu("rules")
		next_ui = game_rules.start_menu()
	else:
		pygame.mixer_music.play(-1)
		game_level = level.Level(int(next_ui))
		next_ui = game_level.start_level()
		pygame.mixer_music.stop()
pygame.quit()
