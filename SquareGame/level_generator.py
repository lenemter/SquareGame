import random

import globals
from common import ROOM_SIZE

from camera import Camera
from player import Player
from wall import Wall
from heart import Heart
from hud import HUD1
from weapon import Weapon, weapons
from stats import update_stats

rooms_count = None
rooms_plan = None
max_rooms_count = None


class Level(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = Camera()
        self.player = None

    def create_objects(self):
        self[0, 0].create_objects(self)

    def event_handler(self, time):
        for bullet in globals.player_bullet_group:
            bullet.event_handler(time)
        self.player.event_handler(time)

    def draw(self, surface):
        self.camera.update(self.player)
        self.camera.draw(surface)


def create_more_rooms(room):
    room_x = room.x
    room_y = room.y

    supposed_rooms_count = random.randint(0, 3)
    if (
        (room_x - 1, room_y) not in rooms_plan
        and supposed_rooms_count > 0
        and rooms_count < max_rooms_count
    ):
        new_room = Room(room_x - 1, room_y)
        room.children.append(new_room)
        supposed_rooms_count -= 1
    if (
        (room_x + 1, room_y) not in rooms_plan
        and supposed_rooms_count > 0
        and rooms_count < max_rooms_count
    ):
        new_room = Room(room_x + 1, room_y)
        room.children.append(new_room)
        supposed_rooms_count -= 1
    if (
        (room_x, room_y - 1) not in rooms_plan
        and supposed_rooms_count > 0
        and rooms_count < max_rooms_count
    ):
        new_room = Room(room_x, room_y - 1)
        room.children.append(new_room)
        supposed_rooms_count -= 1
    if (
        (room_x, room_y + 1) not in rooms_plan
        and supposed_rooms_count > 0
        and rooms_count < max_rooms_count
    ):
        new_room = Room(room_x, room_y + 1)
        room.children.append(new_room)
        supposed_rooms_count -= 1

    for room_child in room.children:
        create_more_rooms(room_child)


def generate_level_layout(min_rooms=5, max_rooms=12):
    global rooms_count
    global rooms_plan
    global max_rooms_count

    rooms_count = 1
    rooms_plan = {}
    max_rooms_count = max_rooms

    root = Room(0, 0)
    create_more_rooms(root)

    if rooms_count < min_rooms:
        return generate_level_layout(min_rooms)
    return rooms_plan

    # Then rooms will create walls and other objects
    # Then they'll be drawn


class Corridor:
    def __init__(self, start_room, end_room):
        self.start_room = start_room
        self.end_room = end_room

    def create_objects(self):
        pass


class Room:
    def __init__(self, x: int, y: int):
        global rooms_count, rooms_plan

        self.name = "<Room name>"
        self.x = x
        self.y = y
        self.children = []

        rooms_count += 1
        rooms_plan[self.x, self.y] = self

    def create_objects(self, level):
        name = self.name

        if name == "The begining":
            level.player = Player(self.x * ROOM_SIZE // 2, self.y * ROOM_SIZE // 2)
        elif name == "Portal":
            pass


def generate_level():
    level = Level(generate_level_layout())
    level[0, 0].name = "The begining"
    for room in set(level.values()) - {level[0, 0]}:
        room.name = random.choice(
            (
                "Regular room",
                "Regular room",
                "Regular room",
                "Regular room",
                "Buff room",
            )
        )

    random.choice(tuple(set(level.values()) - {level[0, 0]})).name = "Portal"

    level.create_objects()
    return level
