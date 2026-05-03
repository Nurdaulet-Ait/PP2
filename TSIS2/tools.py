import pygame
from collections import deque


def flood_fill(surface, x, y, new_color):
    """Flood fill using exact color match with get_at and set_at."""
    width, height = surface.get_size()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))
    new_color = pygame.Color(*new_color)

    if old_color == new_color:
        return

    queue = deque([(x, y)])

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def draw_shape(surface, shape, start_pos, end_pos, color, brush_size):
    """Draw line and all required shapes with active brush size."""
    x1, y1 = start_pos
    x2, y2 = end_pos

    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

    if shape == "line":
        pygame.draw.line(surface, color, start_pos, end_pos, brush_size)

    elif shape == "rect":
        pygame.draw.rect(surface, color, rect, brush_size)

    elif shape == "circle":
        pygame.draw.ellipse(surface, color, rect, brush_size)

    elif shape == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        square_rect = pygame.Rect(
            x1,
            y1,
            side if x2 >= x1 else -side,
            side if y2 >= y1 else -side,
        )
        square_rect.normalize()
        pygame.draw.rect(surface, color, square_rect, brush_size)

    elif shape == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif shape == "equilateral_triangle":
        points = [
            ((x1 + x2) // 2, y1),
            (x1, y2),
            (x2, y2),
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif shape == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y),
        ]
        pygame.draw.polygon(surface, color, points, brush_size)
