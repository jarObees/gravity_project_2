import pygame
import math
import numpy as np
import random as rand
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator 2")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POP = 100

class Particle:
    color = WHITE
    def __init__(self, position_array, radius, mass):
        self.position = position_array
        self.r = radius
        self.m = mass

    # Calculate new position, using dt, and sum of all forces of gravity affecting the particle
    def calc_position(self, part_list):
        pass


#GENERATE PARTICLES
particles = []
for i in range(POP):
    mass = 1
    radius = 1
    position = np.array([rand.randint(0, WIDTH), rand.randint(0, HEIGHT)])
    particle = Particle(position, mass, radius)
    particles.append(particle)
particles = np.array(particles)

def draw():
    for i in range(len(particles)):
        #pygame.draw.circle(WIN, WHITE, (TUPLE HERE)        TO DO: Make the tuple the final position of the object.
        pass
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    WIN.fill(BLACK)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()