import pygame
from game import SnakeGame
from db import init_db
from settings_manager import load_settings, save_settings

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")

FONT = pygame.font.SysFont("Arial", 28)
SMALL_FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 42)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
DARK = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (0, 90, 220)


def draw_text(surface, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)
    return rect


def button(surface, text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    color = (160, 160, 160) if rect.collidepoint(mouse) else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=8)
    draw_text(surface, text, FONT, BLACK, x + w // 2, y + h // 2, center=True)
    return rect


def main_menu(screen, settings):
    username = ""
    active = True
    clock = pygame.time.Clock()

    while True:
        screen.fill((235, 245, 235))
        draw_text(screen, "TSIS4 Snake Game", BIG_FONT, BLACK, WIDTH // 2, 70, center=True)
        draw_text(screen, "Enter username:", SMALL_FONT, BLACK, 250, 130)

        input_rect = pygame.Rect(250, 160, 300, 40)
        pygame.draw.rect(screen, WHITE, input_rect)
        pygame.draw.rect(screen, BLUE if active else BLACK, input_rect, 2)
        draw_text(screen, username + "|", FONT, BLACK, 260, 165)

        play_btn = button(screen, "Play", 300, 230, 200, 45)
        lb_btn = button(screen, "Leaderboard", 300, 290, 200, 45)
        settings_btn = button(screen, "Settings", 300, 350, 200, 45)
        quit_btn = button(screen, "Quit", 300, 410, 200, 45)

        draw_text(screen, "Tip: username is required for database leaderboard", SMALL_FONT, DARK, WIDTH // 2, 500, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", username

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif play_btn.collidepoint(event.pos):
                    if username.strip():
                        return "play", username.strip()
                elif lb_btn.collidepoint(event.pos):
                    return "leaderboard", username.strip()
                elif settings_btn.collidepoint(event.pos):
                    return "settings", username.strip()
                elif quit_btn.collidepoint(event.pos):
                    return "quit", username.strip()
                else:
                    active = False

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        return "play", username.strip()
                else:
                    if len(username) < 20 and event.unicode.isprintable():
                        username += event.unicode

        clock.tick(60)


def leaderboard_screen(screen):
    from db import get_top_scores

    clock = pygame.time.Clock()
    rows = get_top_scores()

    while True:
        screen.fill((245, 245, 255))
        draw_text(screen, "Leaderboard Top 10", BIG_FONT, BLACK, WIDTH // 2, 45, center=True)
        draw_text(screen, "Rank   Name              Score   Level   Date", SMALL_FONT, BLACK, 70, 110)

        y = 145
        for i, row in enumerate(rows, 1):
            name, score, level, played_at = row
            date_text = str(played_at)[:16]
            line = f"{i:<5}  {name[:14]:<14}  {score:<6}  {level:<5}  {date_text}"
            draw_text(screen, line, SMALL_FONT, BLACK, 70, y)
            y += 32

        back_btn = button(screen, "Back", 300, 520, 200, 45)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and back_btn.collidepoint(event.pos):
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        clock.tick(60)


def settings_screen(screen, settings):
    clock = pygame.time.Clock()
    colors = [(0, 180, 0), (0, 120, 255), (255, 120, 0), (180, 0, 180), (0, 0, 0)]

    while True:
        screen.fill((245, 245, 245))
        draw_text(screen, "Settings", BIG_FONT, BLACK, WIDTH // 2, 60, center=True)

        grid_btn = button(screen, f"Grid: {'ON' if settings['grid'] else 'OFF'}", 280, 140, 240, 45)
        sound_btn = button(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 280, 205, 240, 45)

        draw_text(screen, "Snake color:", FONT, BLACK, 280, 285)
        color_rects = []
        x = 280
        for c in colors:
            r = pygame.Rect(x, 330, 45, 45)
            pygame.draw.rect(screen, c, r)
            pygame.draw.rect(screen, BLACK, r, 3 if list(c) == settings["snake_color"] else 1)
            color_rects.append((r, c))
            x += 55

        save_btn = button(screen, "Save & Back", 280, 450, 240, 45)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu"

                for rect, col in color_rects:
                    if rect.collidepoint(event.pos):
                        settings["snake_color"] = list(col)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings)
                return "menu"

        clock.tick(60)


def game_over_screen(screen, result):
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 235, 235))
        draw_text(screen, "Game Over", BIG_FONT, RED, WIDTH // 2, 80, center=True)
        draw_text(screen, f"Score: {result['score']}", FONT, BLACK, WIDTH // 2, 160, center=True)
        draw_text(screen, f"Level reached: {result['level']}", FONT, BLACK, WIDTH // 2, 205, center=True)
        draw_text(screen, f"Personal best: {result['best']}", FONT, BLACK, WIDTH // 2, 250, center=True)

        retry_btn = button(screen, "Retry", 300, 340, 200, 45)
        menu_btn = button(screen, "Main Menu", 300, 400, 200, 45)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"
                if menu_btn.collidepoint(event.pos):
                    return "menu"

        clock.tick(60)


def main():
    settings = load_settings()
    init_db()

    state = "menu"
    username = ""
    last_result = None

    while True:
        if state == "menu":
            state, username = main_menu(screen, settings)

        elif state == "play":
            game = SnakeGame(screen, username, settings)
            last_result = game.run()
            state = "game_over"

        elif state == "retry":
            state = "play"

        elif state == "leaderboard":
            state = leaderboard_screen(screen)

        elif state == "settings":
            state = settings_screen(screen, settings)

        elif state == "game_over":
            state = game_over_screen(screen, last_result)

        elif state == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
