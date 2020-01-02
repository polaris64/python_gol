#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module implementing the core Game of Life algorithm
"""

def get_neighbours(cell):
    """
    Yields each neighbouring cell co-ordinate
    """
    yield (cell[0] - 1, cell[1] - 1)
    yield (cell[0], cell[1] - 1)
    yield (cell[0] + 1, cell[1] - 1)
    yield (cell[0] - 1, cell[1])
    yield (cell[0] + 1, cell[1])
    yield (cell[0] - 1, cell[1] + 1)
    yield (cell[0], cell[1] + 1)
    yield (cell[0] + 1, cell[1] + 1)

def simulate(initial_world, iterations=1):
    """
    Takes a starting world state and performs a number of iterations of the
    Game of Life upon it.  Returns the final world state.
    """
    world = initial_world.copy()

    for _ in range(iterations):
        new_world = set()

        for cell in world:

            # For all neighbours, check if any empty node has 3 living
            # neighbours. If so, add a new living cell to new_world.
            new_world.update(
                [
                    neighbour
                    for neighbour
                    in [x for x in get_neighbours(cell) if x not in world]
                    if len([x for x in get_neighbours(neighbour) if x in world]) == 3
                ]
            )

            # If cell remains alive, add it to new_world
            if 2 <= len([x for x in get_neighbours(cell) if x in world]) <= 3:
                new_world.add(cell)

            # Cells with < 2 or > 3 neighbours are not added to new_world,
            # therefore they die

        world = new_world.copy()

    return world
