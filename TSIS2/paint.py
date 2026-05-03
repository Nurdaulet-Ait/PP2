import pygame
from datetime import datetime
from tools import flood_fill, draw_shape

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
LIGHT_GRAY = (245, 245, 245)
SELECTED = (180, 210, 255)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 180, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 128, 0),
    (128, 0, 255),
    (255, 255, 255),
]

tools = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("square", "Square"),
    ("right_triangle", "R-Tri"),
    ("equilateral_triangle", "E-Tri"),
    ("rhombus", "Rhombus"),
    ("eraser", "Eraser"),
    ("fill", "Fill"),
    ("text", "Text"),
]

current_tool = "pencil"
current_color = BLACK
brush_size = 5

is_drawing = False
start_pos = None
last_pos = None

is_typing = False
text_pos = None
text_value = ""

clock = pygame.time.Clock()


def to_canvas_pos(mouse_pos):
    return mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT


def draw_button(rect, label, selected=False):
    pygame.draw.rect(screen, SELECTED if selected else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label_surface = font.render(label, True, BLACK)
    screen.blit(label_surface, (rect.x + 5, rect.y + 7))


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10
    y = 8
    for tool_id, label in tools:
        rect = pygame.Rect(x, y, 78, 30)
        draw_button(rect, label, current_tool == tool_id)
        x += 84

    x = 10
    y = 50
    for color in colors:
        rect = pygame.Rect(x, y, 32, 28)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if color == current_color:
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)
        x += 40

    size_text = font.render(f"Brush size: {brush_size}   1=2px  2=5px  3=10px   Ctrl+S=save", True, BLACK)
    screen.blit(size_text, (360, 55))


def get_clicked_tool(mouse_pos):
    x = 10
    y = 8
    for tool_id, label in tools:
        rect = pygame.Rect(x, y, 78, 30)
        if rect.collidepoint(mouse_pos):
            return tool_id
        x += 84
    return None


def get_clicked_color(mouse_pos):
    x = 10
    y = 50
    for color in colors:
        rect = pygame.Rect(x, y, 32, 28)
        if rect.collidepoint(mouse_pos):
            return color
        x += 40
    return None


def save_canvas():
    filename = datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


running = True

while running:
    screen.fill(LIGHT_GRAY)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    mouse_pos = pygame.mouse.get_pos()

    if is_drawing and start_pos and current_tool in [
        "line", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"
    ]:
        preview = canvas.copy()
        current_canvas_pos = to_canvas_pos(mouse_pos)
        draw_shape(preview, current_tool, start_pos, current_canvas_pos, current_color, brush_size)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if is_typing and text_pos:
        text_surface = text_font.render(text_value + "|", True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                save_canvas()

            elif is_typing:
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(text_value, True, current_color)
                    canvas.blit(final_text, text_pos)
                    is_typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    is_typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    clicked_tool = get_clicked_tool(event.pos)
                    clicked_color = get_clicked_color(event.pos)

                    if clicked_tool:
                        current_tool = clicked_tool
                        is_typing = False
                        text_value = ""
                        text_pos = None

                    if clicked_color:
                        current_color = clicked_color

                else:
                    pos = to_canvas_pos(event.pos)

                    if current_tool == "fill":
                        flood_fill(canvas, pos[0], pos[1], current_color)

                    elif current_tool == "text":
                        is_typing = True
                        text_pos = pos
                        text_value = ""

                    else:
                        is_drawing = True
                        start_pos = pos
                        last_pos = pos

        elif event.type == pygame.MOUSEMOTION:
            if is_drawing and pygame.mouse.get_pressed()[0]:
                pos = to_canvas_pos(event.pos)

                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and is_drawing:
                end_pos = to_canvas_pos(event.pos)

                if current_tool in [
                    "line", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"
                ]:
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

                is_drawing = False
                start_pos = None
                last_pos = None

    clock.tick(60)

pygame.quit()
