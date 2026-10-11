import sys
import random
import time

import pygame


def simulation_object_yield_tile_neighbour(_simobject_instance, _ecosphere_map):
    directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]  # Left  # Right  # Up  # Down

    for direction in directions:
        check_position_x = _simobject_instance.position[0] + direction[0]
        check_position_y = _simobject_instance.position[1] + direction[1]

        print(f"Checking {check_position_x}, {check_position_y} for food")

        if check_position_y > 127:
            check_position_y = 127
        elif check_position_y < 0:
            check_position_y = 0

        if check_position_x > 71:
            check_position_x = 71
        elif check_position_x < 0:
            check_position_x = 0

        tile = _ecosphere_map[check_position_x][check_position_y]

        yield tile, check_position_x, check_position_y


def ecosphere_map_yield_tile(ecosphere_map, width: int = 128, height: int = 72):
    position_x = 0
    position_y = 0

    for collumn in range(height):
        for row in range(width):
            yield ecosphere_map[collumn][row], position_x, position_y

            position_y += 1

        position_y = 0
        position_x += 1


def ecosphere_map_generate(width: int = 128, height: int = 72) -> list:
    print("Generating map...")
    new_map = []
    position_x = 0
    position_y = 0

    for collumn in range(height):
        new_collumn = []

        for row in range(width):
            place_vegetation = bool(random.getrandbits(1))

            if place_vegetation:
                new_collumn.append(random.randint(1, 5))
            else:
                new_collumn.append(0)

            position_y += 1

        new_map.append(new_collumn)

        position_x += 1

    return new_map
