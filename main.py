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
G = 6.67e-11

class Particle:
    color = WHITE
    def __init__(self, position_array, radius, mass, velocity):
        self.position = position_array
        self.r = radius
        self.m = mass
        self.velocity = velocity

    # Calculate new position in one timestep increment, thru the sum of all forces of gravity affecting the particle. returns new position.
    def calc_position(self, part_list):
        # Calculate force betewen self and each particle.
        g_force_sum = np.array([0, 0])
        for particle in part_list:
            if particle != self:
                distance = (particle.position - self.position) ** 2
                g_force = self.mass * particle.mass * G / (distance ** 2) #g_force is currently a scalar. must transform into correct vector.
                g_force_sum = np.add(g_force_sum, g_force)


        pass


#GENERATE PARTICLES
particles = []
for i in range(POP):
    mass = 1
    radius = 1
    velocity = 0
    position = np.array([rand.randint(0, WIDTH), rand.randint(0, HEIGHT)])
    particle = Particle(position, mass, radius, velocity)
    particles.append(particle)
particles = np.array(particles)

def draw():
    for i in range(len(particles)):
        pygame.draw.circle(WIN, WHITE, (particles[i].calc_position(particles)))
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