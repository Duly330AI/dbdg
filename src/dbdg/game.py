from __future__ import annotations

import os
import sys
import time
from pathlib import Path
import pygame

from .engine.grid import parse_level, find_player, EMPTY, DIRT, ROCK, GEM, STEEL, PLAYER, EXIT_CLOSED, EXIT_OPEN, Level
from .engine.physics import tick

TILE_SIZE = 32
FPS = 60
TICKS_PER_SECOND = 10  # physics speed
TICK_INTERVAL = 1.0 / TICKS_PER_SECOND

# Simple palette
COLORS = {
    EMPTY: (10, 10, 10),
    DIRT: (110, 72, 42),
    ROCK: (120, 120, 120),
    GEM: (40, 200, 255),
    STEEL: (80, 80, 100),
    PLAYER: (255, 220, 60),
    EXIT_CLOSED: (0, 120, 40),
    EXIT_OPEN: (0, 200, 80),
}

SFX_FILES = {
    "dig": "assets/sfx/dig.wav",
    "gem": "assets/sfx/gem.wav",
    "push": "assets/sfx/push.wav",
    "fall": "assets/sfx/fall.wav",
    "roll": "assets/sfx/roll.wav",
    "exit-open": "assets/sfx/exit_open.wav",
    "exit-enter": "assets/sfx/exit_enter.wav",
}

def load_level_text(name: str) -> str:
    p = Path(__file__).resolve().parents[2] / "levels" / name
    return p.read_text(encoding="utf-8")

def ensure_sfx():
    # SFX are shipped in repo. Nothing to do here, but keep hook if user deletes them.
    missing = [k for k, v in SFX_FILES.items() if not Path(v).exists()]
    if missing:
        print("[WARN] Missing SFX:", missing)

def render_tile(surf: pygame.Surface, x: int, y: int, tile: int):
    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    color = COLORS.get(tile, (255, 0, 255))
    pygame.draw.rect(surf, color, rect)

    # embellishments
    if tile == ROCK:
        pygame.draw.circle(surf, (200, 200, 200), rect.center, TILE_SIZE // 3, width=2)
    elif tile == GEM:
        pygame.draw.polygon(
            surf,
            (220, 255, 255),
            [
                (rect.centerx, rect.top + 6),
                (rect.right - 6, rect.centery),
                (rect.centerx, rect.bottom - 6),
                (rect.left + 6, rect.centery),
            ],
            width=0,
        )
        pygame.draw.polygon(
            surf,
            (60, 120, 140),
            [
                (rect.centerx, rect.top + 6),
                (rect.right - 6, rect.centery),
                (rect.centerx, rect.bottom - 6),
                (rect.left - 2 + 6, rect.centery),
            ],
            width=2,
        )
    elif tile == PLAYER:
        pygame.draw.rect(surf, (0, 0, 0), rect.inflate(-10, -10), border_radius=6)
        pygame.draw.rect(surf, (255, 220, 60), rect.inflate(-14, -14), border_radius=4)
    elif tile == EXIT_OPEN:
        pygame.draw.rect(surf, (255, 255, 255), rect.inflate(-8, -8), width=2)

def play_events(sounds, events):
    for ev in events:
        s = sounds.get(ev)
        if s:
            s.play()

def run():
    # init pygame
    os.environ.setdefault("SDL_AUDIODRIVER", "directsound" if sys.platform.startswith("win") else "")
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    ensure_sfx()
    sounds = {k: pygame.mixer.Sound(v) for k, v in SFX_FILES.items() if Path(v).exists()}

    # load level
    level_text = load_level_text("level1.txt")
    level = parse_level(level_text, target_gems=5)
    w, h = level.width, level.height

    screen = pygame.display.set_mode((w * TILE_SIZE, h * TILE_SIZE))
    pygame.display.set_caption("DBDG – Duly's Boulder Dash Game")
    clock = pygame.time.Clock()

    running = True
    paused = False
    accumulator = 0.0
    last_time = time.perf_counter()
    gems_collected = 0
    exit_open = False

    while running:
        # --- input ---
        move = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # reset
                    level = parse_level(level_text, target_gems=5)
                    gems_collected = 0
                    exit_open = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            move = (1, 0)
        elif keys[pygame.K_UP]:
            move = (0, -1)
        elif keys[pygame.K_DOWN]:
            move = (0, 1)

        # --- tick ---
        now = time.perf_counter()
        dt = now - last_time
        last_time = now
        accumulator += dt

        if not paused:
            while accumulator >= TICK_INTERVAL:
                res = tick(level, move, gems_collected, exit_open)
                gems_collected = res.gems_collected
                exit_open = res.exit_open
                play_events(sounds, res.events)
                accumulator -= TICK_INTERVAL
                move = (0, 0)  # consume input each tick

        # --- render ---
        screen.fill((0, 0, 0))
        for y in range(level.height):
            for x in range(level.width):
                render_tile(screen, x, y, level.grid[y][x])

        # HUD (very simple)
        font = pygame.font.SysFont(None, 24)
        hud = font.render(f"Gems: {gems_collected}/{level.target_gems}  {'[PAUSED]' if paused else ''}", True, (255,255,255))
        screen.blit(hud, (8, 4))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def main():
    run()

if __name__ == "__main__":
    main()
