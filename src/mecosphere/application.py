import sys
import random
import time

import pygame

from mecosphere import components
from mecosphere.simulation import *
from mecosphere.tilemap import *


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
                        name="tree",
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
                case 2:
                    new_tree = SimulationObject(
                        components=[],
                        domain="flora",
                        age_maximum=random.randint(120, 270),
                        name="grass",
                        species="grass",
                    )

                    propogated_map[col_index][row_index] = Tile(
                        occupant=new_tree,
                        nutritious=False,
                        contaminated=False,
                        pos_x=col_index,
                        pos_y=row_index,
                    )

                    self.ecosphere.simulation_objects.append(new_tree)
                case 3:
                    new_tree = SimulationObject(
                        components=[],
                        domain="fungus",
                        age_maximum=random.randint(60, 240),
                        name=f"mushroom",
                        species="mushroom",
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

        self.ecosphere.map = propogated_map

        for i in range(100):
            isopod = SimulationObject(
                components=[],
                domain="fauna",
                age_maximum=random.randint(913, 1825),
                name=f"isopod {i}",
                species="isopod",
                component_data={
                    "Eating": {
                        "diet": ["grass", "mushroom"],
                        "hunger": 0,
                        "hunger_max": 30,
                    },
                },
            )

            isopod.components.append(components.component_forage)
            isopod.components.append(components.component_eat)
            isopod.components.append(components.component_reproduce_sexual_direct)

            self.ecosphere.simulation_objects.append(isopod)
            self.ecosphere.map[isopod.position[0]][isopod.position[1]].occupant = isopod
