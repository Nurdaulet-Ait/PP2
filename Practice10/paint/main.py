import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

current_color = BLACK  # текущий цвет
mode = "brush"         # режим рисования
drawing = False        # рисуем или нет

canvas = pygame.Surface((800, 600))
canvas.fill(WHITE)

start_pos = None

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # нажали мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # отпустили мышь
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if mode == "rect":
                pygame.draw.rect(canvas, current_color, (*start_pos, 100, 60))

            if mode == "circle":
                pygame.draw.circle(canvas, current_color, start_pos, 40)

        # движение мыши
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == "brush":
                    pygame.draw.circle(canvas, current_color, event.pos, 5)

                if mode == "eraser":
                    pygame.draw.circle(canvas, WHITE, event.pos, 15)

        # клавиши (смена инструмента)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = RED
            if event.key == pygame.K_g:
                current_color = GREEN
            if event.key == pygame.K_b:
                current_color = BLUE
            if event.key == pygame.K_e:
                mode = "eraser"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_t:
                mode = "rect"
            if event.key == pygame.K_p:
                mode = "brush"

    # рисуем на экран
    screen.blit(canvas, (0, 0))

    pygame.display.flip()
    clock.tick(60)