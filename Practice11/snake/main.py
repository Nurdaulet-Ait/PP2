import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Practice 11 Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

cell = 20
snake = [(300, 300)]
dx, dy = cell, 0

score = 0
speed = 8

food_types = [
    {"weight": 1, "color": (255, 0, 0)},
    {"weight": 2, "color": (255, 165, 0)},
    {"weight": 3, "color": (180, 0, 255)}
]

food = None
food_type = None
food_start_time = 0
food_lifetime = 4000

def create_food():
    # создаем еду в случайном месте
    global food, food_type, food_start_time

    while True:
        x = random.randrange(0, 600, cell)
        y = random.randrange(0, 600, cell)

        if (x, y) not in snake:
            food = (x, y)
            break

    # у еды есть разный вес
    food_type = random.choice(food_types)

    # запоминаем время появления еды
    food_start_time = pygame.time.get_ticks()

create_food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление змейкой
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and dy != cell:
                dx, dy = 0, -cell
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy != -cell:
                dx, dy = 0, cell
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx != cell:
                dx, dy = -cell, 0
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx != -cell:
                dx, dy = cell, 0

    # если время еды вышло, создаем новую еду
    current_time = pygame.time.get_ticks()
    if current_time - food_start_time > food_lifetime:
        create_food()

    head = (snake[0][0] + dx, snake[0][1] + dy)

    # проверка стен
    if head[0] < 0 or head[0] >= 600 or head[1] < 0 or head[1] >= 600:
        pygame.quit()
        sys.exit()

    # проверка столкновения с собой
    if head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, head)

    # если съели еду, прибавляем очки по весу еды
    if head == food:
        score += food_type["weight"]
        create_food()
    else:
        snake.pop()

    # белый фон
    screen.fill((255, 255, 255))

    # сетка
    for x in range(0, 600, cell):
        pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, 600))
    for y in range(0, 600, cell):
        pygame.draw.line(screen, (220, 220, 220), (0, y), (600, y))

    # рисуем змейку
    for part in snake:
        pygame.draw.rect(screen, (0, 180, 0), (part[0], part[1], cell, cell))

    # рисуем еду
    pygame.draw.rect(screen, food_type["color"], (food[0], food[1], cell, cell))

    # показываем счет и таймер еды
    time_left = max(0, food_lifetime - (current_time - food_start_time)) // 1000
    text = font.render("Score: " + str(score) + "  Food time: " + str(time_left), True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)
