from __future__ import annotations
import random
from typing import List, Optional, Set, Tuple

#################################################
# NOTE
#################################################

class Note:
    def __init__(self, degree: int, duration: float = 1.0, rest: bool = False):
        self.degree = degree
        self.duration = duration
        self.rest = rest

    def __repr__(self):
        if self.rest:
            return f"r{self.duration}"
        return f"{self.degree}:{self.duration}"

#################################################
# INTERVAL TILES
#################################################

Tile = Tuple[int, int]  # two-step interval motif

INTERVAL_TILES: List[Tile] = [
    (+1, +1),
    (+1, -1),
    (-1, +1),
    (-1, -1),
    (+2, -1),
    (-2, +1),
]

forward_compat = {t: set() for t in INTERVAL_TILES}
backward_compat = {t: set() for t in INTERVAL_TILES}

for a in INTERVAL_TILES:
    for b in INTERVAL_TILES:
        if a[1] == b[0]:
            forward_compat[a].add(b)
        if b[1] == a[0]:
            backward_compat[a].add(b)

#################################################
# RHYTHM WFC
#################################################

RHYTHM_VALUES = [1.0, 0.5, 0.25]  # quarter, eighth, sixteenth
HEAVY_BEATS = [0, 2]  # strong beats in a 4/4 bar

def generate_bar_rhythm(beats: float = 4.0) -> List[float]:
    remaining = beats
    rhythm: List[float] = []
    while remaining > 0:
        choices = [d for d in RHYTHM_VALUES if d <= remaining]
        weights = [1.0 if len(rhythm) in HEAVY_BEATS else 0.7 for _ in choices]
        dur = random.choices(choices, weights=weights)[0]
        rhythm.append(dur)
        remaining -= dur
    return rhythm

#################################################
# MELODY WFC
#################################################

def generate_melody_for_rhythm(rhythm: List[float]) -> List[Note]:
    length = len(rhythm)
    wave: List[Set[Tile]] = [set(INTERVAL_TILES) for _ in range(length-1)]
    collapsed: List[Optional[Tile]] = [None]*(length-1)
    run_wfc(wave, collapsed)

    # convert tiles to absolute degrees
    melody: List[int] = [random.choice([1,3,5])]  # starting note
    for i, t in enumerate(collapsed):
        step = t[0] if i == 0 else t[1]
        next_degree = melody[-1] + step
        next_degree = max(1, min(7, next_degree))
        melody.append(next_degree)
    melody[-1] = 1  # resolve phrase
    notes = [Note(d, dur) for d, dur in zip(melody, rhythm)]
    return notes

def run_wfc(wave: List[Set[Tile]], collapsed: List[Optional[Tile]]):
    while None in collapsed:
        choices = [i for i, v in enumerate(collapsed) if v is None]
        idx = min(choices, key=lambda i: len(wave[i]))
        tile = random.choice(list(wave[idx]))
        collapsed[idx] = tile
        wave[idx] = {tile}
        propagate(wave, idx)

def propagate(wave: List[Set[Tile]], start_idx: int):
    stack = [start_idx]
    while stack:
        idx = stack.pop()
        current_tiles = wave[idx]
        # forward
        if idx+1 < len(wave):
            allowed = set()
            for t in current_tiles:
                allowed |= forward_compat[t]
            new = wave[idx+1].intersection(allowed)
            if new != wave[idx+1]:
                wave[idx+1] = new
                stack.append(idx+1)
        # backward
        if idx-1 >= 0:
            allowed = set()
            for t in current_tiles:
                allowed |= backward_compat[t]
            new = wave[idx-1].intersection(allowed)
            if new != wave[idx-1]:
                wave[idx-1] = new
                stack.append(idx-1)

#################################################
# BAR / PHRASE / SONG GENERATION
#################################################

def generate_bar(beats: float = 4.0) -> List[Note]:
    rhythm = generate_bar_rhythm(beats)
    melody = generate_melody_for_rhythm(rhythm)
    return melody

def generate_phrase(num_bars: int = 4) -> List[Note]:
    phrase: List[Note] = []
    for _ in range(num_bars):
        phrase.extend(generate_bar(4.0))
    phrase[-1].degree = 1  # resolve phrase
    return phrase

def generate_song(num_phrases: int = 4) -> List[Note]:
    song: List[Note] = []
    for _ in range(num_phrases):
        song.extend(generate_phrase(4))
    return song

#################################################
# LILYPOND EXPORT
#################################################

DEGREE_TO_NOTE = {1: "c'", 2: "d'", 3: "e'", 4: "f'", 5: "g'", 6: "a'", 7: "b'"}
DURATION_MAP = {1.0: 4, 0.5: 8, 0.25: 16}

def notes_to_ly_bar(notes: List[Note]) -> str:
    parts = []
    for n in notes:
        dur = DURATION_MAP.get(n.duration, 4)
        if n.rest:
            parts.append(f"r{dur}")
        else:
            pitch = DEGREE_TO_NOTE[n.degree]
            parts.append(f"{pitch}{dur}")
    return " ".join(parts)

def song_to_ly(song: List[Note], beats_per_bar: float = 4.0) -> str:
    lines = ["\\version \"2.24.2\"", "\\absolute {"]
    bar: List[Note] = []
    current_beats = 0.0
    for n in song:
        bar.append(n)
        current_beats += n.duration
        if abs(current_beats - beats_per_bar) < 0.001:
            lines.append(notes_to_ly_bar(bar) + " |")
            bar = []
            current_beats = 0.0
    if bar:
        lines.append(notes_to_ly_bar(bar) + " |")
    lines.append("}")
    return "\n".join(lines)

#################################################
# MAIN
#################################################

if __name__ == "__main__":
    song = generate_song(2)  # 2 phrases x 4 bars
    ly_code = song_to_ly(song)
    with open("output/generated_song.ly", "w") as f:
        f.write(ly_code)
    print("LilyPond file written: generated_song.ly")
