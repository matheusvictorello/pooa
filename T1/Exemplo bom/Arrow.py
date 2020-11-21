import pygame

class Arrow:
	def __init__(self, origin, direction):
		self.pos = origin
		self.speed = 10
		dx, dy = direction
		self.vel = (dx * self.speed, dy * self.speed)
		self.color = (250, 150, 0)

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, 3)

	def update(self):
		x, y = self.pos
		vx, vy = self.vel
		x += vx
		y += vy
		self.pos = (x, y)