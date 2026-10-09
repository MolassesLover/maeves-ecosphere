import sys
import random
import time
import copy

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


def system_age(simobject_instance, component_instance, ecosphere_map):
    if simobject_instance.is_dead:
        return

    age_current = simobject_instance.age_current
    age_baby = simobject_instance.component_data["Aging"]["age_baby"]
    age_adult = simobject_instance.component_data["Aging"]["age_adult"]

    if age_current < age_baby:
        simobject_instance.image = simobject_instance.image_egg
        simobject_instance.component_data["Aging"]["is_egg"] = True
        simobject_instance.component_data["Aging"]["is_baby"] = False
    elif age_current > age_adult:
        simobject_instance.image = simobject_instance.image_default
        simobject_instance.component_data["Aging"]["is_egg"] = False
        simobject_instance.component_data["Aging"]["is_baby"] = False
    elif age_current > age_baby and age_current < age_adult:
        simobject_instance.image = simobject_instance.image_baby
        simobject_instance.component_data["Aging"]["is_egg"] = False
        simobject_instance.component_data["Aging"]["is_baby"] = True
    else:
        simobject_instance.image = simobject_instance.image_default


def system_forage(simobject_instance, component_instance, ecosphere_map):
    if "Aging" in simobject_instance.component_data:
        if simobject_instance.component_data["Aging"]["is_egg"]:
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

    hunger = simobject_instance.component_data[component_instance["name"]]["hunger"]
    hunger_max = simobject_instance.component_data[component_instance["name"]][
        "hunger_max"
    ]

    hunger += 1

    if hunger >= hunger_max:
        simobject_instance.die()
        return
    else:
        simobject_instance.component_data[component_instance["name"]]["hunger"] = hunger

    for search_tile, pos_x, pos_y in simulation_object_yield_tile_neighbour(
        simobject_instance, ecosphere_map
    ):
        if search_tile.occupant:
            if search_tile.occupant == simobject_instance:
                return
            elif search_tile.occupant.species == simobject_instance.species:
                return
            else:
                eat()
                simobject_instance.component_data[component_instance["name"]][
                    "hunger"
                ] = 0


def is_hungry(_simobject_instance):
    hungry = False

    if "Eating" in _simobject_instance.component_data:
        hunger = _simobject_instance.component_data["Eating"]["hunger"]
        hunger_max = _simobject_instance.component_data["Eating"]["hunger_max"]

        if hunger > (int(round(hunger_max / 2))):
            hungry = True
            return hungry

    return hungry


def system_reproduce_sexual_direct(
    simobject_instance, component_instance, ecosphere_map
):
    reproduction_partner = None

    if "Aging" in simobject_instance.component_data:
        if simobject_instance.component_data["Aging"]["is_egg"]:
            print("Egg")
            return
        elif simobject_instance.component_data["Aging"]["is_baby"]:
            print("Baby")
            return

    if is_hungry(simobject_instance):
        print(f"{simobject_instance.name} is too hungry to make a baby.")
        return
    else:
        print(f"{simobject_instance.component_data['Eating']['hunger']} is ok to make a baby.")

    for search_tile, pos_x, pos_y in simulation_object_yield_tile_neighbour(
        simobject_instance, ecosphere_map
    ):
        if search_tile.occupant:
            if not search_tile.occupant == simobject_instance:
                print("Tile has an occupant")

                if not search_tile.occupant.is_dead:
                    reproduction_partner = search_tile.occupant
                    break
        else:
            print("Search tile does not have an occupant")

    if reproduction_partner:
        print(f"Found partner {reproduction_partner.name}")

        if is_hungry(reproduction_partner):
            print(
                f"Partner of {simobject_instance.name}, {reproduction_partner.name}, is too hungry to make a baby."
            )
            return
        else:
            for search_tile, pos_x, pos_y in simulation_object_yield_tile_neighbour(
                simobject_instance, ecosphere_map
            ):
                if not search_tile.occupant:
                    baby = copy.deepcopy(simobject_instance)  # Awww they're so alike

                    baby.is_egg = True
                    baby.is_baby = False

                    if "Eating" in baby.component_data:
                        baby_hunger_max = baby.component_data["Eating"]["hunger_max"]

                        # Set the baby's hunger to 1/4 max hunger
                        baby.component_data["Eating"]["hunger"] = int(
                            round(baby_hunger_max / 4)
                        )

                    baby.age_current = 0

                    ecosphere_map[pos_x][pos_y].occupant = baby

                    if "Eating" in search_tile.occupant.component_data:
                        search_tile.occupant.component_data["Eating"]["hunger"] += int(
                            round(
                                search_tile.occupant.component_data["Eating"][
                                    "hunger_max"
                                ]
                                / 3
                            )
                        )
                    if "Eating" in simobject_instance.component_data:
                        simobject_instance.component_data["Eating"]["hunger"] += int(
                            round(
                                simobject_instance.component_data["Eating"][
                                    "hunger_max"
                                ]
                                / 2
                            )
                        )

                    print(f"Baby was born at (x{pos_x}, y{pos_y})")


component_forage: dict = create_component(
    component_name="Foraging", callback=system_forage
)

component_eat: dict = create_component(
    component_name="Eating",
    callback=system_eat,
)

component_reproduce_sexual_direct: dict = create_component(
    component_name="ReproducingSexuallyDirectly",
    callback=system_reproduce_sexual_direct,
)

component_age: dict = create_component(
    component_name="Aging",
    callback=system_age,
)
