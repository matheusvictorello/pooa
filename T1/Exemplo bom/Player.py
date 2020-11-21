import pygame
from game_config import *
from game_util import *
from Bow import Bow

class Player:
	def __init__(self):
		self.color = (200, 0, 255)
		self.pos = (WIDTH/2, HEIGHT/2)
		self.speed = 2.5
		self.bow = Bow(self.pos)

	def processEvent(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.bow.shoot(event.pos)

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, 15)
		self.bow.draw(surface)

	def update(self):
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
		x, y = self.pos
		x += vx * self.speed
		y += vy * self.speed
		self.pos = (x, y)

		self.bow.update(self.pos)
