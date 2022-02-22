import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import json
import logging
import pygame

from common import STATS_COLOR, FONT_ANTIALIAS, STATS_FILE_PATH

"""
games = Количество сыгранных игр
deaths = Количество смертей
kills = Количество убитых врагов
upgrades = Количество взятых прокачек
weapons = Количество взятого оружия
hearts = Количество взятых сердечек
rooms = Количество пройденных комнат
levels = Количество пройденных уровней
"""

title_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20)
stats_font = pygame.font.Font("fonts/Press_Start_2P/PressStart2P-Regular.ttf", 16)


def update_stats(added_stats):
    existence = os.path.exists(STATS_FILE_PATH)

    if not existence:
        defult_stats = {
            "games": 0,
            "deaths": 0,
            "kills": 0,
            "upgrades": 0,
            "weapons": 0,
            "hearts": 0,
            "rooms": 0,
            "levels": 0,
        }

        with open(STATS_FILE_PATH, mode="w", encoding="UTF-8") as stats_file_writer:
            json.dump(defult_stats, stats_file_writer)

    with open(STATS_FILE_PATH, mode="r", encoding="UTF-8") as stats_file_reader:
        try:
            stats = json.load(stats_file_reader)
        except json.JSONDecodeError:
            stats = {
                "games": 0,
                "deaths": 0,
                "kills": 0,
                "upgrades": 0,
                "weapons": 0,
                "hearts": 0,
                "rooms": 0,
                "levels": 0,
            }
        logging.error(f"Unable to load stats from {STATS_FILE_PATH}")

    for key in added_stats:
        stats[key] += added_stats[key]

    with open(STATS_FILE_PATH, mode="w", encoding="UTF-8") as stats_file_writer:
        json.dump(stats, stats_file_writer)


def render_stats(surface):
    existence = os.path.exists(STATS_FILE_PATH)

    if not existence:
        default_stats = {
            "games": 0,
            "deaths": 0,
            "kills": 0,
            "upgrades": 0,
            "weapons": 0,
            "hearts": 0,
            "rooms": 0,
            "levels": 0,
        }
        with open(STATS_FILE_PATH, mode="w", encoding="UTF-8") as stats_file_writer:
            json.dump(default_stats, stats_file_writer)

    with open(STATS_FILE_PATH, mode="r", encoding="UTF-8") as stats_file_reader:
        try:
            stats = json.load(stats_file_reader)
        except json.JSONDecodeError:
            stats = {
                "games": 0,
                "deaths": 0,
                "kills": 0,
                "upgrades": 0,
                "weapons": 0,
                "hearts": 0,
                "rooms": 0,
                "levels": 0,
            }
        logging.error(f"Unable to load stats from {STATS_FILE_PATH}")

    text = title_font.render("Статистика", FONT_ANTIALIAS, STATS_COLOR)
    surface.blit(text, ((surface.get_width() - text.get_width()) // 2, 360))

    stats_keys = [
        "Количество сыгранных игр: ",
        "Количество смертей: ",
        "Количество убитых врагов: ",
        "Количество взятых прокачек: ",
        "Количество взятого оружия: ",
        "Количество взятых сердечек: ",
        "Количество пройденных комнат: ",
        "Количество пройденных уровней: ",
    ]

    stats = [str(value) for value in stats.values()]

    height = 400

    for i in range(len(stats_keys)):
        stat = stats_font.render(stats_keys[i] + stats[i], FONT_ANTIALIAS, STATS_COLOR)
        surface.blit(stat, ((surface.get_width() - stat.get_width()) // 2, height))
        height += 30
