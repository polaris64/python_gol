"""
Module implementing GoL world I/O (loading worlds from file, rendering worlds
as ASCII strings).
"""

import re

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

def rle_extract_dims_from_header(header):
    """
    Given a RLE header string with the format "x = i, y = j", extracts and
    returns the X, Y grid dimensions.
    """
    dims = None
    if header:
        match = re.match(r"^.*(x *= *[0-9]+), ?(y *= *[0-9]+)", header, re.IGNORECASE)
        if match and len(match.groups()) == 2:
            dims_raw = match.groups()
            dims = []
            for dim_raw in dims_raw:
                match = re.match(r"[xy] *= *([0-9]+)", dim_raw, re.IGNORECASE)
                if match and len(match.groups()) == 1:
                    dims.append(int(match.groups()[0]))
            dims = tuple(dims)
    return dims

def rle_build_world_from_data(data):
    """
    Parses a combined RLE data line and builds a world from it.
    """

    # Build the world one line at a time
    world = set()
    lines = data.split("$")
    for y_c, line in enumerate(lines):

        # Find all RLE parts, which are a run length (1 if missing) followed by
        # "o" (alive cell) or "b" (dead cell). Parts can optionally be
        # separated by spaces.
        parts = [x for x in re.split(r"([0-9]* *[bo] *)", line, flags=re.IGNORECASE) if len(x) > 0]

        # Extract run length and type from each part and add cells to the world
        # as necessary
        x_c = 0
        for part in parts:
            match = re.match(r"([0-9]*) *([bo])", part, re.IGNORECASE)
            if match and len(match.groups()) == 2:
                run_len = match.groups()[0]
                run_len = int(run_len) if run_len else 1
                cell_type = match.groups()[1].upper()
                for _ in range(run_len):
                    if cell_type == "O":
                        world.add((x_c, y_c))
                    x_c += 1

    return world

def load_world_from_rle(filename):
    """
    Loads a world from a file in RLE format
    """

    # Read header and data_lines from filename
    with open(filename, "rt") as rlefile:
        header = None
        data_lines = []

        for line in rlefile.readlines():

            # Skip all empty and command lines
            if not line or not line.strip() or line[:1] == "#":
                continue

            # Header if always the first non-command line
            if not header:
                header = line.strip()
            else:
                data_lines.append(line.strip())

    # Header and >= 1 data_lines must have been read
    if not data_lines or not header:
        return None

    # Extract grid dimensions from the header (format: "x = i, y = j")
    dims = rle_extract_dims_from_header(header)

    # Abort if dimensions were not read correctly
    if not dims or len(dims) != 2:
        return None

    # Join all data_lines to one single data_line: actual grid lines are
    # independently separated by "$"
    data_line = "".join(data_lines)

    return rle_build_world_from_data(data_line)

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
