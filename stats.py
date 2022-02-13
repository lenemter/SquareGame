import json
import pygame

from common import STATS_TEXT_COLOR

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


def update_stats(added_stats):
    with open("stats.json", "r") as stats_file_reader:
        stats = json.load(stats_file_reader)

    keys = [key for key in added_stats.keys()]

    for index in range(len(keys)):
        stats[keys[index]] += added_stats[keys[index]]

    with open("stats.json", "w") as stats_file_writer:
        json.dump(stats, stats_file_writer)


def render_stats(screen):
    with open("stats.json", "r") as stats_file_reader:
        stats = json.load(stats_file_reader)

    font = pygame.font.SysFont("ComicSans", 28)
    text = font.render("Статистика", True, "#DDDDDD")
    screen.blit(text, ((screen.get_width() - text.get_width()) // 2, 360))

    stats_keys = ["Количество сыгранных игр: ", "Количество смертей: ", "Количество убитых врагов: ",
                  "Количество взятых прокачек: ", "Количество взятого оружия: ",
                  "Количество взятых сердечек: ", "Количество пройденных комнат: ",
                  "Количество пройденных комнат: "]

    stats = [str(value) for value in stats.values()]

    height = 400

    for i in range(len(stats_keys)):
        stats_font = pygame.font.SysFont("ComicSans", 22)
        stat = stats_font.render(stats_keys[i] + stats[i], True, STATS_TEXT_COLOR)
        screen.blit(stat, ((screen.get_width() - stat.get_width()) // 2, height))
        height += 30