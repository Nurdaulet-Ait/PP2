import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Practice 11 Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)

canvas = pygame.Surface((800, 600))
canvas.fill(WHITE)

current_color = BLACK
mode = "square"
drawing = False
start_pos = None

# кнопки цветов
btn_red = pygame.Rect(10, 10, 30, 30)
btn_green = pygame.Rect(50, 10, 30, 30)
btn_blue = pygame.Rect(90, 10, 30, 30)
btn_black = pygame.Rect(130, 10, 30, 30)

# кнопки фигур
btn_square = pygame.Rect(200, 10, 80, 30)
btn_right = pygame.Rect(290, 10, 80, 30)
btn_equal = pygame.Rect(380, 10, 80, 30)
btn_rhombus = pygame.Rect(470, 10, 100, 30)
btn_clear = pygame.Rect(580, 10, 70, 30)

def draw_button(rect, text, active):
    # рисуем кнопку инструмента
    color = (170, 170, 170) if active else (230, 230, 230)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, BLACK)
    screen.blit(label, (rect.x + 5, rect.y + 7))

def draw_panel():
    # верхняя панель с кнопками
    pygame.draw.rect(screen, GRAY, (0, 0, 800, 50))

    pygame.draw.rect(screen, RED, btn_red)
    pygame.draw.rect(screen, GREEN, btn_green)
    pygame.draw.rect(screen, BLUE, btn_blue)
    pygame.draw.rect(screen, BLACK, btn_black)

    pygame.draw.rect(screen, BLACK, btn_red, 2)
    pygame.draw.rect(screen, BLACK, btn_green, 2)
    pygame.draw.rect(screen, BLACK, btn_blue, 2)
    pygame.draw.rect(screen, BLACK, btn_black, 2)

    draw_button(btn_square, "Square", mode == "square")
    draw_button(btn_right, "Right", mode == "right")
    draw_button(btn_equal, "Equal", mode == "equal")
    draw_button(btn_rhombus, "Rhombus", mode == "rhombus")
    draw_button(btn_clear, "Clear", False)

def draw_shape(surface, start, end, outline=0):
    # рисуем выбранную фигуру
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    if size == 0:
        return

    sign_x = 1 if x2 >= x1 else -1
    sign_y = 1 if y2 >= y1 else -1

    if mode == "square":
        rect = pygame.Rect(x1, y1, sign_x * size, sign_y * size)
        rect.normalize()
        pygame.draw.rect(surface, current_color, rect, outline)

    elif mode == "right":
        p1 = (x1, y1)
        p2 = (x1 + sign_x * size, y1)
        p3 = (x1, y1 + sign_y * size)
        pygame.draw.polygon(surface, current_color, [p1, p2, p3], outline)

    elif mode == "equal":
        height = int(size * math.sqrt(3) / 2)
        p1 = (x1, y1 - sign_y * height)
        p2 = (x1 - sign_x * size // 2, y1 + sign_y * height // 2)
        p3 = (x1 + sign_x * size // 2, y1 + sign_y * height // 2)
        pygame.draw.polygon(surface, current_color, [p1, p2, p3], outline)

    elif mode == "rhombus":
        cx, cy = x1, y1
        p1 = (cx, cy - size)
        p2 = (cx + size, cy)
        p3 = (cx, cy + size)
        p4 = (cx - size, cy)
        pygame.draw.polygon(surface, current_color, [p1, p2, p3, p4], outline)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # если нажали на верхнюю панель
            if y <= 50:
                if btn_red.collidepoint(x, y):
                    current_color = RED
                elif btn_green.collidepoint(x, y):
                    current_color = GREEN
                elif btn_blue.collidepoint(x, y):
                    current_color = BLUE
                elif btn_black.collidepoint(x, y):
                    current_color = BLACK
                elif btn_square.collidepoint(x, y):
                    mode = "square"
                elif btn_right.collidepoint(x, y):
                    mode = "right"
                elif btn_equal.collidepoint(x, y):
                    mode = "equal"
                elif btn_rhombus.collidepoint(x, y):
                    mode = "rhombus"
                elif btn_clear.collidepoint(x, y):
                    canvas.fill(WHITE)
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                if end_pos[1] > 50:
                    draw_shape(canvas, start_pos, end_pos)
            drawing = False
            start_pos = None

    screen.blit(canvas, (0, 0))

    # показываем пример фигуры во время рисования
    if drawing and start_pos is not None:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] > 50:
            draw_shape(screen, start_pos, mouse_pos, 2)

    draw_panel()

    pygame.display.flip()
    clock.tick(60)
