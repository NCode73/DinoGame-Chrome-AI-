import pygame
import neat 
import time
import os
import random 
import math 

pygame.init()

win_width = 1200
win_height = 200

score = 0 
jumpvar = -16
pop_size = 5050

STAT_FONT = pygame.font.SysFont("comicsans", 20)

DINO_LIST = [pygame.image.load(os.path.join(r"pics\\Dino1.png")),
pygame.image.load(os.path.join(r"pics\\Dino2.png")),
pygame.image.load(os.path.join(r"pics\\Dino3.png")),
pygame.image.load(os.path.join(r"pics\\down_Dino1.png")),
pygame.image.load(os.path.join(r"pics\\down_Dino2.png"))]

OBSTACLES = [pygame.image.load(os.path.join(r"pics\\cactuss.png")),
pygame.image.load(os.path.join(r"pics\\bird_pic1.png")),
pygame.image.load(os.path.join(r"pics\\bird_pic2.png"))]

BASE = pygame.image.load(os.path.join(r"pics\\Base.png"))
BG = pygame.image.load(os.path.join(r"pics\\BG.png"))


class Dino:
	animation_time = 20

	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.vel = 10 
		self.jump_vel = 8.5
		self.img = DINO_LIST[0]
		self.img_count = 0 
		self.img_count2 = 0 
		self.height = y
		self.tick_count = 0
		self.dino_jump = False
		self.jump_count = -16
		self.dino_down = False 
		self.count1 = 0 

	def dino_down1(self):
		if self.count1 == 16:
			self.dino_down = True 

	def draw(self, win):
		if self.img_count < self.animation_time*2 and self.dino_down == False:
			self.img = DINO_LIST[1]
			self.img_count += 1 
			win.blit(self.img, (self.x, self.y))
		elif self.img_count < self.animation_time*3 and self.dino_down == False:
			self.img = DINO_LIST[2]
			self.img_count += 1 
			win.blit(self.img, (self.x, self.y))
		elif self.img_count < self.animation_time*4 and self.dino_down == False:
			self.img = DINO_LIST[1]
			self.img_count = 10
			win.blit(self.img, (self.x, self.y))
		if self.dino_down == True and self.img_count2 < self.animation_time*2:
			self.img = DINO_LIST[3]
			self.img_count2 += 1 
			win.blit(self.img, (self.x, self.y+40))
		elif self.dino_down == True and self.img_count2 < self.animation_time*3:
			self.img = DINO_LIST[4]
			self.img_count2 += 1 
			win.blit(self.img, (self.x, self.y+40))
		elif self.dino_down == True and self.img_count2 < self.animation_time*4:
			self.img = DINO_LIST[3] 
			self.img_count2 = 10 
			self.img_count = 10 
			self.count1 = 0
			self.dino_down = False
			win.blit(self.img, (self.x, self.y+40))

	def get_mask(self):
		return pygame.mask.from_surface(DINO_LIST[0])

	def dino_jump1(self):
		if self.jump_count >= -15 and self.dino_down == False:
			n = 1 
			if self.jump_count <= 0:
				n = -1 
			self.y -= (self.jump_count**2)*0.15*n
			self.jump_count -= 1 


class Base:
	def __init__(self, x):
		self.vel = 10
		self.x = x 
		self.x2 = 1200
		self.y = 182

	def move(self):
		global score
		score += 0.01

		self.x -= self.vel
		self.x2 -= self.vel

		if self.x + BASE.get_width() <0 :
			self.x = self.x2 + BASE.get_width()
		if self.x2 + BASE.get_width() < 0:
			self.x2 = self.x + BASE.get_width()

	def draw(self, win):
		win.blit(BASE, (self.x, self.y))
		win.blit(BASE, (self.x2, self.y))


class Obstacles:
	def __init__(self, x):
		self.x = x 
		self.x2 = self.x + 26 
		self.x3 = self.x + 52
		self.x_bird  = x + 350
		self.height = 56
		self.obstacle_pic = OBSTACLES[0]
		self.obstacle_pic2 = OBSTACLES[0]
		self.obstacle_pic3 = OBSTACLES[0]
		self.obstacle_pic_bird1 = OBSTACLES[1]
		self.random_num = 1 
		self.vel = 10
		self.animation_time = 20
		self.img_count = 0
		self.bird_int = -2

	def move(self):
		self.x -= self.vel
		self.x2 -= self.vel 
		self.x3 -= self.vel 
		self.x_bird -= self.vel 

		if self.x < 0:
			self.random_num = random.randint(1,3)
			self.bird_int += 1 

			self.x = random.randint(900,4000)
			self.x2 = self.x + 26
			self.x3 = self.x2 + 26

		if self.x_bird < -20:
			if self.bird_int == 3:
				self.x_bird = self.x + 650
				self.bird_int = 0

	def draw(self, win):
		self.img_count += 1.2

		if self.img_count < self.animation_time*2:
			self.obstacle_pic_bird1 = OBSTACLES[1]
		elif self.img_count < self.animation_time*3:
			self.obstacle_pic_bird1 = OBSTACLES[2]
		elif self.img_count < self.animation_time*4:
			self.obstacle_pic_bird1 = OBSTACLES[1]
			self.img_count = 10 

		win.blit(self.obstacle_pic_bird1, (self.x_bird, -20))

		if self.random_num == 1: 
			win.blit(self.obstacle_pic, (self.x, 135))
		if self.random_num == 2:
			win.blit(self.obstacle_pic, (self.x, 135))
			win.blit(self.obstacle_pic2, (self.x2, 135))
		if self.random_num == 3:
			win.blit(self.obstacle_pic, (self.x, 135))
			win.blit(self.obstacle_pic2, (self.x2, 135))
			win.blit(self.obstacle_pic3, (self.x3, 135))

	def collide(self, dino):
		mask = dino.get_mask()

		mask1 = pygame.mask.from_surface(self.obstacle_pic)
		mask2 = (self.x - dino.x, 87 - round(dino.y))

		mask3 = pygame.mask.from_surface(self.obstacle_pic2)
		mask4 = (self.x2 - dino.x, 87 - round(dino.y))

		mask5 = pygame.mask.from_surface(self.obstacle_pic3)
		mask6 = (self.x3 - dino.x, 87 - round(dino.y))

		mask7 = pygame.mask.from_surface(self.obstacle_pic_bird1)
		mask8 = (self.x_bird - dino.x, 0 - round(dino.y))


		overlap = mask.overlap(mask1, mask2)
		overlap2 = mask.overlap(mask3, mask4)
		overlap3 = mask.overlap(mask5, mask6)
		overlap4 = mask.overlap(mask7, mask8)

		if overlap or overlap2 or overlap3:
			return True
		if overlap4 and dino.dino_down == True:
			return False
		elif overlap4:
			return True 

		return False

def draw(win, dinosours, base, obstacle, pop_size, vel, gen, scores):
	win.blit(BG, (0,0))

	base.draw(win)
	obstacle.draw(win)

	for dino in dinosours:
		dino.draw(win)
	
	text = STAT_FONT.render(f"Score: {round(score)}", 1, (255,255,255))
	text2 = STAT_FONT.render(f"Dinos-left: {round(pop_size)}", 1, (255,255,255))
	text3 = STAT_FONT.render(f"Speed: {round(vel)}", 1, (255,255,255))
	text4 = STAT_FONT.render(f"Gen: {round(gen)}", 1, (255,255,255))
	text5 = STAT_FONT.render(f"Best Score: {scores[(len(scores)-1)]}", 1, (255,255,255))
	win.blit(text, (win_width - 10 - text.get_width(), 0))
	win.blit(text3, (win_width - 10 - text3.get_width(), 20))
	win.blit(text2, (win_width - 140 - text2.get_width(), 0))
	win.blit(text4, (win_width - 10 - text4.get_width(), 40))
	win.blit(text5, (win_width - 140 - text5.get_width(), 20))

	pygame.display.update()

def check_exit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit(), pygame.QUIT, os.QUIT()

def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

""" 
For self playing!

def lost(win):
	text = STAT_FONT.render("Sorry, you lost!", 1, (255,0,0))
	win.blit(text, (600 -144, 100))
	print(text.get_width())
	pygame.display.update()

def input(dino):
	if pygame.key.get_pressed()[pygame.K_SPACE]:
		dino.jump_count = 15
"""

def remove(index, dinosours, ge, nets):
    dinosours.pop(index)
    ge.pop(index)
    nets.pop(index)

def main(genomes, config):
	global gen, score, pop_size

	nets = []
	ge = []
	dinosours = []

	win = pygame.display.set_mode((win_width, win_height))
	pygame.display.set_caption("Dino Game")
	clock = pygame.time.Clock()
	base = Base(0)
	obstacle = Obstacles(400)

	for id, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		dinosours.append(Dino(100, 93))
		g.fitness = 0 
		ge.append(g)


	while True:
		clock.tick(120)

		draw(win, dinosours, base, obstacle, pop_size, obstacle.vel, gen, scores)

		base.move()
		obstacle.move()

		for x, dino in enumerate(dinosours): 
			output = nets[x].activate((dino.y, distance((dino.x, dino.y),(obstacle.x, obstacle.height)), distance((dino.x, dino.y),(obstacle.x_bird, 140))))
			output1 = nets[x].activate((dino.y, distance((dino.x, dino.y),(obstacle.x_bird, 140)), distance((dino.x, dino.y),(obstacle.x, obstacle.height))))

			if output[0] > 0.5 and dino.y == 93:
				ge[x].fitness += 6
				dino.jump_count = 15
			if output1[0] > 0.5 and dino.y == 93:
				ge[x].fitness += 6
				dino.count1 = 16

		for dino in dinosours:
			dino.dino_down1()
			dino.dino_jump1()
			dino.draw(win)
			pygame.display.update()

			check_exit()

			base.vel += 0.0005
			obstacle.vel += 0.0005

		for i, dino in enumerate(dinosours):
			if obstacle.collide(dino) == True:
				for g in ge:
					pop_size -= 1 
					g.fitness -= 6
				remove(i, dinosours, ge, nets)

		if len(dinosours) == 0:
			scores.append(round(score))
			scores.sort()

			score = 0
			gen += 1
			pop_size = 5050 

			break

def run(config_path):
	 config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	 p = neat.Population(config)
	 p.add_reporter(neat.StdOutReporter(True))

	 stats = neat.StatisticsReporter()

	 p.add_reporter(stats)
	 p.run(main)

if __name__ == "__main__":
	scores = [0]
	gen = 1 

	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")

	run(config_path)