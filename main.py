import pygame
import math
import numpy as np
import random as rand
WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator 2")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POP = 100
G = 6.67e-11
TIME_STEP = 5


class Particle:
    color = WHITE
    def __init__(self, position_array, mass, radius, velocity):
        self.position = position_array
        self.radius = radius
        self.mass = mass
        self.velocity = velocity

    # Calculate new position in one timestep increment, thru the sum of all forces of gravity affecting the particle. returns new position.
    def calc_position(self, part_list):
        # Calculate vector sum of all forces.
        g_force_sum_vector = np.array([0, 0])
        for particle in part_list:
            if particle != self:
                theta = math.atan2(particle.position[1] - self.position[1], particle.position[0] - self.position[0])
                distance_vector = particle.position - self.position
                distance_magnitude = math.sqrt(distance_vector[0] ** 2 + distance_vector[1] ** 2)
                g_force = self.mass * particle.mass * G / (distance_magnitude ** 2)
                g_force_vector = np.array([g_force * math.cos(theta), g_force * math.sin(theta)])
                g_force_sum_vector = np.add(g_force_sum_vector, g_force_vector)

        # Calculate final velocity, then calculate and return final position.
        acceleration_vector = np.array([f / self.mass for f in g_force_sum_vector])
        self.velocity = np.add(self.velocity, (acceleration_vector * TIME_STEP))
        self.position = np.add(self.position, (self.velocity * TIME_STEP))
        return self.position



#GENERATE PARTICLES
particles = []
for i in range(POP):
    mass = 1e9
    radius = 1
    velocity = 0
    position = np.array([rand.randint(0, WIDTH), rand.randint(0, HEIGHT)])
    particle = Particle(position, mass, radius, velocity)
    particles.append(particle)
particles = np.array(particles)

def draw():
    for i in range(len(particles)):
        pygame.draw.circle(WIN, WHITE, (particles[i].calc_position(particles)), particles[i].radius)

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    WIN.fill(BLACK)
    draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()