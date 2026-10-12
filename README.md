# Maeve's Ecosphere

<p><a href="https://ko-fi.com/molasses"><img src="https://img.shields.io/badge/donate-kofi-blue?style=for-the-badge&amp;logo=ko-fi&amp;color=e57578&amp;logoColor=FFFFFF&amp;labelColor=262a35" alt="Ko-Fi"></a>
<a href="https://www.patreon.com/molasseslover"><img src="https://img.shields.io/badge/donate-patreon-blue?style=for-the-badge&amp;logo=patreon&amp;color=e57578&amp;logoColor=FFFFFF&amp;labelColor=262a35" alt="Patreon"></a> 

This is a simple procedural cellular automata simulation resembling an ecosystem. 
I made this, in my boredom, to toy around with during a lengthy 
[PEM](https://en.wikipedia.org/wiki/Post-exertional_malaise) flare-up.

The project makes use of rudimentary ECS-inspired framework, which makes use 
of Python's dictionaries to manage data. Every tile (cell) is an object which 
may contain another object as its `occupant`. These objects are referred to 
as `SimulationObject`s and are this project's (much more bloated) equivalent
to entities. Every `SimulationObject` contains a list of components, stored as
dictionaries. Every component dictionary contains a callback function, which 
serves as a system instance, as you'd see in a project using a conventional
ECS architecture. Lastly, `SimulationObject`s also contain a `component_data` 
dictionary which stores data accessed by components, straying from real 
ECS implementations where data is stored directly inside of components.

![A screenshot of the Maeve's Ecosphere project depicting various tiles, each one depicting either a tree, grass, mushroom, or an isopod.](/docs/img/screenshot.png)

[YouTube Video](https://youtu.be/FK47rwov3aU)

## Features 

- Tiles which may be occupied by simulated objects
- Simulated objects which may:
    - Forage to other tiles.
    - Consume other objects.
    - Starve to death if too hungry.
    - Produce objects in neighbouring tiles by:
        - Reproducing with partner objects.
        - Reproducing on their own.
    - Age into different life stages.
    - Die after reaching a certain age.
    - Decompose after death.
    - Affect the nutrition of a tile on birth or death.

### Organisms
#### Trees
Trees take a significant amount of time to age into adulthood, and
consequently encroach on surrounding organisms over time.

#### Grass
Grass has a very short lifespan, and serves as the initial food source for
animals.

#### Mushrooms
Mushrooms take a long time to reach adulthood, spread prior to adulthood, and
serve as the main food source for animals.

#### Isopods
Isopods forage the map, eating and mating with partner isopods when they can.

## Cloning
This project makes use of the [Git LFS](https://git-lfs.com/) extension, please
make sure to install it prior to cloning.

```sh
➜ git lfs install
```

Already cloned the repository before setting Git LFS up? After you've 
installed Git LFS, these commands should download all Git LFS files.

```sh
➜ git lfs fetch --all
➜ git lfs pull
➜ git lfs checkout
```

## Credits
Image assets under the [`res/img/`](res/img) directory are taken from or 
derivations of Pierre Vandermaesen' 1-bit asset pack,
found [here](https://pierre-vandermaesen.itch.io/1-bit-16x16-asset-packs).

## Running & Installing
### Nix

The recommended installation route is with use of Nix. This project provides a Nix 
flake which can be installed via Home Manager, your NixOS configuration, and
a plethora of other solutions which support Nix flakes.

Alternatively the project can simply be run without installation using the following command:

```sh
➜ nix build .; ./result/result/bin/maeves-ecosphere
```

### Python

Installation is required to run this project without Nix.

```sh
➜ pip install pygame cython
➜ pip install .
➜ python -m mecosphere.cli
```