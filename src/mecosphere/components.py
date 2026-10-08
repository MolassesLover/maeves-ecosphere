import sys
import random
import time

from mecosphere.simulation import *


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


def system_forage(simobject_instance, component_instance, ecosphere_map):
    if simobject_instance.is_dead:
        return

    position_old_tile = ecosphere_map[simobject_instance.position[0]][
        simobject_instance.position[1]
    ]

    position_old_tile.occupant = simobject_instance

    position_new = simobject_instance.position.copy()

    position_new = [
        position_new[0] + random.randint(-1, 1),
        position_new[1] + random.randint(-1, 1),
    ]

    if position_new[0] > 35 or position_new[0] < 0:
        return
    elif position_new[1] > 63 or position_new[1] < 0:
        return
    else:
        position_new_tile = ecosphere_map[position_new[0]][position_new[1]]

    if not position_new_tile.occupant:
        position_old_tile.occupant = None

        simobject_instance.position = position_new

        position_new_tile.occupant = simobject_instance


def system_eat(simobject_instance, component_instance, ecosphere_map):
    def eat():
        if (
            search_tile.occupant.species
            in simobject_instance.component_data[component_instance["name"]]["diet"]
        ):
            print(f"Eating {search_tile.occupant.name}")
            search_tile.occupant.die()

    for search_tile in simulation_object_yield_tile_neighbour(
        simobject_instance, ecosphere_map
    ):
        if search_tile.occupant:
            if search_tile.occupant == simobject_instance:
                return
            elif search_tile.occupant.species == simobject_instance.species:
                return
            else:
                eat()


component_forage: dict = create_component(
    component_name="Foraging", callback=system_forage
)

component_eat: dict = create_component(
    component_name="Eating",
    callback=system_eat,
)
