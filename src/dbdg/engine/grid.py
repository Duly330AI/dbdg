from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

# Tile IDs (small ints for speed)
EMPTY, DIRT, ROCK, GEM, STEEL, PLAYER, EXIT_CLOSED, EXIT_OPEN = range(8)

TILE_FROM_CHAR = {
    " ": EMPTY,
    ".": DIRT,
    "o": ROCK,
    "*": GEM,
    "#": STEEL,
    "P": PLAYER,
    "E": EXIT_CLOSED,
    "e": EXIT_OPEN,
}
CHAR_FROM_TILE = {v: k for k, v in TILE_FROM_CHAR.items()}

@dataclass
class Level:
    grid: List[List[int]]
    width: int
    height: int
    target_gems: int = 5

def parse_level(text: str, target_gems: int = 5) -> Level:
    rows = [list(line.rstrip("\n")) for line in text.splitlines() if line.strip()]
    h = len(rows)
    w = max(len(r) for r in rows)
    grid: List[List[int]] = [[EMPTY] * w for _ in range(h)]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            grid[y][x] = TILE_FROM_CHAR.get(ch, EMPTY)
    return Level(grid=grid, width=w, height=h, target_gems=target_gems)

def find_player(level: Level) -> Tuple[int, int]:
    for y in range(level.height):
        for x in range(level.width):
            if level.grid[y][x] == PLAYER:
                return (x, y)
    raise ValueError("Player not found")

def in_bounds(level: Level, x: int, y: int) -> bool:
    return 0 <= x < level.width and 0 <= y < level.height

def clone_grid(grid: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in grid]
