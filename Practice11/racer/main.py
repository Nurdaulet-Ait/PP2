import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Practice 11 Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

player_x = 180
player_y = 500

enemy_x = random.randint(60, 300)
enemy_y = -100
enemy_speed = 5

coin_x = random.randint(70, 330)
coin_y = -50
coin_speed = 5

coins = 0

coin_types = [
    {"weight": 1, "color": (255, 255, 0), "radius": 10},
    {"weight": 2, "color": (255, 165, 0), "radius": 13},
    {"weight": 3, "color": (255, 0, 255), "radius": 16}
]

current_coin = random.choice(coin_types)

def new_coin():
    # создаем новую монету со случайным весом
    global coin_x, coin_y, current_coin
    coin_x = random.randint(70, 330)
    coin_y = -50
    current_coin = random.choice(coin_types)

def new_enemy():
    # создаем нового врага сверху
    global enemy_x, enemy_y
    enemy_x = random.randint(60, 300)
    enemy_y = -100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # управление машиной
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= 6
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += 6

    # не даем машине выйти за дорогу
    if player_x < 55:
        player_x = 55
    if player_x > 305:
        player_x = 305

    enemy_y += enemy_speed
    coin_y += coin_speed

    # если враг ушел вниз, появляется новый
    if enemy_y > 600:
        new_enemy()

    # если монета ушла вниз, появляется новая
    if coin_y > 600:
        new_coin()

    player_rect = pygame.Rect(player_x, player_y, 40, 80)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 40, 80)
    coin_rect = pygame.Rect(
        coin_x - current_coin["radius"],
        coin_y - current_coin["radius"],
        current_coin["radius"] * 2,
        current_coin["radius"] * 2
    )

    # сбор монеты
    if player_rect.colliderect(coin_rect):
        coins += current_coin["weight"]
        new_coin()

        # каждые 5 очков скорость врага увеличивается
        if coins % 5 == 0:
            enemy_speed += 1

    # столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        pygame.quit()
        sys.exit()

    # фон: трава и дорога
    screen.fill((0, 150, 0))
    pygame.draw.rect(screen, (60, 60, 60), (50, 0, 300, 600))

    # линии дороги
    for y in range(0, 600, 80):
        pygame.draw.rect(screen, (255, 255, 255), (195, y, 10, 40))

    # игрок, враг и монета
    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    pygame.draw.rect(screen, (255, 0, 0), enemy_rect)
    pygame.draw.circle(screen, current_coin["color"], (coin_x, coin_y), current_coin["radius"])

    # счет в правом верхнем углу
    text = font.render("Coins: " + str(coins), True, (255, 255, 255))
    screen.blit(text, (400 - text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)
