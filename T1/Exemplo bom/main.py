import pygame
from game_config import *
from game_util import *
from Player import Player

def main():
	pygame.init()
	screen = pygame.display.set_mode([WIDTH, HEIGHT])
	clock = pygame.time.Clock()
	running = True

	player = Player()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			player.processEvent(event)

		screen.fill((40, 40, 40))

		player.update()
		
		player.draw(screen)

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()