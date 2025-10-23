from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable

from .grid import (
    Level,
    EMPTY, DIRT, ROCK, GEM, STEEL, PLAYER, EXIT_CLOSED, EXIT_OPEN,
    in_bounds, clone_grid, find_player
)

@dataclass
class TickResult:
    grid: List[List[int]]
    events: List[str]
    player_alive: bool
    gems_collected: int
    exit_open: bool

# Directions
DIRS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

def can_player_enter(tile: int) -> bool:
    return tile in (EMPTY, DIRT, GEM, EXIT_OPEN, EXIT_CLOSED)

def step_player(level: Level, dx: int, dy: int, gems_collected: int, exit_open: bool) -> Tuple[int, int, int, bool, List[str]]:
    events: List[str] = []
    px, py = find_player(level)
    tx, ty = px + dx, py + dy
    if not in_bounds(level, tx, ty):
        return px, py, gems_collected, exit_open, events
    target = level.grid[ty][tx]

    # Handle pushing rocks horizontally
    if target == ROCK and dy == 0:
        beyond_x = tx + dx
        if in_bounds(level, beyond_x, ty) and level.grid[ty][beyond_x] == EMPTY:
            # push
            level.grid[ty][beyond_x] = ROCK
            level.grid[ty][tx] = EMPTY
            target = EMPTY
            events.append("push")

    if target == STEEL:
        return px, py, gems_collected, exit_open, events

    # Move player
    if target in (EMPTY, DIRT, GEM, EXIT_OPEN, EXIT_CLOSED):
        # collect
        if target == DIRT:
            events.append("dig")
        if target == GEM:
            gems_collected += 1
            events.append("gem")
        if target == EXIT_OPEN:
            events.append("exit-enter")
        # If exit is closed, allow standing on it but it's not win yet
        level.grid[py][px] = EMPTY
        level.grid[ty][tx] = PLAYER
        px, py = tx, ty

    # Open exit when enough gems
    if not exit_open and gems_collected >= level.target_gems:
        # convert all EXIT_CLOSED to EXIT_OPEN
        for y in range(level.height):
            for x in range(level.width):
                if level.grid[y][x] == EXIT_CLOSED:
                    level.grid[y][x] = EXIT_OPEN
        exit_open = True
        events.append("exit-open")

    return px, py, gems_collected, exit_open, events

def tick_gravity(level: Level) -> Tuple[List[str], bool]:
    """Apply gravity/rolling for ROCK and GEM. Returns (events, player_alive)."""
    events: List[str] = []
    player_alive = True
    g = level.grid
    w, h = level.width, level.height
    moved = [[False]*w for _ in range(h)]

    for y in range(h-2, -1, -1):  # from second-last row up to top
        for x in range(w):
            t = g[y][x]
            if t not in (ROCK, GEM):
                continue
            if moved[y][x]:
                continue
            below = g[y+1][x]
            # fall straight
            if below == EMPTY:
                g[y+1][x] = t
                g[y][x] = EMPTY
                moved[y+1][x] = True
                events.append("fall")
                continue
            # roll left
            if below in (ROCK, GEM, STEEL):
                lx = x - 1
                if lx >= 0 and g[y][lx] == EMPTY and g[y+1][lx] == EMPTY:
                    g[y][lx] = t
                    g[y][x] = EMPTY
                    moved[y][lx] = True
                    events.append("roll")
                    continue
                # roll right
                rx = x + 1
                if rx < w and g[y][rx] == EMPTY and g[y+1][rx] == EMPTY:
                    g[y][rx] = t
                    g[y][x] = EMPTY
                    moved[y][rx] = True
                    events.append("roll")
                    continue
            # if falling onto player (when player is just below), we could kill; keep simple for now
            # We'll detect crush after all moves:
    # detect crush (any ROCK/GEM resting on player?)
    px, py = find_player(level)
    if py+1 < h and g[py+1][px] in (ROCK, GEM) and g[py][px] == PLAYER:
        # If the rock moved into player last tick, treat as safe if not falling;
        # Simplification: no crush unless it actually moved into player's tile, which we didn't model.
        pass
    return events, player_alive

def tick(level: Level, player_input: Tuple[int, int], gems_collected: int, exit_open: bool) -> TickResult:
    # player move first (BD variants differ; this is intuitive for arcade feel)
    px, py, gems_collected, exit_open, ev1 = step_player(level, player_input[0], player_input[1], gems_collected, exit_open)
    ev2, alive = tick_gravity(level)
    events = ev1 + ev2
    return TickResult(grid=level.grid, events=events, player_alive=alive, gems_collected=gems_collected, exit_open=exit_open)
