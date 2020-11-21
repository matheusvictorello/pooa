import math
import pygame
from collections import defaultdict

WIDTH = 500
HEIGHT = 500

class Game:
	def __init__(self):
		pygame.init()
		screen = pygame.display.set_mode([WIDTH, HEIGHT])
		clock = pygame.time.Clock()
		running = True
		player_pos = (WIDTH/2, HEIGHT/2)
		player_color = (200, 0, 255)
		player_speed = 2.5
		bow_pos = player_pos
		bow_color = (255, 255, 255)
		arrows = []
		arrow_speed = 10
		arrow_color = (250, 150, 0)
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = player_pos
					tx, ty = event.pos
					dx, dy = (tx - x, ty - y)
					mag = math.sqrt(dx**2 + dy**2)
					dx /= mag
					dy /= mag
					origin = (x, y)
					direction = (dx * arrow_speed, dy * arrow_speed)
					arrows.append([origin, direction])
			screen.fill((40, 40, 40))
			keys = pygame.key.get_pressed()
			vx, vy = 0, 0
			if keys[pygame.K_a]:
				vx -= 1
			if keys[pygame.K_w]:
				vy -= 1
			if keys[pygame.K_s]:
				vy += 1
			if keys[pygame.K_d]:
				vx += 1
			x, y = player_pos
			x += vx * player_speed
			y += vy * player_speed
			player_pos = (x, y)
			for i, arrow in enumerate(arrows):
				pos, vel = arrow
				x, y = pos
				vx, vy = vel
				x += vx
				y += vy
				pos = (x, y)
				arrows[i] = [pos, vel]
			arrows_on_screen = []
			for arrow in arrows:
				pos, _ = arrow
				x, y = pos
				if 0 <= x < WIDTH:
					if 0 <= y < HEIGHT:
						arrows_on_screen.append(arrow)
			arrows = arrows_on_screen
			bow_pos = player_pos
			pygame.draw.circle(screen, player_color, player_pos, 15)
			mx, my = pygame.mouse.get_pos()
			x, y = bow_pos
			dx, dy = (mx - x, my - y)
			mag = math.sqrt(dx**2 + dy**2)
			dx /= mag
			dy /= mag
			fx = x + dx * 15
			fy = y + dy * 15
			pygame.draw.line(screen, bow_color, bow_pos, (fx, fy), 3)
			for arrow in arrows:
				pos, _ = arrow
				pygame.draw.circle(screen, arrow_color, pos, 3)
			pygame.display.flip()
			clock.tick(60)
		pygame.quit()

if __name__ == '__main__':
	Game()
