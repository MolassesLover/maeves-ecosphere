import sys
import random
import time

import pygame

from mecosphere.tilemap import *


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
        self.simulation_objects = (
            []
        )  # Set on every update call, do not change manually.
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
                            simulation_object.decomposition_current
                            >= simulation_object.decomposition_maximum
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
