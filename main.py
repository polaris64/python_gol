#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple implementation of Conway's Game of Life, rendered as ASCII text
"""

import argparse
import time

import gol
import world

def main():
    """
    Main CLI handler
    """
    parser = argparse.ArgumentParser(description="Conway's Game of Life simulation")
    parser.add_argument(
        "worldfile",
        help="Path to file containing the initial world layout",
        type=str
    )
    parser.add_argument(
        "--delay",
        default=0.1,
        help="Delay between frames in seconds (defaults to 0.1)",
        required=False,
        type=float
    )
    parser.add_argument(
        "--alive",
        default="#",
        help="Character to use when rendering living cells (defaults to \"#\")",
        required=False,
        type=str
    )
    parser.add_argument(
        "--dead",
        default=" ",
        help="Character to use when rendering living cells (defaults to \" \")",
        required=False,
        type=str
    )
    args = parser.parse_args()

    if args.worldfile[-3:].upper() == "RLE":
        gol_world = world.load_world_from_rle(args.worldfile)
    else:
        gol_world = world.load_world(args.worldfile)
    while True:
        gol_world = gol.simulate(gol_world, 1)
        print(world.render_world(gol_world, alive=args.alive, dead=args.dead))
        time.sleep(args.delay)

if __name__ == "__main__":
    main()
