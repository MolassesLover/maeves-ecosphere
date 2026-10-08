import sys
import random
import time

import pygame


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
