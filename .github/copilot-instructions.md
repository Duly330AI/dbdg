## Quick orientation

This small Pygame project implements a Boulder-Dash style game. Key code lives under
`src/dbdg/`:

- `game.py` – Pygame loop, rendering, sound hooks (entry point `dbdg.game:main`).
- `engine/grid.py` – Level parsing, tile constants, `Level` dataclass, coordinate helpers.
- `engine/physics.py` – Core game rules: `step_player`, `tick_gravity`, and `tick`.

Entry points and common commands

- Run game: `python -m dbdg` (script `dbdg` is defined in `pyproject.toml`).
- Run tests: `pytest -q` (tests are in `tests/`).
- Dev install: `pip install -e ".[dev]"` (see `[project.optional-dependencies]` in `pyproject.toml`).

Important data shapes & conventions (do not assume immutability)

- Level.grid is a List[List[int]] indexed as `grid[y][x]` (row-major). See `Level` in `engine/grid.py`.
- Tile IDs are small ints (constants in `engine/grid.py`): EMPTY, DIRT, ROCK, GEM, STEEL, PLAYER, EXIT_CLOSED, EXIT_OPEN.
- ASCII level format uses these chars: ` " ", ".", "o", "*", "#", "P", "E", "e"` which map via `TILE_FROM_CHAR`.
- Coordinates are (x, y). `find_player(level)` returns `(x, y)`.
- Most engine functions mutate `level.grid` in-place (e.g. `step_player`, `tick_gravity`). When editing code, prefer in-place updates or be explicit when cloning with `clone_grid()`.

Physics contract (how `tick` behaves)

- Signature: `tick(level, player_input, gems_collected, exit_open) -> TickResult`
  - `player_input` is a tuple `(dx, dy)` where dx/dy are -1/0/1.
  - Returns `TickResult` with `.grid`, `.events` (sound keys), `.player_alive`, `.gems_collected`, `.exit_open`.
- Order: `step_player` applies the player's move first (including pushes and gem collection), then `tick_gravity` applies falling/rolling.
- `events` contains strings like `dig`, `gem`, `push`, `fall`, `roll`, `exit-open`, `exit-enter` used by `game.py` to play SFX.

Where to make changes (examples)

- Add a new tile: update `TILE_FROM_CHAR` / `CHAR_FROM_TILE` in `engine/grid.py`, pick an unused int constant, update `COLORS` and `render_tile` in `game.py` for visuals.
- Change physics: edit `engine/physics.py`. Note the engine mutates `level.grid` directly; tests create levels via `parse_level(...)` and call `tick(...)`.
- Change level content: `levels/*.txt` are ASCII levels parsed by `parse_level()`.

Tests & examples

- Tests live in `tests/` and use simple ASCII level strings parsed with `parse_level`. See `tests/test_physics.py` for patterns:
  - Use `parse_level(text, target_gems=...)` to create a Level.
  - Call `tick(...)` or helper loops to simulate multiple ticks.
- When adding tests, assert on `TickResult` fields (e.g. `.exit_open`, `.gems_collected`, `.player_alive`) or directly inspect `level.grid[y][x]`.

Build / CI notes

- `pyproject.toml` defines the package and dev dependencies (pygame needed to run the game; tests only exercise engine code).
- Packaging hint: `pyinstaller -F -n dbdg ...` is used in README for standalone builds.

Quick tips for agents

- Prefer editing `engine/*` for deterministic logic changes; keep rendering and sound code isolated in `game.py`.
- Respect in-place mutation semantics: many callers rely on `level.grid` being updated by functions.
- Use the existing event strings when producing audio/visual side effects so `game.play_events` maps them to SFX.

Files to open first

- `src/dbdg/engine/grid.py` (tile map and parsing)
- `src/dbdg/engine/physics.py` (rules and tick contract)
- `src/dbdg/game.py` (loop, rendering, SFX mapping)
- `tests/test_physics.py` (examples of how code is used in tests)

If anything here is unclear or you want more examples (e.g., adding a new tile type or writing a focused unit test), ask and I'll expand the instructions.
