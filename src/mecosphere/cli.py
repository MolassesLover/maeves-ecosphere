#!/usr/local/bin/env python3

"""
A simple ecosphere simulator I made while bored and sick.
This project uses the terms 'entity' and 'component,' however,
please note that this is not an ECS.
"""

import sys
import random
import csv

import pygame


def generate_ecosphere_map(width: int = 64, height: int = 36) -> list:
    print("Generating map...")
    new_map = []

    for collumn in range(height):
        new_collumn = []

        for row in range(width):
            place_tile = bool(random.getrandbits(1))

            if place_tile:
                new_collumn.append("1")
            else:
                new_collumn.append("0")

        new_map.append(new_collumn)

    with open("map-initial.csv", "w", newline="") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(new_map)

    return new_map


def create_component(component_name, callback: callable, is_active=True) -> dict:
    """
    A simple constructor for components as dictionaries. This is not an ECS,
    just borrowing the language.
    """

    component_dictionary = {
        "name": component_name,
        "active": is_active,
        "callback": callback,
    }

    return component_dictionary


class EcosphereApplication:
    def __init__(self):
        self.should_run = True
        self.should_simulate = True

        pygame.init()

        self.pygame_display = pygame.display.set_mode((1024, 576))
        
        self.tile_tree = pygame.image.load("res/img/tree.png").convert()

        self.ecosphere = Ecosphere()

    def tiles_render(self):
        col_index = 0
        row_index = 0

        for collumn in self.ecosphere.map:
            for row in collumn:
                if self.ecosphere.map[col_index][row_index] == "1":
                    self.pygame_display.blit(self.tile_tree, (row_index*16, col_index*16))

                row_index += 1

            row_index = 0
            col_index += 1

    def run(self):
        while self.should_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_run = False

            if self.should_simulate:
                if self.ecosphere.update() == 1:
                    self.should_simulate = False
                
                self.tiles_render()

                pygame.display.flip()

        pygame.quit()


class Organism:
    """
    Abstracts all fauna, flora, and bacteria.
    """

    def __init__(self, name, domain, components: list, age_maximum=7):
        self.age_current = 0
        self.age_maximum = age_maximum
        self.components: list = components
        self.name = name
        self.domain = domain

    def die(self):
        print(f"{self.name} is now a corpse.")


class Ecosphere:
    """
    The entire system containing natural resources, entities and viruses.
    """

    def __init__(self):
        self.entities = []  # Set on every update call.
        self.fauna: list = []
        self.flora: list = []
        self.bacteria: list = []
        self.viruses: list = []
        self.time = 0.0
        self.map = generate_ecosphere_map()

    def update(self) -> int:
        self.entities = self.fauna + self.flora + self.bacteria + self.viruses

        if self.entities:
            for entity in self.entities.copy():
                entity.age_current += 1

                if entity.age_current > entity.age_maximum:
                    # Kill the entity
                    print(f"Organism {entity.name} died.")

                    entity.die()

                    match entity.domain:
                        case "fauna":
                            self.fauna.remove(entity)
                else:
                    for component in entity.components:
                        component["callback"]()
        else:
            print("No more entities, ending simulation.")
            return 1

        return 0


def main():
    """
    The entrypoint for the script.
    """

    def forage():
        print("Foraging")

    component_forage: dict = create_component(
        component_name="Foraging", callback=forage
    )

    application = EcosphereApplication()

    isopod = Organism(
        components=[component_forage], domain="fauna", age_maximum=913, name="isopod"
    )

    # Propogation
    print("Propogating ecosphere...")

    application.ecosphere.fauna.append(isopod)

    try:
        application.run()
    except KeyboardInterrupt:
        application.should_run = False


if __name__ == "__main__":
    main()
