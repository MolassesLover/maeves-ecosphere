#!/usr/local/bin/env python3

"""
A simple ecosphere simulator I made while bored and sick.
This project uses the terms 'entity' and 'component,' however,
please note that this is not an ECS.
"""

import sys
import random
import csv
import time

import pygame


def generate_ecosphere_map(width: int = 64, height: int = 36) -> list:
    print("Generating map...")
    new_map = []
    position_x = 0
    position_y = 0

    for collumn in range(height):
        new_collumn = []

        for row in range(width):
            place_tree = bool(random.getrandbits(1))

            if place_tree:
                organism_tree = Organism("tree", "tree", "flora", None, 999)
                tile_tree_instance = Tile(
                    occupant=organism_tree,
                    nutritious=True,
                    contaminated=False,
                    pos_x=position_x,
                    pos_y=position_y,
                )

                new_collumn.append(tile_tree_instance)
            else:
                tile_instance = Tile(
                    occupant=None,
                    nutritious=False,
                    contaminated=False,
                    pos_x=position_x,
                    pos_y=position_y,
                )

                new_collumn.append(tile_instance)

            position_y += 1

        new_map.append(new_collumn)

        position_x += 1

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

        self.tile_dirt = pygame.image.load("res/img/dirt.png").convert()

        self.ecosphere = Ecosphere()

        self.initialize()

    def tiles_render(self):
        col_index = 0
        row_index = 0

        for collumn in self.ecosphere.map:
            for row in collumn:
                tile = self.ecosphere.map[col_index][row_index]

                if tile.occupant:
                    self.pygame_display.blit(
                        tile.occupant.image, (row_index * 16, col_index * 16)
                    )
                else:
                    self.pygame_display.blit(
                        self.tile_dirt, (row_index * 16, col_index * 16)
                    )

                row_index += 1

            row_index = 0
            col_index += 1

    def run(self):
        print("Running core loop...")

        while self.should_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.should_run = False

            if self.should_simulate:
                if self.ecosphere.update() == 1:
                    self.should_simulate = False

                self.tiles_render()

                pygame.display.flip()

            time.sleep(0.01666)

        pygame.quit()

    def initialize(self):
        def forage(entity_instance):
            # print("Foraging")

            position_old_tile = self.ecosphere.map[entity_instance.position[0]][
                entity_instance.position[1]
            ]

            position_old_tile.occupant = entity_instance

            position_new = entity_instance.position.copy()

            # print(f"Current position is {position_new}")

            position_new = [
                position_new[0] + random.randint(-1, 1),
                position_new[1] + random.randint(-1, 1),
            ]

            if position_new[0] > 35 or position_new[0] < 0:
                return
            elif position_new[1] > 63 or position_new[1] < 0:
                return
            else:
                position_new_tile = self.ecosphere.map[position_new[0]][position_new[1]]

            if not position_new_tile.occupant:
                position_old_tile.occupant = None

                entity_instance.position = position_new

                position_new_tile.occupant = entity_instance

        component_forage: dict = create_component(
            component_name="Foraging", callback=forage
        )

        # Propogation
        print("Propogating ecosphere...")

        for i in range(100):
            isopod = Organism(
                components=[],
                domain="fauna",
                age_maximum=random.randint(913, 1825),
                name=f"isopod {i}",
                species="isopod",
            )
            isopod.components.append(component_forage)
            self.ecosphere.fauna.append(isopod)


class Tile(object):
    __slots__ = ("occupant", "metadata", "pos_x", "pos_y")

    def __init__(self, occupant, nutritious, contaminated, pos_x, pos_y):
        self.occupant: Organism = occupant
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.metadata = self.metadata_create(nutritious, contaminated)

    def metadata_create(self, nutritious=False, contaminated=False) -> dict:
        metadata_dictionary = {"nutritious": nutritious, "contaminated": contaminated}

        return metadata_dictionary


class Organism:
    def __init__(self, name, species, domain, components: list, age_maximum=7):
        self.age_current = 0
        self.age_maximum = age_maximum
        self.components: list = components
        self.name = name
        self.species = species
        self.position = [random.randint(1, 35), random.randint(1, 63)]
        self.domain = domain
        self.image = pygame.image.load(f"res/img/{species}.png")
        # self.image_dead = pygame.image.load(f"res/img/{name}-dead.png")

    def die(self):
        print(f"{self.name} is now dead.")


class Ecosphere:
    def __init__(self):
        self.entities = []  # Set on every update call, do not change manually.
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

                    entity.die() # Messed up, man. :C

                    self.map[entity.position[0]][entity.position[1]].occupant = None
                    
                    self.fauna.remove(entity)

                    del entity
                else:
                    for component in entity.components:
                        component["callback"](entity)
        else:
            print("No more entities, ending simulation.")

            return 1

        return 0


def main():
    """
    The entrypoint for the script.
    """

    application = EcosphereApplication()

    try:
        application.run()
    except KeyboardInterrupt:
        application.should_run = False


if __name__ == "__main__":
    main()
