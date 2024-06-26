import pygame
import random
import math

pygame.init()

win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Boids Simulator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

num_boids = 50
boid_size = 10
max_speed = 3
avoidance_distance = 25
cohesion_distance = 100
alignment_distance = 50
cohesion_strength = 0.01
alignment_strength = 0.1

# Initialisierung der Boids
boids = []
for _ in range(num_boids):
    x = random.randint(boid_size, win_width - boid_size)
    y = random.randint(boid_size, win_height - boid_size)
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, max_speed)
    boids.append([x, y, angle, speed])

def move_boids():
    for i in range(num_boids):
        # Bewegung basierend auf aktuellem Winkel und Geschwindigkeit
        x, y, angle, speed = boids[i]
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        x += dx
        y += dy

        # Randbedingungen (wrap-around)
        if x < -boid_size:
            x = win_width + boid_size
        elif x > win_width + boid_size:
            x = -boid_size
        if y < -boid_size:
            y = win_height + boid_size
        elif y > win_height + boid_size:
            y = -boid_size

        # Aktualisierte Position speichern
        boids[i][0] = x
        boids[i][1] = y

def draw_boids():
    for boid in boids:
        x, y = int(boid[0]), int(boid[1])
        pygame.draw.rect(win, RED, (x - boid_size // 2, y - boid_size // 2, boid_size, boid_size))

def update():
    move_boids()

def draw():
    win.fill(WHITE)
    draw_boids()
    pygame.display.flip()

# Hauptprogrammschleife
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    draw()

    clock.tick(60)

pygame.quit()
