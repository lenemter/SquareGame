import json

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
