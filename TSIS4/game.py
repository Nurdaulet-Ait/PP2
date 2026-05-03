import random
import pygame
from db import get_or_create_player, get_personal_best, save_session

CELL = 20
WIDTH, HEIGHT = 800, 600
TOP_BAR = 60
GRID_W = WIDTH // CELL
GRID_H = (HEIGHT - TOP_BAR) // CELL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 100, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 220, 0)
PURPLE = (150, 0, 200)
ORANGE = (255, 140, 0)
GRAY = (100, 100, 100)

class SnakeGame:
    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.player_id = get_or_create_player(username)
        self.personal_best = get_personal_best(username)

        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.eaten = 0
        self.base_speed = 8

        self.food = None
        self.food_spawn_time = 0
        self.food_life = 7000
        self.poison = None

        self.powerup = None
        self.powerup_spawn_time = 0
        self.powerup_life = 8000
        self.active_powerup = None
        self.active_until = 0
        self.shield = False

        self.obstacles = []
        self.clock = pygame.time.Clock()
        self.game_over = False

        self.spawn_food()
        self.spawn_poison()

    def random_empty_cell(self):
        while True:
            pos = (random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))
            if pos not in self.snake and pos not in self.obstacles and pos != self.food and pos != self.poison:
                if self.powerup is None or pos != self.powerup["pos"]:
                    return pos

    def spawn_food(self):
        self.food = {
            "pos": self.random_empty_cell(),
            "value": random.choice([1, 2, 3]),
            "color": random.choice([RED, ORANGE, YELLOW])
        }
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison = self.random_empty_cell()

    def spawn_powerup(self):
        if self.powerup is None and random.random() < 0.015:
            kind = random.choice(["speed", "slow", "shield"])
            color = BLUE if kind == "speed" else PURPLE if kind == "slow" else YELLOW
            self.powerup = {"pos": self.random_empty_cell(), "kind": kind, "color": color}
            self.powerup_spawn_time = pygame.time.get_ticks()

    def create_obstacles(self):
        if self.level < 3:
            self.obstacles = []
            return

        count = min(5 + self.level * 2, 35)
        new_blocks = []
        head = self.snake[0]

        attempts = 0
        while len(new_blocks) < count and attempts < 500:
            attempts += 1
            pos = (random.randint(2, GRID_W - 3), random.randint(2, GRID_H - 3))

            near_head = abs(pos[0] - head[0]) <= 2 and abs(pos[1] - head[1]) <= 2

            if pos in self.snake or pos in new_blocks or near_head:
                continue

            new_blocks.append(pos)

        self.obstacles = new_blocks

    def speed(self):
        speed = self.base_speed + self.level
        now = pygame.time.get_ticks()

        if self.active_powerup == "speed" and now < self.active_until:
            speed += 5

        if self.active_powerup == "slow" and now < self.active_until:
            speed = max(4, speed - 5)

        if self.active_powerup in ["speed", "slow"] and now >= self.active_until:
            self.active_powerup = None

        return speed

    def draw_cell(self, pos, color):
        x = pos[0] * CELL
        y = TOP_BAR + pos[1] * CELL
        pygame.draw.rect(self.screen, color, (x, y, CELL, CELL))
        pygame.draw.rect(self.screen, BLACK, (x, y, CELL, CELL), 1)

    def draw(self):
        self.screen.fill(WHITE)

        pygame.draw.rect(self.screen, (225, 225, 225), (0, 0, WIDTH, TOP_BAR))
        info = f"Player: {self.username} | Score: {self.score} | Level: {self.level} | Best: {self.personal_best}"
        self.screen.blit(self.font.render(info, True, BLACK), (10, 15))

        if self.active_powerup:
            remaining = max(0, (self.active_until - pygame.time.get_ticks()) // 1000)
            text = f"Active: {self.active_powerup} {remaining}s"
            self.screen.blit(self.small_font.render(text, True, BLUE), (560, 40))
        elif self.shield:
            self.screen.blit(self.small_font.render("Shield: ready", True, BLUE), (560, 40))

        if self.settings.get("grid", True):
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(self.screen, (230, 230, 230), (x, TOP_BAR), (x, HEIGHT))
            for y in range(TOP_BAR, HEIGHT, CELL):
                pygame.draw.line(self.screen, (230, 230, 230), (0, y), (WIDTH, y))

        for obs in self.obstacles:
            self.draw_cell(obs, GRAY)

        for part in self.snake:
            self.draw_cell(part, tuple(self.settings["snake_color"]))

        if self.food:
            self.draw_cell(self.food["pos"], self.food["color"])

        if self.poison:
            self.draw_cell(self.poison, DARK_RED)

        if self.powerup:
            self.draw_cell(self.powerup["pos"], self.powerup["color"])

        pygame.display.flip()

    def handle_collision(self, new_head):
        x, y = new_head
        collision = (
            x < 0 or x >= GRID_W or
            y < 0 or y >= GRID_H or
            new_head in self.snake or
            new_head in self.obstacles
        )

        if collision:
            if self.shield:
                self.shield = False
                return False
            return True

        return False

    def update_level(self):
        new_level = self.eaten // 4 + 1
        if new_level > self.level:
            self.level = new_level
            self.create_obstacles()

    def move(self):
        self.direction = self.next_direction
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if self.handle_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        ate = False

        if self.food and new_head == self.food["pos"]:
            self.score += self.food["value"] * 10
            self.eaten += 1
            ate = True
            self.spawn_food()
            self.update_level()

        if self.poison and new_head == self.poison:
            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()
            self.poison = None
            self.spawn_poison()
            if len(self.snake) <= 1:
                self.game_over = True
                return

        if self.powerup and new_head == self.powerup["pos"]:
            kind = self.powerup["kind"]
            self.powerup = None

            if kind == "shield":
                self.active_powerup = None
                self.shield = True
            else:
                self.shield = False
                self.active_powerup = kind
                self.active_until = pygame.time.get_ticks() + 5000
                self.score += 15

        if not ate:
            self.snake.pop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.next_direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True

        return None

    def run(self):
        while not self.game_over:
            status = self.handle_events()
            if status == "quit":
                return {"score": self.score, "level": self.level, "best": self.personal_best}

            now = pygame.time.get_ticks()

            if self.food and now - self.food_spawn_time > self.food_life:
                self.spawn_food()

            if self.powerup and now - self.powerup_spawn_time > self.powerup_life:
                self.powerup = None

            self.spawn_powerup()
            self.move()
            self.draw()
            self.clock.tick(self.speed())

        save_session(self.username, self.score, self.level)
        best = max(self.personal_best, self.score)

        return {
            "score": self.score,
            "level": self.level,
            "best": best
        }
