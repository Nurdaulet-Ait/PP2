import pygame

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 28)
BIG_FONT = pygame.font.SysFont("Arial", 52)
SMALL_FONT = pygame.font.SysFont("Arial", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
DARK = (35, 35, 35)
BLUE = (50, 120, 255)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        label = FONT.render(self.text, True, BLACK)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, font=FONT, color=BLACK, center=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)


def ask_username(screen, clock, width, height):
    name = ""
    active = True
    while active:
        screen.fill((25, 25, 25))
        draw_text(screen, "Enter your name", width // 2, 180, BIG_FONT, WHITE, True)
        pygame.draw.rect(screen, WHITE, (width // 2 - 180, 270, 360, 55), border_radius=8)
        draw_text(screen, name + "|", width // 2 - 165, 282, FONT, BLACK)
        draw_text(screen, "Press ENTER to start", width // 2, 370, SMALL_FONT, WHITE, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player", True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return (name.strip() or "Player"), False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode
        clock.tick(60)
