import random
import pygame
from persistence import CAR_COLORS, DIFFICULTIES, add_score
from ui import draw_text, Button, FONT, BIG_FONT, SMALL_FONT, WHITE, BLACK

ROAD_X = 220
ROAD_W = 360
LANES = 3
LANE_W = ROAD_W // LANES
HEIGHT = 700
WIDTH = 800
PLAYER_Y = 580

class RacerGame:
    def __init__(self, screen, clock, settings, username):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.username = username
        self.diff = DIFFICULTIES[settings["difficulty"]]
        self.base_speed = self.diff["speed"]
        self.speed = self.base_speed
        self.finish_distance = self.diff["finish_distance"]
        self.player = pygame.Rect(ROAD_X + LANE_W + 30, PLAYER_Y, 60, 90)
        self.car_color = CAR_COLORS[settings["car_color"]]
        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.road_marks_y = 0
        self.distance = 0
        self.coin_count = 0
        self.score = 0
        self.active_power = None
        self.power_end = 0
        self.shield = False
        self.spawn_timer = 0
        self.power_timer = 0
        self.running = True
        self.game_over = False
        self.finished = False

    def lane_x(self, lane):
        return ROAD_X + lane * LANE_W + 30

    def random_lane_rect(self, w=60, h=80):
        lane = random.randint(0, LANES - 1)
        return pygame.Rect(self.lane_x(lane), -h, w, h)

    def safe_to_spawn(self, rect):
        if abs(rect.centerx - self.player.centerx) < 80 and rect.y < 160:
            return False
        for obj in self.traffic + self.obstacles:
            if rect.colliderect(obj["rect"].inflate(20, 90)):
                return False
        return True

    def spawn_objects(self):
        progress = self.distance / 1000
        spawn_rate = max(18, self.diff["spawn_rate"] - int(progress * 5))
        self.spawn_timer += 1
        self.power_timer += 1

        if self.spawn_timer >= spawn_rate:
            self.spawn_timer = 0
            choice = random.choice(["traffic", "traffic", "barrier", "oil", "pothole", "bump", "nitrostrip"])
            rect = self.random_lane_rect()
            if self.safe_to_spawn(rect):
                if choice == "traffic":
                    self.traffic.append({"rect": rect, "color": random.choice([(180, 40, 40), (40, 180, 80), (220, 180, 40)])})
                elif choice in ["barrier", "oil", "pothole"]:
                    self.obstacles.append({"rect": rect, "type": choice})
                elif choice == "bump":
                    self.obstacles.append({"rect": pygame.Rect(rect.x, rect.y, 65, 35), "type": "bump"})
                else:
                    self.obstacles.append({"rect": pygame.Rect(rect.x, rect.y, 65, 35), "type": "nitrostrip"})

        if random.randint(1, 70) == 1:
            rect = self.random_lane_rect(35, 35)
            self.coins.append({"rect": rect, "value": random.choice([1, 2, 5])})

        if self.power_timer >= 260:
            self.power_timer = 0
            rect = self.random_lane_rect(42, 42)
            if self.safe_to_spawn(rect):
                self.powerups.append({"rect": rect, "type": random.choice(["nitro", "shield", "repair"]), "life": 300})

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move = 7
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= move
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += move
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= move
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += move

        self.player.left = max(ROAD_X, self.player.left)
        self.player.right = min(ROAD_X + ROAD_W, self.player.right)
        self.player.top = max(90, self.player.top)
        self.player.bottom = min(HEIGHT - 10, self.player.bottom)

    def update_power(self):
        now = pygame.time.get_ticks()
        if self.active_power == "nitro":
            if now < self.power_end:
                self.speed = self.base_speed + 4
            else:
                self.speed = self.base_speed
                self.active_power = None
        elif self.active_power == "shield":
            self.speed = self.base_speed
        else:
            self.speed = self.base_speed

    def move_objects(self):
        self.road_marks_y = (self.road_marks_y + self.speed) % 80
        self.distance += self.speed * 0.12

        for group in [self.traffic, self.obstacles, self.coins, self.powerups]:
            for obj in group:
                obj["rect"].y += self.speed

        self.traffic = [o for o in self.traffic if o["rect"].y < HEIGHT + 100]
        self.obstacles = [o for o in self.obstacles if o["rect"].y < HEIGHT + 100]
        self.coins = [o for o in self.coins if o["rect"].y < HEIGHT + 100]

        for p in self.powerups:
            p["life"] -= 1
        self.powerups = [p for p in self.powerups if p["life"] > 0 and p["rect"].y < HEIGHT + 100]

    def collision_hit(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            return False
        return True

    def collisions(self):
        for car in self.traffic[:]:
            if self.player.colliderect(car["rect"]):
                if self.collision_hit():
                    self.end_game()
                else:
                    self.traffic.remove(car)

        for obs in self.obstacles[:]:
            if self.player.colliderect(obs["rect"]):
                t = obs["type"]
                if t == "oil":
                    self.player.x += random.choice([-35, 35])
                elif t == "bump":
                    self.speed = max(2, self.speed - 2)
                elif t == "nitrostrip":
                    self.active_power = "nitro"
                    self.power_end = pygame.time.get_ticks() + 3500
                else:
                    if self.collision_hit():
                        self.end_game()
                    else:
                        self.obstacles.remove(obs)
                if obs in self.obstacles and t != "oil":
                    self.obstacles.remove(obs)

        for coin in self.coins[:]:
            if self.player.colliderect(coin["rect"]):
                self.coin_count += coin["value"]
                self.score += coin["value"] * 100
                self.coins.remove(coin)

        for power in self.powerups[:]:
            if self.player.colliderect(power["rect"]):
                ptype = power["type"]
                self.powerups.remove(power)
                if ptype == "nitro" and self.active_power is None:
                    self.active_power = "nitro"
                    self.power_end = pygame.time.get_ticks() + 4000
                    self.score += 50
                elif ptype == "shield" and self.active_power is None:
                    self.active_power = "shield"
                    self.shield = True
                    self.score += 50
                elif ptype == "repair":
                    if self.obstacles:
                        self.obstacles.pop(0)
                    self.score += 150

        if self.distance >= self.finish_distance:
            self.finished = True
            self.end_game()

    def end_game(self):
        self.score += int(self.distance) + self.coin_count * 50
        add_score(self.username, self.score, self.distance, self.coin_count)
        self.game_over = True
        self.running = False

    def draw_road(self):
        self.screen.fill((30, 140, 60))
        pygame.draw.rect(self.screen, (45, 45, 45), (ROAD_X, 0, ROAD_W, HEIGHT))
        pygame.draw.line(self.screen, (240, 240, 240), (ROAD_X, 0), (ROAD_X, HEIGHT), 5)
        pygame.draw.line(self.screen, (240, 240, 240), (ROAD_X + ROAD_W, 0), (ROAD_X + ROAD_W, HEIGHT), 5)
        for i in range(1, LANES):
            x = ROAD_X + i * LANE_W
            for y in range(-80, HEIGHT, 80):
                pygame.draw.rect(self.screen, (245, 245, 245), (x - 4, y + self.road_marks_y, 8, 45))

    def draw_car(self, rect, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10)
        pygame.draw.rect(self.screen, (180, 220, 255), (rect.x + 10, rect.y + 12, rect.w - 20, 22), border_radius=4)
        pygame.draw.circle(self.screen, BLACK, (rect.x + 10, rect.y + 20), 6)
        pygame.draw.circle(self.screen, BLACK, (rect.right - 10, rect.y + 20), 6)
        pygame.draw.circle(self.screen, BLACK, (rect.x + 10, rect.bottom - 20), 6)
        pygame.draw.circle(self.screen, BLACK, (rect.right - 10, rect.bottom - 20), 6)

    def draw_objects(self):
        for car in self.traffic:
            self.draw_car(car["rect"], car["color"])

        for obs in self.obstacles:
            r = obs["rect"]
            t = obs["type"]
            if t == "barrier":
                pygame.draw.rect(self.screen, (230, 100, 20), r)
                pygame.draw.line(self.screen, WHITE, r.topleft, r.bottomright, 4)
            elif t == "oil":
                pygame.draw.ellipse(self.screen, BLACK, r)
            elif t == "pothole":
                pygame.draw.ellipse(self.screen, (70, 40, 25), r)
            elif t == "bump":
                pygame.draw.rect(self.screen, (200, 200, 50), r, border_radius=8)
            elif t == "nitrostrip":
                pygame.draw.rect(self.screen, (0, 220, 255), r, border_radius=8)
                draw_text(self.screen, "N", r.centerx, r.centery - 12, SMALL_FONT, BLACK, True)

        for coin in self.coins:
            r = coin["rect"]
            pygame.draw.circle(self.screen, (255, 215, 0), r.center, 17)
            draw_text(self.screen, str(coin["value"]), r.centerx, r.centery - 12, SMALL_FONT, BLACK, True)

        for power in self.powerups:
            r = power["rect"]
            colors = {"nitro": (0, 200, 255), "shield": (100, 180, 255), "repair": (255, 80, 120)}
            pygame.draw.rect(self.screen, colors[power["type"]], r, border_radius=8)
            draw_text(self.screen, power["type"][0].upper(), r.centerx, r.centery - 12, FONT, BLACK, True)

    def draw_hud(self):
        remaining = max(0, int(self.finish_distance - self.distance))
        draw_text(self.screen, f"Name: {self.username}", 10, 10, SMALL_FONT, WHITE)
        draw_text(self.screen, f"Coins: {self.coin_count}", 10, 35, SMALL_FONT, WHITE)
        draw_text(self.screen, f"Score: {int(self.score + self.distance)}", 10, 60, SMALL_FONT, WHITE)
        draw_text(self.screen, f"Distance: {int(self.distance)} m", 600, 10, SMALL_FONT, WHITE)
        draw_text(self.screen, f"Remaining: {remaining} m", 600, 35, SMALL_FONT, WHITE)
        if self.active_power == "nitro":
            left = max(0, (self.power_end - pygame.time.get_ticks()) // 1000)
            draw_text(self.screen, f"Power: Nitro {left}s", 600, 60, SMALL_FONT, WHITE)
        elif self.active_power == "shield":
            draw_text(self.screen, "Power: Shield", 600, 60, SMALL_FONT, WHITE)
        else:
            draw_text(self.screen, "Power: none", 600, 60, SMALL_FONT, WHITE)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            self.handle_input()
            self.update_power()
            self.spawn_objects()
            self.move_objects()
            self.collisions()

            self.draw_road()
            self.draw_objects()
            self.draw_car(self.player, self.car_color)
            self.draw_hud()
            pygame.display.flip()
            self.clock.tick(60)

        return "game_over"
