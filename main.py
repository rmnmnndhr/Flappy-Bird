import pygame
import random, sys
from os import path
from letter import *
# assets from https://github.com/sourabhv/FlapPyBird/tree/master/assets/sprites

WIDTH = 288
HEIGHT = 512
FPS = 60

# define a few useful color
BLACK = (0, 0, 0)

pygame.init() #initialize pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
vect = pygame.math.Vector2

img_dir = path.join(path.dirname(__file__), 'sprites')


# loading images --------------------------------------------------------------------------------------------
background_img = random.choice([pygame.image.load(path.join(img_dir, 'background-day.png')).convert_alpha(),
							pygame.image.load(path.join(img_dir, 'background-night.png')).convert_alpha()])
message_img = pygame.image.load(path.join(img_dir, 'message.png')).convert_alpha()
pipe = random.choice([pygame.image.load(path.join(img_dir, 'pipe-green.png')).convert_alpha(),
						pygame.image.load(path.join(img_dir, 'pipe-red.png')).convert_alpha()])
base_img = pygame.image.load(path.join(img_dir, 'base.png')).convert_alpha()
go_img = pygame.image.load(path.join(img_dir, 'gameover.png')).convert_alpha()
bird1 = [pygame.image.load(path.join(img_dir, 'yellowbird-downflap.png')).convert_alpha(), 
		pygame.image.load(path.join(img_dir, 'yellowbird-midflap.png')).convert_alpha(),
		pygame.image.load(path.join(img_dir, 'yellowbird-upflap.png')).convert_alpha()]
bird2 = [pygame.image.load(path.join(img_dir, 'bluebird-downflap.png')).convert_alpha(), 
		pygame.image.load(path.join(img_dir, 'bluebird-midflap.png')).convert_alpha(),
		pygame.image.load(path.join(img_dir, 'bluebird-upflap.png')).convert_alpha()]
bird3 = [pygame.image.load(path.join(img_dir, 'redbird-downflap.png')).convert_alpha(), 
		pygame.image.load(path.join(img_dir, 'redbird-midflap.png')).convert_alpha(),
		pygame.image.load(path.join(img_dir, 'redbird-upflap.png')).convert_alpha()]
bird_img = random.choice([bird1, bird2, bird3])
scoreboard_img = pygame.image.load(path.join(img_dir, 'scoreboard.png')).convert_alpha()
new_img = pygame.image.load(path.join(img_dir, 'new.png')).convert_alpha()


class Bird:
	def __init__(self):
		self.pos = vect(WIDTH/2 - 10, HEIGHT/2)
		self.index = 0
		self.img = bird_img[self.index]
		self.imgCopy = self.img.copy()
		self.rect = self.img.get_rect()
		self.vel = vect(0, 0)
		self.acc = vect(0, 0.65)
		self.rectCopy = self.rect
		self.now = pygame.time.get_ticks()
		self.rotangle = 0

	def draw(self, screen):
		self.rectCopy.center = self.pos
		screen.blit(self.img, self.rectCopy)
		# pygame.draw.rect(screen, BLACK, self.rect, 1) #To test the rect

	def update(self):
		self.vel += self.acc

		if self.vel.y > 8:
			self.vel.y = 8

		if self.vel.y < -8:
			self.vel.y = -8

		self.pos += self.vel

		if self.pos.y < -self.rect.height:
			self.pos.y = -self.rect.height

		self.mask = pygame.mask.from_surface(self.img)

	def animate(self):
		if pygame.time.get_ticks() - self.now >= 100:
			self.now = pygame.time.get_ticks()
			self.index = (self.index + 1) % len(bird_img)
			self.img = bird_img[self.index]
			self.imgCopy = self.img.copy()

	def rotations(self):
		self.prev = self.rect
		
		if self.vel.y < 6:
			self.rotangle += 10
			if self.rotangle > 20:
				self.rotangle = 20
			self.img = pygame.transform.rotate(self.imgCopy, self.rotangle)
			self.rect = self.img.get_rect()
			self.rect.center = self.prev.center
			self.rectCopy = self.rect

		if self.vel.y > 6:
			self.rotangle -= 10
			if self.rotangle < -90:
				self.rotangle = -90
			self.img = pygame.transform.rotate(self.imgCopy, self.rotangle)
			self.rect = self.img.get_rect()
			self.rect.center = self.prev.center
			self.rectCopy = self.rect

		
class Base:
	def __init__(self):
		self.pos = vect(0, HEIGHT- 112)
		self.vel = vect(-2.5, 0)
		self.img = base_img
		self.rect = self.img.get_rect()
		self.rect.y = HEIGHT- 112
		self.rectCopy = self.rect

	def draw(self, screen):
		self.rectCopy = self.pos
		screen.blit(base_img, self.rectCopy)

	def update(self):
		self.pos += self.vel
		if self.pos.x < -47:
			self.pos = vect(0, HEIGHT- 112)


class PipeUp:
	def __init__(self, y):
		self.img = pipe
		self.rect = self.img.get_rect()
		self.pos = vect(400, y)
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, screen):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		screen.blit(self.img, self.rect)

	def update(self):
		self.pos.x -= 2.5

class PipeDown:
	def __init__(self, y):
		self.img = pygame.transform.rotate(pipe, 180)
		self.rect = self.img.get_rect()
		self.pos = vect(400, y)
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, screen):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		screen.blit(self.img, self.rect)

	def update(self):
		self.pos.x -= 2.5
class Score:
	def __init__(self):
		self.x = 425

	def update(self):
		self.x -=2.5

# Game loop -------------------------------------------------------------------------------------------------
def main():
	bird = Bird()
	base = Base()
	pipesUp = []
	pipesDown = []
	scores = []
	t = 0
	score = 0
	running = True
	waiting = True

	with open(path.join(path.dirname(__file__), 'highscore.txt'), 'r') as file:
		try:
			highscore = int(file.read())
		except:
			highscore = 0

	while running:
		t += 1
		screen.fill(BLACK) # Filling the screen with color
		screen.blit(background_img, (0,0))

		# waiting screen ------------------------------------------------------------------------------------
		while waiting:
			clock.tick(FPS)
			screen.blit(background_img, (0,0))
			bird.animate()
			bird.draw(screen)	

			screen.blit(message_img, (55, 10))

			base.update()
			base.draw(screen)


			# checking event on waiting screen
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						bird.vel.y -= 25
						waiting = False

			pygame.display.flip()

		# main screen ---------------------------------------------------------------------------------------
		clock.tick(FPS)
		for event in pygame.event.get():
			# check for closing the window
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.vel.y -= 20

		#update
		bird.update()
		bird.animate()
		bird.rotations()
		bird.draw(screen)

		if t > 60:
			t = 0
			pipe()

		for i in range(len(pipesUp)-1, 0, -1):
			pipesUp[i].draw(screen)
			pipesUp[i].update()
			if pipesUp[i].pos.x < -52:
				pipesUp.remove(pipesUp[i])

			x = pipesUp[i].rect.x - bird.rect.x 
			y = pipesUp[i].rect.y - bird.rect.y
			overlap = bird.mask.overlap(pipesUp[i].mask, (x, y))

			if overlap:
				drop()
				gameover(highscore)

			pipesDown[i].draw(screen)
			pipesDown[i].update()
			if pipesDown[i].pos.x < -52:
				pipesDown.remove(pipesDown[i])

			x = pipesDown[i].rect.x - bird.rect.x 
			y = pipesDown[i].rect.y - bird.rect.y
			overlap = bird.mask.overlap(pipesDown[i].mask, (x, y))

			if overlap:
				drop()
				gameover(highscore)

			

		for i in range(len(scores)-1, 0,-1):
			scores[i].update()
			if scores[i].x < WIDTH/2 - 10:
				score += 1
				scores.remove(scores[i])

		base.draw(screen)
		base.update()

		draw_text(str(score), 100, screen, WIDTH/2, 10)

		if bird.rect.colliderect(base.rect):
			bird.rect.bottom = base.rect.top
			gameover(highscore)

		# game over screen ----------------------------------------------------------------------------------
		def gameover(highscore):
			waiting = True
			new = False

			while waiting:
				clock.tick(FPS)
				screen.blit(background_img, (0,0))
				for i in range(len(pipesUp)-1, 0, -1):
					pipesUp[i].draw(screen)

				for i in range(len(pipesDown)-1, 0, -1):
					pipesDown[i].draw(screen)

				screen.blit(go_img, (55, 10))
				bird.draw(screen)
				base.draw(screen)


				screen.blit(pygame.transform.scale(scoreboard_img, (150, 199)), (75, HEIGHT/2-100))
				if score > highscore:
					highscore = score
					with open(path.join(path.dirname(__file__), 'highscore.txt'), 'w') as file:
						file.write(str(score))
					new = True

				if new:
					screen.blit(pygame.transform.scale(new_img, (50, 22)), (83, HEIGHT/2+3))
				draw_text(str(score), 120, screen, WIDTH/2+20, HEIGHT/2 - 45)
				draw_text(str(highscore), 120, screen, WIDTH/2+20, HEIGHT/2 + 30)


				# checking event on waiting screen
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							main()

				pygame.display.flip()

		def pipe():
			top = random.randrange(200, 400)
			pipesUp.append(PipeUp(top))
			pipesDown.append(PipeDown(top - 420))
			scores.append(Score())

		def drop():
			dropping = True
			while dropping:
				clock.tick(FPS)
				screen.blit(background_img, (0,0))
				bird.vel.y = 10

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				for i in range(len(pipesUp)-1, 0, -1):
					pipesUp[i].draw(screen)

				for i in range(len(pipesDown)-1, 0, -1):
					pipesDown[i].draw(screen)

				bird.draw(screen)
				bird.update()
				bird.animate()
				bird.rotations()
				base.draw(screen)

				if bird.rect.colliderect(base.rect):
					dropping = False

				draw_text(str(score), 100, screen, WIDTH/2, 10)


				pygame.display.flip()


		# updating the window
		pygame.display.flip()

main()
pygame.quit()