import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 180, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)

        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value

        return settings

    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
