import pygame

pygame.init()

win_width = 1000
win_height = 1000
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Boids")

BLACK = (0, 0, 0)
RED = (255, 0, 0)

bird_speed = 5

boid_positions = [
    (100, 100),
    (200, 200),
    (300, 300),
    (400, 400),
    (500, 500),
    (600, 600),
    (700, 700),
    (800, 800),
    (900, 900),
]

def draw_boid(win, position):
    x, y = position
    points = [
        (x, y),
        (x + 20, y + 40),
        (x - 20, y + 40)
    ]
    pygame.draw.polygon(win, RED, points)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill(BLACK)

    for position in boid_positions:
        draw_boid(win, position)

    pygame.display.flip()

pygame.quit()
