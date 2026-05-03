import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Moving Ball')
clock = pygame.time.Clock()

radius = 25
x = WIDTH // 2
y = HEIGHT // 2
step = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x - step - radius >= 0:
                x -= step
            elif event.key == pygame.K_RIGHT and x + step + radius <= WIDTH:
                x += step
            elif event.key == pygame.K_UP and y - step - radius >= 0:
                y -= step
            elif event.key == pygame.K_DOWN and y + step + radius <= HEIGHT:
                y += step

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
