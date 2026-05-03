import os
import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 720, 420
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
DARK = (45, 45, 45)
BLUE = (60, 110, 220)
GREEN = (0, 160, 90)
RED = (210, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Music Player')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 28)
small_font = pygame.font.SysFont('Arial', 22)

BASE_DIR = os.path.dirname(__file__)
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

playlist = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
playlist.sort()

current = 0
is_playing = False
start_ticks = 0
paused_position = 0

def load_and_play(index):
    global is_playing, start_ticks, paused_position
    if not playlist:
        return
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, playlist[index]))
    pygame.mixer.music.play()
    is_playing = True
    paused_position = 0
    start_ticks = pygame.time.get_ticks()

def stop_music():
    global is_playing, paused_position
    pygame.mixer.music.stop()
    is_playing = False
    paused_position = 0

def next_track():
    global current
    if not playlist:
        return
    current = (current + 1) % len(playlist)
    load_and_play(current)

def previous_track():
    global current
    if not playlist:
        return
    current = (current - 1) % len(playlist)
    load_and_play(current)

def draw_button(x, y, w, h, text, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    label = small_font.render(text, True, WHITE)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                if playlist:
                    load_and_play(current)
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                previous_track()

    if is_playing and not pygame.mixer.music.get_busy():
        next_track()

    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, (70, 45, 580, 320), border_radius=25)
    pygame.draw.rect(screen, DARK, (100, 80, 520, 90), border_radius=18)

    title = font.render('Pygame Music Player', True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 15))

    if playlist:
        track_text = small_font.render('Current track: ' + playlist[current], True, WHITE)
        status = 'Playing' if is_playing else 'Stopped'
        status_text = small_font.render('Status: ' + status, True, GREEN if is_playing else RED)
        screen.blit(track_text, (125, 100))
        screen.blit(status_text, (125, 130))
    else:
        no_music = small_font.render('No music found. Run create_sample_tracks.py first.', True, WHITE)
        screen.blit(no_music, (120, 115))

    # progress bar. For sample tracks, visual progress is estimated.
    elapsed = 0
    if is_playing:
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
    progress = min(elapsed / 4, 1) if is_playing else 0
    pygame.draw.rect(screen, WHITE, (120, 205, 480, 22), border_radius=10)
    pygame.draw.rect(screen, BLUE, (120, 205, int(480 * progress), 22), border_radius=10)

    draw_button(100, 270, 105, 55, 'P Play', GREEN)
    draw_button(220, 270, 105, 55, 'S Stop', RED)
    draw_button(340, 270, 105, 55, 'N Next', BLUE)
    draw_button(460, 270, 105, 55, 'B Back', BLUE)

    info = small_font.render('Q = Quit', True, BLACK)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 375))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
