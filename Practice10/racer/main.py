import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

player_x = 180
enemy_x = random.randint(50, 300)
enemy_y = -100

coin_x = random.randint(50, 350)
coin_y = -50

coins = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # движение машины
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5

    enemy_y += 5
    coin_y += 5

    # если враг ушел вниз — появляется новый
    if enemy_y > 600:
        enemy_y = -100
        enemy_x = random.randint(50, 300)

    # если монета ушла — новая
    if coin_y > 600:
        coin_y = -50
        coin_x = random.randint(50, 350)

    player_rect = pygame.Rect(player_x, 500, 40, 80)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 40, 80)
    coin_rect = pygame.Rect(coin_x, coin_y, 20, 20)

    # сбор монеты
    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = -50

    # столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        print("Game Over")
        pygame.quit()
        sys.exit()

    # фон (трава + дорога)
    screen.fill((0, 150, 0))  # трава
    # дорога
    pygame.draw.rect(screen, (50, 50, 50), (50, 0, 300, 600))
    # линии на дороге
    for i in range(0, 600, 80):
        pygame.draw.rect(screen, (255, 255, 255), (195, i, 10, 40))

    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    pygame.draw.rect(screen, (255, 0, 0), enemy_rect)
    pygame.draw.circle(screen, (255, 255, 0), (coin_x, coin_y), 10)

    pygame.display.flip()
    clock.tick(60)