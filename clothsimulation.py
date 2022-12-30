import pygame
from math import sqrt
import numpy as np

w = 10


class VerletPhysics:
    def __init__(self):
        self.particles = []
        self.springs = []
        self.behaviours = []

    def addParticle(self, p):
        self.particles.append(p)

    def addSpring(self, s):
        self.springs.append(s)

    def addBehaviour(self, b):
        self.behaviours.append(b)

    def update(self):

        for p in self.particles:
            if not p.locked:
                for b in self.behaviours:
                    p.x += b[0]
                    p.y += b[1]

        for s in self.springs:
            dx = s.b.x - s.a.x
            dy = s.b.y - s.a.y

            distance = sqrt(dx**2 + dy**2)
            difference = s.restLength - distance
            percent = s.strength * difference / distance / 2

            offSetX = dx * percent
            offSetY = dy * percent

            if not s.a.locked:
                s.a.x -= offSetX
                s.a.y -= offSetY

            if not s.b.locked:
                s.b.x += offSetX
                s.b.y += offSetY

        for p in self.particles:
            vx = p.x - p.oldx
            vy = p.y - p.oldy

            p.oldx = p.x
            p.oldy = p.y

            if not p.locked:
                p.x += vx
                p.y += vy


physics = VerletPhysics()
gravity = [0, 0.05]
physics.addBehaviour(gravity)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.oldx = self.x
        self.oldy = self.y
        self.locked = False

    def display(self):
        pygame.draw.ellipse(screen, BLACK, [self.x - 5, self.y - 5, 10, 10], 2)

    def lock(self):
        self.locked = True


class Spring:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.restLength = 10
        self.strength = 0.97

    def display(self):
        pygame.draw.line(screen, BLACK, [self.a.x, self.a.y], [self.b.x, self.b.y], 1)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

particles = []
springs = []


x = 100


for i in range(40):
    particles.append([])
    y = 10
    for j in range(40):
        p = Particle(x, y)
        particles[i].append(p)
        physics.addParticle(p)
        y += w
    x += w


for i in range(len(particles)):
    for j in range(len(particles)):
        a = particles[i][j]

        if i + 1 <= len(particles) - 1:

            b1 = particles[i + 1][j]
            s1 = Spring(a, b1)
            springs.append(s1)
            physics.addSpring(s1)

        if j + 1 <= len(particles) - 1:
            b2 = particles[i][j + 1]
            s2 = Spring(a, b2)
            springs.append(s2)
            physics.addSpring(s2)


# for i in range(len(particles) - 20):
#     particles[i][0].lock()

particles[0][0].lock()
# particles[10][0].lock()
# particles[20][20].lock()
particles[39][0].lock()

print(len(springs))

pygame.init()

# Set the width and height of the screen [width, height]
size = (600, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Verlet Physics")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    physics.update()
    # print(particles[39].x, particles[39].y)

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)

    # --- Drawing code should go here
    # for row in particles:
    #    for p in row:
    #        p.display()

    for s in springs:
        s.display()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()

