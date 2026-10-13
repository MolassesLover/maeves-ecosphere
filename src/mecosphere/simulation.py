import sys
import random
import time

import pygame

from mecosphere.tilemap import *


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
    def __init__(
        self,
        name,
        species,
        domain,
        position_range_width,
        position_range_height,
        components: list,
        age_maximum=7,
        component_data={},
        images={},
        position=[],
    ):
        self.age_current = 0
        self.age_maximum = age_maximum
        self.decomposition_current = 0
        self.decomposition_maximum = int(round(age_maximum / 8))
        self.components: list = components
        self.images = images
        self.name = name
        self.species = species
        self.position_range_width = position_range_width
        self.position_range_height = position_range_height

        if not position:
            self.position = [
                random.randint(1, self.position_range_height - 1),
                random.randint(1, self.position_range_width - 1),
            ]
        else:
            self.position = position

        self.domain = domain
        self.is_dead = False

        self.image_default = pygame.image.load(f"res/img/{species}.bmp")
        self.image_egg = pygame.image.load(f"res/img/egg.bmp")
        self.image_dead = pygame.image.load(f"res/img/{species}-dead.bmp")
        self.image_baby = self.image_default

        if "image_baby" in images:
            self.image_baby = pygame.image.load(f"res/img/{images['image_baby']}.bmp")
        elif "image_egg" in images:
            self.image_egg = pygame.image.load(f"res/img/{images['image_egg']}.bmp")

        self.image = self.image_default

        # `self.component_data`` is a dict of component names matched to any other child dict
        # Example:
        # { "Eating": { "diet": [ "grass", "mushroom" ] }, }

        self.component_data = component_data

    def die(self):
        # print(f"{self.name} is now dead.")
        self.image = self.image_dead
        self.is_dead = True


class Ecosphere:
    def __init__(self, _application_settings):
        self.simulation_objects = (
            []
        )  # Set on every update call, do not change manually.
        self.fauna: list = []
        self.flora: list = []
        self.bacteria: list = []
        self.viruses: list = []
        self.time = 0.0
        self.application_settings = _application_settings
        self.map = ecosphere_map_generate(self.application_settings)

    def update(self) -> int:
        if self.simulation_objects:
            # Old list may contain out of bounds entitities
            # We set self.simulation_objects to this new list in order to remove them
            new_entities_list = []
            living_entities_count = 0

            for tile, col_index, row_index in ecosphere_map_yield_tile(
                self.map,
                width=self.application_settings.width,
                height=self.application_settings.height,
            ):
                simulation_object = tile.occupant

                if simulation_object:
                    new_entities_list.append(simulation_object)

                    if simulation_object.age_current > simulation_object.age_maximum:
                        if not simulation_object.is_dead:
                            # print(f"{simulation_object.name} died.")

                            simulation_object.die()  # Messed up, man. :C
                        elif (
                            simulation_object.decomposition_current
                            >= simulation_object.decomposition_maximum
                        ):
                            # print(f"{simulation_object.name} decomposed.")

                            if simulation_object.species == "fauna":
                                self.map[col_index][row_index].contaminated = True

                            self.map[col_index][row_index].occupant = None

                            self.simulation_objects.remove(simulation_object)

                            del simulation_object
                        else:
                            simulation_object.decomposition_current += 1
                    else:
                        living_entities_count += 1
                        simulation_object.age_current += 1

                        if (
                            simulation_object.components
                            and not simulation_object.is_dead
                        ):
                            for component in simulation_object.components:
                                print(
                                    f"Running callback for entity {living_entities_count}"
                                )

                                component["callback"](
                                    simulation_object,
                                    component,
                                    self.map,
                                    self.application_settings,
                                )

            self.simulation_objects = new_entities_list
        else:
            print("No more simulation objects, ending simulation.")

            return 1

        return 0
