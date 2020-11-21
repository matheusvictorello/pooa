import pygame
from game_util import *
from Arrow import Arrow

class Bow:
	def __init__(self, pos):
		self.pos = pos
		self.arrows = []
		self.color = (255, 255, 255)

	def shoot(self, target):
		x, y = self.pos
		tx, ty = target
		dx, dy = magnitude((tx - x, ty - y))
		origin = (x, y)
		direction = (dx, dy)
		self.arrows.append(Arrow(origin, direction))

	def draw(self, surface):
		mx, my = pygame.mouse.get_pos()
		x, y = self.pos
		dx, dy = magnitude((mx - x, my - y))
		fx = x + dx * 15
		fy = y + dy * 15
		pygame.draw.line(surface, self.color, self.pos, (fx, fy), 3)

		for arrow in self.arrows:
			arrow.draw(surface)

	def update(self, pos):
		self.pos = pos
		
		for arrow in self.arrows:
			arrow.update()
		self.arrows = list(filter(self.arrowOnScreen, self.arrows))

	def arrowOnScreen(self, arrow):
		return onScreen(arrow.pos)

