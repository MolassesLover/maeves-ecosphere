import sys
import random
import time


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


def system_forage(entity_instance, ecosphere_map):
    position_old_tile = ecosphere_map[entity_instance.position[0]][
        entity_instance.position[1]
    ]

    position_old_tile.occupant = entity_instance

    position_new = entity_instance.position.copy()

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

        entity_instance.position = position_new

        position_new_tile.occupant = entity_instance


def system_eat(entity_instance, ecosphere_map):
    for x in range(-1, 1):
        for y in range(-1, 1):
            check_position_x = entity_instance.position[0] + x
            check_position_y = entity_instance.position[1] + y

            print(f"Checking {check_position_x}, {check_position_y} for food")

            if check_position_x > 63:
                check_position_x = 63
            elif check_position_x < 0:
                check_position_x = 0

            if check_position_x > 35:
                check_position_x = 35
            elif check_position_x < 0:
                check_position_x = 0

            search_tile = ecosphere_map[check_position_x][check_position_y]

            if search_tile.occupant:
                if not search_tile.occupant == entity_instance:
                    print(f"Eating {search_tile.occupant.name}")


component_forage: dict = create_component(
    component_name="Foraging", callback=system_forage
)

component_eat: dict = create_component(component_name="Eating", callback=system_eat)
