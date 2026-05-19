from __future__ import annotations
import random
from typing import List, Optional, Set, Tuple


#################################################
# NOTE
#################################################

class Note:

    def __init__(self, degree: int, duration: float = 1.0):
        self.degree = degree
        self.duration = duration

    def __repr__(self):
        return str(self.degree)


#################################################
# TILE
#################################################

# tiles represent melodic INTERVALS
# example: (1,-1) means up step then down step

Tile = Tuple[int, int]

TILES: List[Tile] = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (2, -1),
    (-2, 1),
    (3, -1),
    (-3, 1),
]

TILE_SIZE = 2


#################################################
# COMPATIBILITY
#################################################

def compatible(a: Tile, b: Tile) -> bool:
    return a[1] == b[0]


forward_compat = {t: set() for t in TILES}
backward_compat = {t: set() for t in TILES}

for a in TILES:
    for b in TILES:

        if compatible(a, b):
            forward_compat[a].add(b)

        if compatible(b, a):
            backward_compat[a].add(b)


#################################################
# WFC
#################################################

def generate_melody(length: int = 12) -> List[Note]:

    positions = length - TILE_SIZE

    wave: List[Set[Tile]] = [set(TILES) for _ in range(positions)]
    collapsed: List[Optional[Tile]] = [None] * positions

    run_wfc(wave, collapsed)

    return tiles_to_notes(collapsed, length)


def run_wfc(wave, collapsed):

    while None in collapsed:

        choices = [i for i, v in enumerate(collapsed) if v is None]

        idx = min(choices, key=lambda i: len(wave[i]))

        tile = random.choice(list(wave[idx]))

        collapsed[idx] = tile
        wave[idx] = {tile}

        propagate(wave, idx)


#################################################
# PROPAGATION
#################################################

def propagate(wave, start_idx):

    stack = [start_idx]

    while stack:

        idx = stack.pop()

        if idx + 1 < len(wave):

            allowed = set()

            for t in wave[idx]:
                allowed |= forward_compat[t]

            new = wave[idx+1].intersection(allowed)

            if new != wave[idx+1]:

                wave[idx+1] = new
                stack.append(idx+1)

        if idx - 1 >= 0:

            allowed = set()

            for t in wave[idx]:
                allowed |= backward_compat[t]

            new = wave[idx-1].intersection(allowed)

            if new != wave[idx-1]:

                wave[idx-1] = new
                stack.append(idx-1)


#################################################
# BUILD MELODY
#################################################

def tiles_to_notes(tiles, length):

    melody = [random.choice([1,3,5])]

    for tile in tiles:

        step = tile[0]

        next_degree = melody[-1] + step

        next_degree = max(1, min(7, next_degree))

        melody.append(next_degree)

    melody = melody[:length]

    melody[-1] = 1

    return [Note(d) for d in melody]


#################################################
# TEST
#################################################

if __name__ == "__main__":

    for _ in range(10):

        melody = generate_melody(12)

        print(melody)
