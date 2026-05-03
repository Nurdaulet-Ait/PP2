import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

snake = [(300, 300)]  # тело змейки
dx, dy = 20, 0        # направление

food = (100, 100)

score = 0
level = 1
speed = 8

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx, dy = 0, -20
            if event.key == pygame.K_DOWN:
                dx, dy = 0, 20
            if event.key == pygame.K_LEFT:
                dx, dy = -20, 0
            if event.key == pygame.K_RIGHT:
                dx, dy = 20, 0

    # движение змейки
    head = (snake[0][0] + dx, snake[0][1] + dy)

    # проверка выхода за границы
    if head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 600:
        print("Game Over")
        pygame.quit()
        sys.exit()

    # проверка столкновения с собой
    if head in snake:
        print("Game Over")
        pygame.quit()
        sys.exit()

    snake.insert(0, head)

    # если съели еду
    if head == food:
        score += 1

        # уровень растет каждые 3 очка
        if score % 3 == 0:
            level += 1
            speed += 2

        food = (random.randrange(0, 600, 20), random.randrange(0, 600, 20))
    else:
        snake.pop()

    # фон
    screen.fill((255, 255, 255))
    # сетка
    for x in range(0, 600, 20):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, 600))
    for y in range(0, 600, 20):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (600, y))

    # рисуем змейку
    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, 20, 20))

    # рисуем еду
    pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))

    pygame.display.flip()
    clock.tick(speed)