import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}

CAR_COLORS = {
    "blue": (40, 120, 255),
    "red": (230, 50, 50),
    "green": (40, 180, 90),
    "yellow": (240, 210, 40)
}

DIFFICULTIES = {
    "easy": {"speed": 4, "spawn_rate": 70, "finish_distance": 2500},
    "normal": {"speed": 6, "spawn_rate": 55, "finish_distance": 3500},
    "hard": {"speed": 8, "spawn_rate": 40, "finish_distance": 4500}
}


def load_json(filename, default):
    if not os.path.exists(filename):
        save_json(filename, default)
        return default.copy() if isinstance(default, dict) else list(default)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default.copy() if isinstance(default, dict) else list(default)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_settings():
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)
    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])
    if not isinstance(data, list):
        return []
    return data


def add_score(name, score, distance, coins):
    leaderboard = load_leaderboard()
    leaderboard.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })
    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]
    save_json(LEADERBOARD_FILE, leaderboard)
    return leaderboard
