import math
from game_config import *

def magnitude(vec):
	vx, vy = vec
	mag = math.sqrt(vx**2 + vy**2)
	vx /= mag
	vy /= mag
	return (vx, vy)

def onScreen(pos):
	x, y = pos

	if 0 <= x < WIDTH:
		if 0 <= y < HEIGHT:
			return True
	return False