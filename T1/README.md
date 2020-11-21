# Princípio da ... responsabilidade única?
Autor: Matheus Victorello

## O que é então?

O Princípio da responsabilidade única é um dos cinco componentes SOLID, todo mundo fala o que o princípio diz, que uma classe ou função deve fazer apenas uma coisa ou ser modificada por apenas um motivo, o próprio Robert C. Martin (Uncle Bob) o descreve no livro [Agile Software Development](https://books.google.com/books?id=0HYhAQAAIAAJ&redir_esc=y) como "A classe deve ter apenas um motivo para ser modificada", dada a confusão e imprecisão associada ao conseito ele volta a defini-lo em [The Clean Code Blog](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html) como "O princípio é sobre pessoas", ... eeeeehh, meio confuso né, vamos deixar essas descrições e nomes de lado, particularmente eu prefiro chama-lo de "Princípido não é da minha conta".
Vamos usar esse código como exemplo:
```python
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
```
Quem fez essa monstruosidade definitivamente tinha tudo sobre controle, o problema é que ... só ele né, dependendo nem ele, daqui a um més com certeza nem ele.
Como melhorar ? Meu ponto de partida é o altruísmo, por exemplo, vamos nos colocar no lugar de um objeto `Game` por um momento, primeiro não há nada, então algo nos instancia e nos dá responsabilidade sobre esse código ai, e a gente pensa, "mas o que ~~merda~~ é essa", exatamente, a vida de um `Game` não é fácil.

## E agora?
Sejamos programadores altruístas, felizmente eu tenho conhecimento sobre o objetivo desse código, vamos ver.
```python
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
```
O Game não existe mais, ufa, bom pra ele, mas agora tem uma tal de `main`, que é uma função, isso porque ela não tem sentimentos, memória própria, ideias, comportamentos, praticamente um zumbi, ela só tem que fazer seu trabalho, que trabalho?
Se a gente observar vamos conseguir ver algumas coisas sendo declaradas, um loop, eventos, `player`, `screen`, `update`, `draw`, isso mesmo, é um "game loop" de um jogo que tem apenas um player, e ai que entra o nome do princípio, não, não o da "Responsabilidade única", mas sim o "Princípido não é da minha conta", a `main` não liga para o que o `player` faz em `processEvent`, `fill` ou `draw`, falaram para ela chamar essas funções e isso que ela faz.
Mas calma lá, a gente se importa.
```python
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
```
Agora sim, ai está o que um `Player` faz, o `processEvent` processa eventos que são importantes para ele, o `draw` o desenha em uma `surface` e o `update` atualiza sua posição, não nos passa despercebido o `Bow` que o `Player` tem, novamente, "não é da conta dele" o que o `Bow` faz. Tem essa outra função `shoot` do `Bow`, certamente um `Player` não atira `Arrow`'s, um `Bow` sim, o `Player` só usa ele, é claro, o `Player` poderia atirar as `Arrow`'s, mas ai ser constrangedor né, vamos ver como o `Bow` faz.
```python
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
```
Analogamente ao `Player`, o `Bow` se desenha na `draw` e atualiza sua posição na `update`, mas é a `shoot` que nos intereça, o `Bow` recebe do `Player` o ..., não né, o `Bow` nem sabe o que é `Player`, do ponto de vista dele ele só recebe e vida que segue. O ponto é que o `Bow` transforma o `target` em uma `origin` e `direction` para poder informar um `Arrow` o que fazer.
```python
class Arrow:
	def __init__(self, origin, direction):
		self.pos = origin
		self.speed = 10
		dx, dy = direction
		self.vel = (dx * self.speed, dy * self.speed)
		self.color = (250, 150, 0)

	def __del__(self):
		print('Fiz o que tinha que fazer!')

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, 3)

	def update(self):
		x, y = self.pos
		vx, vy = self.vel
		x += vx
		y += vy
		self.pos = (x, y)
```
A `Arrow` por sua vez faz o que tem que fazer, voa por ai até morrer.

É desse modo que cada um faz o que têm que fazer e ninguém quer saber como.