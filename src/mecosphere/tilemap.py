import sys
import random
import time

import pygame


def simulation_object_yield_tile_neighbour(_simobject_instance, _ecosphere_map):
    for x in range(-1, 1):
        for y in range(-1, 1):
            check_position_x = _simobject_instance.position[0] + x
            check_position_y = _simobject_instance.position[1] + y

            # print(f"Checking {check_position_x}, {check_position_y} for food")

            if check_position_x > 63:
                check_position_x = 63
            elif check_position_x < 0:
                check_position_x = 0

            if check_position_x > 35:
                check_position_x = 35
            elif check_position_x < 0:
                check_position_x = 0

            tile = _ecosphere_map[check_position_x][check_position_y]

            yield tile, check_position_x, check_position_y


def ecosphere_map_yield_tile(ecosphere_map, width: int = 64, height: int = 36):
    position_x = 0
    position_y = 0

    for collumn in range(height):
        for row in range(width):
            yield ecosphere_map[collumn][row], position_x, position_y

            position_y += 1

        position_y = 0
        position_x += 1


def ecosphere_map_generate(width: int = 64, height: int = 36) -> list:
    print("Generating map...")
    new_map = []
    position_x = 0
    position_y = 0

    for collumn in range(height):
        new_collumn = []

        for row in range(width):
            place_vegetation = bool(random.getrandbits(1))

            if place_vegetation:
                new_collumn.append(random.randint(1, 3))
            else:
                new_collumn.append(0)

                position_y += 1

        new_map.append(new_collumn)

        position_x += 1

    return new_map
