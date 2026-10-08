#!/usr/local/bin/env python3

"""
A simple ecosphere simulator I made while bored and sick.
This project uses the terms 'simulation_object' and 'component,' however,
please note that this is not an ECS.
"""

import sys
import random
import csv
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
            place_tree = bool(random.getrandbits(1))

            if place_tree:
                new_collumn.append(1)
            else:
                new_collumn.append(0)

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

                self.pygame_display.blit(
                    self.tile_dirt, (row_index * 16, col_index * 16)
                )

                if tile.occupant:
                    self.pygame_display.blit(
                        tile.occupant.image, (row_index * 16, col_index * 16)
                    )

                row_index += 1

            row_index = 0
            col_index += 1

    def run(self):
        print("Running core loop...")

        while self.should_run:
            self.pygame_display.fill((0, 0, 0))

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

            # print(self.ecosphere.map)

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

        propogated_map = self.ecosphere.map.copy()

        for tile, col_index, row_index in ecosphere_map_yield_tile(
            self.ecosphere.map, 64, 36
        ):
            tile = propogated_map[col_index][row_index]

            match tile:
                case 1:
                    new_tree = SimulationObject(
                        components=[],
                        domain="flora",
                        age_maximum=random.randint(1825, 3650),
                        name=f"tree",
                        species="tree",
                    )

                    propogated_map[col_index][row_index] = Tile(
                        occupant=new_tree,
                        nutritious=False,
                        contaminated=False,
                        pos_x=col_index,
                        pos_y=row_index,
                    )

                    self.ecosphere.simulation_objects.append(new_tree)
                case _:
                    propogated_map[col_index][row_index] = Tile(
                        occupant=None,
                        nutritious=False,
                        contaminated=False,
                        pos_x=col_index,
                        pos_y=row_index,
                    )

            row_index += 1

        row_index = 0
        col_index += 1

        # print(propogated_map)

        self.ecosphere.map = propogated_map

        for i in range(100):
            isopod = SimulationObject(
                components=[],
                domain="fauna",
                age_maximum=random.randint(913, 1825),
                name=f"isopod {i}",
                species="isopod",
            )

            isopod.components.append(component_forage)

            self.ecosphere.simulation_objects.append(isopod)
            self.ecosphere.map[isopod.position[0]][isopod.position[1]].occupant = isopod


class Tile(object):
    __slots__ = ("occupant", "metadata", "pos_x", "pos_y")

    def __init__(self, occupant, nutritious, contaminated, pos_x, pos_y):
        self.occupant: SimulationObject = occupant
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.metadata = self.metadata_create(nutritious, contaminated)

    def metadata_create(self, nutritious=False, contaminated=False) -> dict:
        metadata_dictionary = {"nutritious": nutritious, "contaminated": contaminated}

        return metadata_dictionary


class SimulationObject:
    def __init__(self, name, species, domain, components: list, age_maximum=7):
        self.age_current = 0
        self.age_maximum = age_maximum
        self.decomposition_current = 0
        self.decomposition_maximum = int(round(age_maximum / 2))
        self.components: list = components
        self.name = name
        self.species = species
        self.position = [random.randint(1, 35), random.randint(1, 63)]
        self.domain = domain
        self.is_dead = False

        self.image_default = pygame.image.load(f"res/img/{species}.png")
        self.image_dead = pygame.image.load(f"res/img/{species}-dead.png")
        self.image = self.image_default

    def die(self):
        print(f"{self.name} is now dead.")
        self.image = self.image_dead
        self.is_dead = True


class Ecosphere:
    def __init__(self):
        self.simulation_objects = []  # Set on every update call, do not change manually.
        self.fauna: list = []
        self.flora: list = []
        self.bacteria: list = []
        self.viruses: list = []
        self.time = 0.0
        self.map = ecosphere_map_generate()

    def update(self) -> int:
        if self.simulation_objects:
            # Old list may contain out of bounds entitities
            # We set self.simulation_objects to this new list in order to remove them
            new_entities_list = []

            for tile, col_index, row_index in ecosphere_map_yield_tile(
                self.map, 64, 36
            ):
                simulation_object = tile.occupant

                if simulation_object:
                    new_entities_list.append(simulation_object)

                    if simulation_object.age_current > simulation_object.age_maximum:
                        if not simulation_object.is_dead:
                            print(f"{simulation_object.name} died.")

                            simulation_object.die()  # Messed up, man. :C
                        elif (
                            simulation_object.decomposition_current >= simulation_object.decomposition_maximum
                        ):
                            print(f"{simulation_object.name} decomposed.")

                            self.map[col_index][row_index].occupant = None

                            self.simulation_objects.remove(simulation_object)

                            del simulation_object
                        else:
                            simulation_object.decomposition_current += 1
                    else:
                        simulation_object.age_current += 1

                        if simulation_object.components:
                            for component in simulation_object.components:
                                component["callback"](simulation_object)

            self.simulation_objects = new_entities_list
        else:
            print("No more simulation objects, ending simulation.")

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
