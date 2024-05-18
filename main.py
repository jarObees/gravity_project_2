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
MASS_START = 1e9
particles = []


def _magnitude(array):
    magnitude = math.sqrt(array[0] ** 2 + array[1] ** 2)
    return magnitude


class Particle:
    color = WHITE

    def __init__(self, position_array, mass, radius, velocity):
        self.position = position_array
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.exists = True

    def collision(self, particle):
        self.mass = self.mass + particle.mass
        self.radius = math.sqrt(self.mass / MASS_START) # Increases the radius by a factor of the square of it's mass according to A = pi * r^2
        # v3 = (m1v1 + m2v2) / (m1 + m2)
        final_collision_velocity = (self.mass * self.velocity + particle.mass * particle.velocity) / (self.mass + particle.mass)
        self.velocity = np.add(self.velocity, (final_collision_velocity))

    def add_g_forces(self, particle, distance_magnitude, g_force_sum_vector):
        theta = math.atan2(particle.position[1] - self.position[1], particle.position[0] - self.position[0])
        g_force = self.mass * particle.mass * G / (distance_magnitude ** 2)
        g_force_vector = np.array([g_force * math.cos(theta), g_force * math.sin(theta)])
        g_force_sum_vector = np.add(g_force_sum_vector, g_force_vector)
        return g_force_sum_vector

    def physics_engine(self, part_list):
        g_force_sum_vector = np.array([0, 0])
        for particle in part_list:
            if particle != self:
                distance_vector = particle.position - self.position
                distance_magnitude = _magnitude(distance_vector)
                # Check to see if particles collide or not, and perform collision calc once on larger particle.
                if distance_magnitude <= self.radius + particle.radius and self.mass >= particle.mass:
                    self.collision(particle)
                else:
                    g_force_sum_vector = self.add_g_forces(particle, distance_magnitude, g_force_sum_vector)

        # Calculate final velocity, then calculate and return final position.
        acceleration_vector = np.array([f / self.mass for f in g_force_sum_vector])
        self.velocity = np.add(self.velocity, (acceleration_vector * TIME_STEP))
        self.position = np.add(self.position, (self.velocity * TIME_STEP))
        return self.position


#GENERATE PARTICLES
for i in range(POP):
    radius = 1
    velocity = 0
    position = np.array([rand.randint(0, WIDTH), rand.randint(0, HEIGHT)])
    particle = Particle(position, MASS_START, radius, velocity)
    particles.append(particle)
particles = np.array(particles)

def draw():
    for i in range(len(particles)):
        if particles[i].exists:
            particle = particles[i].physics_engine(particles)
            pygame.draw.circle(WIN, WHITE, particle, particles[i].radius)

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    WIN.fill(BLACK)

    draw()

    # Update list to not include particles that don't exist. FIX THIS THING
    particles = [particle for particle in particles if particle.exists]

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()