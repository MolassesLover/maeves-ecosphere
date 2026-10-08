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

from mecosphere.application import *
from mecosphere.simulation import *
from mecosphere.tilemap import *


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
