#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module implementing GoL world I/O (loading worlds from file, rendering worlds
as ASCII strings).
"""

def load_world(filename, alive="#"):
    """
    Loads a world from a given file
    """
    with open(filename, "rt") as worldfile:
        grid = [[1 if x == alive else 0 for x in line] for line in worldfile.readlines()]
        world = set()
        for y_c, row in enumerate(grid):
            for x_c, cell in enumerate(row):
                if cell == 1:
                    world.add((x_c, y_c))
    return world

def render_world(world, alive="#", dead="."):
    """
    Renders and returns the given world as a string
    """
    x_range = (min(world, key=lambda x: x[0])[0], max(world, key=lambda x: x[0])[0])
    y_range = (min(world, key=lambda x: x[1])[1], max(world, key=lambda x: x[1])[1])
    output = "x-range:{}, y-range:{}\n".format(x_range, y_range)
    for y_c in range(y_range[0] - 1, y_range[1] + 2):
        for x_c in range(x_range[0] - 1, x_range[1] + 2):
            output += alive if (x_c, y_c) in world else dead
        output += "\n"
    return output
