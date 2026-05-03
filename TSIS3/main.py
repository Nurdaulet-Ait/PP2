import pygame
from ui import Button, draw_text, ask_username, BIG_FONT, FONT, SMALL_FONT, WHITE, BLACK
from persistence import load_settings, save_settings, load_leaderboard, CAR_COLORS, DIFFICULTIES
from racer import RacerGame

pygame.init()
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")
clock = pygame.time.Clock()
settings = load_settings()


def main_menu():
    buttons = [
        Button(300, 230, 200, 55, "Play"),
        Button(300, 300, 200, 55, "Leaderboard"),
        Button(300, 370, 200, 55, "Settings"),
        Button(300, 440, 200, 55, "Quit")
    ]
    while True:
        screen.fill((25, 25, 25))
        draw_text(screen, "TSIS3 RACER", WIDTH // 2, 130, BIG_FONT, WHITE, True)
        for b in buttons:
            b.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if buttons[0].clicked(event):
                return "play"
            if buttons[1].clicked(event):
                return "leaderboard"
            if buttons[2].clicked(event):
                return "settings"
            if buttons[3].clicked(event):
                return "quit"
        clock.tick(60)


def leaderboard_screen():
    back = Button(300, 610, 200, 50, "Back")
    while True:
        screen.fill((245, 245, 245))
        draw_text(screen, "TOP 10 LEADERBOARD", WIDTH // 2, 60, BIG_FONT, BLACK, True)
        data = load_leaderboard()
        y = 130
        draw_text(screen, "Rank   Name          Score     Distance", 140, y, FONT, BLACK)
        y += 45
        for i, item in enumerate(data[:10], 1):
            line = f"{i:<5}  {item['name']:<12}  {item['score']:<8}  {item['distance']} m"
            draw_text(screen, line, 140, y, SMALL_FONT, BLACK)
            y += 35
        if not data:
            draw_text(screen, "No scores yet", WIDTH // 2, 250, FONT, BLACK, True)
        back.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event):
                return "menu"
        clock.tick(60)


def settings_screen():
    global settings
    sound_btn = Button(270, 190, 260, 50, "")
    color_btn = Button(270, 270, 260, 50, "")
    diff_btn = Button(270, 350, 260, 50, "")
    back = Button(300, 520, 200, 50, "Back")

    color_names = list(CAR_COLORS.keys())
    diff_names = list(DIFFICULTIES.keys())

    while True:
        sound_btn.text = "Sound: ON" if settings["sound"] else "Sound: OFF"
        color_btn.text = "Car color: " + settings["car_color"]
        diff_btn.text = "Difficulty: " + settings["difficulty"]

        screen.fill((245, 245, 245))
        draw_text(screen, "SETTINGS", WIDTH // 2, 90, BIG_FONT, BLACK, True)
        sound_btn.draw(screen)
        color_btn.draw(screen)
        diff_btn.draw(screen)
        back.draw(screen)
        draw_text(screen, "Click buttons to change options", WIDTH // 2, 460, SMALL_FONT, BLACK, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return "quit"
            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            if color_btn.clicked(event):
                i = color_names.index(settings["car_color"])
                settings["car_color"] = color_names[(i + 1) % len(color_names)]
                save_settings(settings)
            if diff_btn.clicked(event):
                i = diff_names.index(settings["difficulty"])
                settings["difficulty"] = diff_names[(i + 1) % len(diff_names)]
                save_settings(settings)
            if back.clicked(event):
                return "menu"
        clock.tick(60)


def game_over_screen():
    retry = Button(300, 380, 200, 55, "Retry")
    menu = Button(300, 450, 200, 55, "Main Menu")
    board = Button(300, 520, 200, 55, "Leaderboard")
    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "GAME OVER", WIDTH // 2, 130, BIG_FONT, WHITE, True)
        draw_text(screen, "Your result was saved to leaderboard.json", WIDTH // 2, 220, FONT, WHITE, True)
        retry.draw(screen)
        menu.draw(screen)
        board.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry.clicked(event):
                return "play"
            if menu.clicked(event):
                return "menu"
            if board.clicked(event):
                return "leaderboard"
        clock.tick(60)


def main():
    state = "menu"
    while state != "quit":
        if state == "menu":
            state = main_menu()
        elif state == "play":
            username, quit_now = ask_username(screen, clock, WIDTH, HEIGHT)
            if quit_now:
                state = "quit"
            else:
                game = RacerGame(screen, clock, settings, username)
                result = game.run()
                state = "quit" if result == "quit" else "game_over"
        elif state == "leaderboard":
            state = leaderboard_screen()
        elif state == "settings":
            state = settings_screen()
        elif state == "game_over":
            state = game_over_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
