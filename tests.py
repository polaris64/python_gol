#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for all functions in "gol" and "world" modules
"""

import gol
import world

EXAMPLE_FILE = "./examples/glider.txt"

def test_load_world():
    """Tests world.load_world()"""
    gol_world = world.load_world(EXAMPLE_FILE, alive="#")
    assert len(gol_world) == 5
    assert gol_world == set([(3, 1), (1, 2), (3, 2), (2, 3), (3, 3)])

    gol_world = world.load_world(EXAMPLE_FILE, alive="O")
    assert gol_world == set()

def test_render_world():
    """Tests world.render_world()"""
    gol_world = world.load_world(EXAMPLE_FILE)
    actual = world.render_world(gol_world, alive="#", dead=".")
    expected = "x-range:(1, 3), y-range:(1, 3)\n"
    expected += ".....\n"
    expected += "...#.\n"
    expected += ".#.#.\n"
    expected += "..##.\n"
    expected += ".....\n"
    assert actual == expected

    actual = world.render_world(gol_world, alive="O", dead=" ")
    expected = "x-range:(1, 3), y-range:(1, 3)\n"
    expected += "     \n"
    expected += "   O \n"
    expected += " O O \n"
    expected += "  OO \n"
    expected += "     \n"
    assert actual == expected

def test_simulate():
    """Tests gol.simulate()"""
    gol_world = world.load_world(EXAMPLE_FILE)

    # x-range:(1, 3), y-range:(1, 3)
    # .....
    # ...#.
    # .#.#.
    # ..##.
    # .....
    actual = gol.simulate(gol_world, iterations=0)
    assert actual == set([(3, 1), (1, 2), (3, 2), (2, 3), (3, 3)])

    # x-range:(2, 4), y-range:(1, 3)
    # .....
    # .#...
    # ..##.
    # .##..
    # .....
    actual = gol.simulate(gol_world, iterations=1)
    assert actual == set([(2, 1), (3, 2), (4, 2), (2, 3), (3, 3)])

    # x-range:(2, 4), y-range:(1, 3)
    # .....
    # ..#..
    # ...#.
    # .###.
    # .....
    actual = gol.simulate(gol_world, iterations=2)
    assert actual == set([(3, 1), (4, 2), (2, 3), (3, 3), (4, 3)])
