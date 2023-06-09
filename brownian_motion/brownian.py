import pygame
import random
import pymunk
import pymunk.pygame_util
pymunk.pygame_util.positive_v_is_up=False

pygame.init()

PURPLE=(255,0,255)
RED =(255,0,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
pygame.display.set_caption("Броуновское движение")
pygame.display.set_icon(pygame.image.load("nt.png"))
display=pygame.display.set_mode((800,800))
clock=pygame.time.Clock()
space=pymunk.Space()
FPS=90

class Particle():
	def __init__(self,x, y, mass=5, radius=50, velocity=0.1, density=1, elastic=0.8):
		self.x=x
		self.y=y
		self.mass=mass
		self.radius=radius
		self.moment=pymunk.moment_for_circle(self.mass,0,self.radius)
		self.body=pymunk.Body(self.mass,self.moment)
		self.body.position=x,y
		self.body.velocity=velocity,velocity
		self.shape=pymunk.Circle(self.body,self.radius)
		self.shape.density=density
		self.shape.elasticity= elastic
		space.add(self.body,self.shape)

	def draw(self):
		x,y=self.body.position
		pygame.draw.circle(display,BLUE,(int(x),int(y)),self.radius)

class Atom(Particle):
	def __init_(self, x, y, mass, radius, velocity, density, elastic ):
		super().__init__( x, y, mass, radius, velocity, density, elastic)

	def draw(self):
		x, y = self.body.position
		pygame.draw.circle(display,PURPLE,(int(x),int(y)),self.radius)

class Wall():
	def __init__(self,p1,p2):
		self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
		self.shape=pymunk.Segment(self.body,p1,p2,5)
		self.shape.elasticity=1
		space.add(self.body,self.shape)

def game():
    atoms=[Atom(random.randint(0,800),random.randint(0,800), 1,8,random.uniform(-100,100),1, 1) for i in range(450)]
    particles=[Particle(random.randint(0,800),random.randint(0,800)) for i in range(5)]
    walls=[Wall((0,0),(0,800)),
 				Wall((0,0),(800,0)),
 				Wall((0,800),(800,800)),
 				Wall((800,0),(800,800))]

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
               exit()

        display.fill((0,0,0))
        for atom in atoms:
            atom.draw()
            for particle in particles:
                particle.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()

