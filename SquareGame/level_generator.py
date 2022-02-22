import random
import pygame

import globals
from common import ROOM_SIZE

from camera import Camera
from enemy import Enemy
from floor_piece import FloorPiece
from heart import Heart
from player import Player
from portal import Portal
from wall import Wall
from weapon import Weapon, weapons

rooms_count = None
rooms_plan = None
max_rooms_count = None


class Level(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = Camera()

    def create_objects(self):
        self[0, 0].create_objects(self)

    def event_handler(self, time):
        for bullet in globals.player_bullet_group:
            bullet.event_handler(time)
        for bullet in globals.enemy_bullet_group:
            bullet.event_handler(time)
        for enemy in globals.enemy_group:
            enemy.event_handler(time)
        globals.game.player.event_handler(time)

        for room in self.values():
            room.event_handler()

    def draw(self, surface):
        self.camera.update(globals.game.player)
        self.camera.draw(surface)

    def remove_all_objects(self):
        for room in self.values():
            room.remove_all_objects()


class Room:
    def __init__(self, x: int, y: int):
        global rooms_count
        global rooms_plan

        self.name = "<Room name>"
        self.children = []
        self.x = x
        self.y = y
        self.enemies_group = pygame.sprite.Group()

        rooms_count += 1
        rooms_plan[self.x, self.y] = self

    def remove_all_objects(self):
        for obj in globals.walls_group:
            obj.kill()
        globals.created_walls_cords.clear()

        for obj in globals.floor_pieces:
            obj.kill()

        for obj in globals.hearts_group:
            obj.kill()

        for obj in globals.weapon_group:
            obj.kill()

        for obj in globals.portal_group:
            obj.kill()

        for obj in globals.player_bullet_group:
            obj.kill()

        for obj in globals.enemy_group:
            obj.kill()

        for obj in globals.enemy_bullet_group:
            obj.kill()

    def create_objects(self, level):
        name = self.name

        room_center = (
            self.x * ROOM_SIZE + ROOM_SIZE / 2 - self.x,
            self.y * ROOM_SIZE + ROOM_SIZE / 2 - self.y,
        )

        # Create floor
        FloorPiece(
            self.x * ROOM_SIZE - self.x,
            self.y * ROOM_SIZE - self.y,
            ROOM_SIZE,
            ROOM_SIZE,
        )

        if name == "The beginning":
            # 0.3 - half of the player's size
            if globals.game.player is None:
                globals.game.player = Player(room_center[0] - 0.3, room_center[1] - 0.3)
            else:
                globals.game.player.x = room_center[0] - 0.3
                globals.game.player.y = room_center[1] - 0.3
        elif name == "Portal":
            # 0.5 and 1 are half of the portal's width and height
            Portal(room_center[0] - 0.5, room_center[1] - 1)
        elif name == "Regular room":
            for _ in range(random.randint(5, 8)):
                # -0.6 - Enemies' size
                enemy_x = random.uniform(
                    self.x * ROOM_SIZE - self.x + 1,
                    self.x * ROOM_SIZE + ROOM_SIZE - self.x - 1 - 0.6,
                )
                enemy_y = random.uniform(
                    self.y * ROOM_SIZE - self.y + 1,
                    self.y * ROOM_SIZE + ROOM_SIZE - self.y - 1 - 0.6,
                )
                self.enemies_group.add(Enemy(enemy_x, enemy_y))
        elif name == "Buff room":
            choice = random.choice(("Heart", "Weapon"))
            if choice == "Heart":
                Heart(room_center[0] - 0.5, room_center[1] - 0.5)
            elif choice == "Weapon":
                weapon = random.choice(weapons)
                Weapon(room_center[0] - 0.5, room_center[1] - 0.5, weapon)

        # Create walls
        room_x = self.x * ROOM_SIZE
        room_y = self.y * ROOM_SIZE
        for x in range(ROOM_SIZE):
            Wall(room_x - self.x + x, room_y - self.y)
            Wall(room_x - self.x + x, room_y - self.y + ROOM_SIZE - 1)
        for y in range(ROOM_SIZE):
            Wall(room_x - self.x, room_y - self.y + y)
            Wall(room_x - self.x + ROOM_SIZE - 1, room_y - self.y + y)

        walls_for_removal = set()
        for child in self.children:
            child.create_objects(level)
            if child.x == self.x - 1:
                for i in range((ROOM_SIZE - 2) // 3):
                    walls_for_removal.add(
                        (
                            self.x * ROOM_SIZE - self.x,
                            (self.y * ROOM_SIZE)
                            + (ROOM_SIZE - 2) // 3
                            + i
                            - self.y
                            + 1,
                        )
                    )
            elif child.x == self.x + 1:
                for i in range((ROOM_SIZE - 2) // 3):
                    walls_for_removal.add(
                        (
                            self.x * ROOM_SIZE + ROOM_SIZE - self.x - 1,
                            (self.y * ROOM_SIZE)
                            + (ROOM_SIZE - 2) // 3
                            + i
                            - self.y
                            + 1,
                        )
                    )
            elif child.y == self.y - 1:
                for i in range((ROOM_SIZE - 2) // 3):
                    walls_for_removal.add(
                        (
                            (self.x * ROOM_SIZE)
                            + (ROOM_SIZE - 2) // 3
                            + i
                            - self.x
                            + 1,
                            self.y * ROOM_SIZE - self.y,
                        )
                    )
            elif child.y == self.y + 1:
                for i in range((ROOM_SIZE - 2) // 3):
                    walls_for_removal.add(
                        (
                            (self.x * ROOM_SIZE)
                            + (ROOM_SIZE - 2) // 3
                            + i
                            - self.x
                            + 1,
                            self.y * ROOM_SIZE + ROOM_SIZE - self.y - 1,
                        )
                    )

        for wall in globals.walls_group:
            if (wall.x, wall.y) in walls_for_removal:
                wall.kill()

    def event_handler(self):
        player = globals.game.player
        if (  # If player in a room and it eneters it from another room
            self.x * ROOM_SIZE - self.x + 1
            < player.x
            < self.x * ROOM_SIZE + ROOM_SIZE - self.x - 1
            and self.y * ROOM_SIZE - self.y + 1
            < player.y
            < self.y * ROOM_SIZE + ROOM_SIZE - self.y - 1
            and player.last_room != (self.x, self.y)
        ):
            player.last_room = (self.x, self.y)
            globals.game.rooms += 1
            for enemy in self.enemies_group:
                enemy.is_active = True


def create_more_rooms(room):
    room_x = room.x
    room_y = room.y

    supposed_rooms_count = random.randint(0, 3)

    def left():
        nonlocal supposed_rooms_count
        if (
            (room_x - 1, room_y) not in rooms_plan
            and supposed_rooms_count > 0
            and rooms_count < max_rooms_count
        ):
            new_room = Room(room_x - 1, room_y)
            room.children.append(new_room)
            supposed_rooms_count -= 1

    def right():
        nonlocal supposed_rooms_count
        if (
            (room_x + 1, room_y) not in rooms_plan
            and supposed_rooms_count > 0
            and rooms_count < max_rooms_count
        ):
            new_room = Room(room_x + 1, room_y)
            room.children.append(new_room)
            supposed_rooms_count -= 1

    def top():
        nonlocal supposed_rooms_count
        if (
            (room_x, room_y - 1) not in rooms_plan
            and supposed_rooms_count > 0
            and rooms_count < max_rooms_count
        ):
            new_room = Room(room_x, room_y - 1)
            room.children.append(new_room)
            supposed_rooms_count -= 1

    def bottom():
        nonlocal supposed_rooms_count
        if (
            (room_x, room_y + 1) not in rooms_plan
            and supposed_rooms_count > 0
            and rooms_count < max_rooms_count
        ):
            new_room = Room(room_x, room_y + 1)
            room.children.append(new_room)
            supposed_rooms_count -= 1

    functions = [left, right, top, bottom]
    random.shuffle(functions)
    for function in functions:
        function()

    for room_child in room.children:
        create_more_rooms(room_child)


def generate_level_layout(min_rooms=6, max_rooms=10):
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


def generate_level():
    level = Level(generate_level_layout())
    level[0, 0].name = "The beginning"
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
