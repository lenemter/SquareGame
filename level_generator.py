import random


rooms_count = None
rooms_plan = None
max_rooms_count = None


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

    # Then fill rooms with supposed content
    # Then rooms will create walls and other objects
    # Then they'll be drawn


class Room:
    def __init__(self, x: int, y: int):
        global rooms_count, rooms_plan

        self.name = "<Room name>"
        self.x = x
        self.y = y
        self.children = []

        rooms_count += 1
        rooms_plan[self.x, self.y] = self


def generate_level()