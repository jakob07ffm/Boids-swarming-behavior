import pygame
import random
import math
import sys

# Pygame initialisieren
pygame.init()

# Bildschirmgröße
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Simulator")

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Boid-Klasse
class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(random.uniform(2, 4))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1

    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0
        self.edges()

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def flock(self, boids):
        separation = pygame.Vector2(0, 0)
        alignment = pygame.Vector2(0, 0)
        cohesion = pygame.Vector2(0, 0)
        total = 0
        perception_radius = 50

        for other in boids:
            distance = self.position.distance_to(other.position)
            if self != other and distance < perception_radius:
                diff = self.position - other.position
                diff /= distance  # Gewichtung nach Distanz
                separation += diff
                alignment += other.velocity
                cohesion += other.position
                total += 1

        if total > 0:
            separation /= total
            alignment /= total
            cohesion /= total
            cohesion -= self.position

            separation = separation.normalize() * self.max_speed - self.velocity
            alignment = alignment.normalize() * self.max_speed - self.velocity
            cohesion = cohesion.normalize() * self.max_speed - self.velocity

            separation = separation.normalize() * min(separation.length(), self.max_force)
            alignment = alignment.normalize() * min(alignment.length(), self.max_force)
            cohesion = cohesion.normalize() * min(cohesion.length(), self.max_force)

        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(cohesion)

    def draw(self, win):
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        points = [
            self.position + pygame.Vector2(10, 0).rotate(angle),
            self.position + pygame.Vector2(-10, 5).rotate(angle),
            self.position + pygame.Vector2(-10, -5).rotate(angle)
        ]
        pygame.draw.polygon(win, WHITE, points)

# Hauptprogramm
def main():
    clock = pygame.time.Clock()
    FPS = 60
    num_boids = 50
    boids = [Boid() for _ in range(num_boids)]

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(BLACK)

        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw(win)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
