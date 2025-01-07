import pygame
import math
import numpy as np
import random as rand
import cProfile
import time

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator 2")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POP = 100
G = 6.67e-11
TIME_STEP = 0.25
MASS_START = 1e11

# To calculate the magnitude for vectors.
def _magnitude(array):
    magnitude = math.sqrt(array[0] ** 2 + array[1] ** 2)
    return magnitude

class Particle:
    color = WHITE

    def __init__(self, position_array, mass, radius, velocity):
        self.position = position_array
        self.radius = radius
        self.mass = mass
        self.velocity_vector = velocity
        self.exists = True

    def collision(self, other_particle):
        print("Collision!")
        self.mass = self.mass + other_particle.mass
        self.radius = math.sqrt(self.mass / MASS_START) # Increases the radius by a factor of the square of it's mass according to A = pi * r^2
        # v3 = (m1v1 + m2v2) / (m1 + m2)
        final_collision_velocity = (self.mass * self.velocity_vector + other_particle.mass * other_particle.velocity_vector) / (self.mass + other_particle.mass)
        self.velocity_vector = np.add(self.velocity_vector, final_collision_velocity)
        other_particle.exists = False

    def add_g_forces(self, other_particle, distance_magnitude, g_force_sum_vector):
        theta = math.atan2(other_particle.position[1] - self.position[1], other_particle.position[0] - self.position[0])
        g_force = self.mass * other_particle.mass * G / (distance_magnitude ** 2)
        g_force_vector = np.array([g_force * math.cos(theta), g_force * math.sin(theta)])
        g_force_sum_vector = np.add(g_force_sum_vector, g_force_vector)
        return g_force_sum_vector

    def physics_engine(self, particle_list):
        g_force_sum_vector = np.array([0, 0])
        for other_particle in particle_list:
            if other_particle != self:
                distance_vector = other_particle.position - self.position
                distance_magnitude = _magnitude(distance_vector)
                # Check to see if particles collide or not, and perform collision calc once on larger particle.
                if distance_magnitude <= self.radius + other_particle.radius and self.mass >= other_particle.mass:
                    self.collision(other_particle)
                else:
                    g_force_sum_vector = self.add_g_forces(other_particle, distance_magnitude, g_force_sum_vector)

        # Calculate final velocity, then calculate and return final position.
        acceleration_vector = np.array([f / self.mass for f in g_force_sum_vector])
        self.velocity_vector = np.add(self.velocity_vector, (acceleration_vector * TIME_STEP))
        self.position = np.add(self.position, (self.velocity_vector * TIME_STEP))
        return self.position

particles = []


#GENERATE PARTICLES
for i in range(POP):
    radius = 1
    velocity = 0
    position = np.array([rand.randint(0, WIDTH), rand.randint(0, HEIGHT)])
    particle = Particle(position, MASS_START, radius, velocity)
    particles.append(particle)
particles = np.array(particles)

#Removes any particles that have been absorbed (particle.exists == False) through a collision.
def remove_absorbed():
    global particles
    particles = [particle for particle in particles if particle.exists]

#For actually drawing in the stuff into Pygame.
def draw():
    for i in range(len(particles)):
        particle = particles[i].physics_engine(particles)
        pygame.draw.circle(WIN, WHITE, particle, particles[i].radius)


running = True
clock = pygame.time.Clock()
#Some code from optimization attempts.
with cProfile.Profile() as profile:
    while running:
        clock.tick(60)
        WIN.fill(BLACK)
        OPT_current_time = time.time()
        #if OPT_current_time - OPT_timer_start > 5:
        #    running = False
        remove_absorbed()
        #print("Particle Count :", len(particles))
        draw()
        # Update list to not include particles that don't exist. FIX THIS THING
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

pygame.quit()