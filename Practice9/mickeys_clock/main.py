import math
import os
from datetime import datetime

import pygame

pygame.init()

WIDTH, HEIGHT = 700, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
BLUE = (40, 100, 220)
RED = (220, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 28)
small_font = pygame.font.SysFont('Arial', 20)

BASE_DIR = os.path.dirname(__file__)
face = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mickey_face.png')).convert_alpha()
right_hand = pygame.image.load(os.path.join(BASE_DIR, 'images', 'right_hand.png')).convert_alpha()
left_hand = pygame.image.load(os.path.join(BASE_DIR, 'images', 'left_hand.png')).convert_alpha()
face = pygame.transform.smoothscale(face, (360, 360))
right_hand = pygame.transform.smoothscale(right_hand, (48, 170))
left_hand = pygame.transform.smoothscale(left_hand, (42, 145))

center = (WIDTH // 2, HEIGHT // 2)

def blit_rotate_center(surface, image, center_pos, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center_pos)
    surface.blit(rotated_image, new_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.now()
    minute = now.minute
    second = now.second

    # 0 minutes/seconds points up. pygame rotates counterclockwise, so use negative angle.
    minute_angle = -(minute * 6)
    second_angle = -(second * 6)

    screen.fill(WHITE)

    # clock circle
    pygame.draw.circle(screen, GRAY, center, 250, 4)
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        outer = (center[0] + math.cos(angle) * 240, center[1] + math.sin(angle) * 240)
        inner_len = 220 if i % 5 == 0 else 232
        inner = (center[0] + math.cos(angle) * inner_len, center[1] + math.sin(angle) * inner_len)
        pygame.draw.line(screen, BLACK, inner, outer, 3 if i % 5 == 0 else 1)

    # face
    face_rect = face.get_rect(center=center)
    screen.blit(face, face_rect)

    # hands. Right hand = minutes, Left hand = seconds.
    blit_rotate_center(screen, right_hand, center, minute_angle)
    blit_rotate_center(screen, left_hand, center, second_angle)
    pygame.draw.circle(screen, BLACK, center, 8)

    text = font.render(now.strftime('%M:%S'), True, BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 610))
    help_text = small_font.render('Right hand = minutes | Left hand = seconds', True, BLACK)
    screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, 645))

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
