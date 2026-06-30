# DBDG – Duly's Boulder Dash Game

**DBDG** is a small Python/Pygame cave puzzle game inspired by classic tile-based digging games.

The player digs through dirt, collects gems, avoids falling rocks, and reaches the exit once enough gems have been collected. The project uses simple programmatically generated graphics and lightweight 8-bit-style sound effects, so no external art assets are required.

## Status

**Finished small game / portfolio side project**

The game is playable and includes multiple levels, simple physics rules, generated assets, tests, and optional packaging support.

## Features

- Tile-based cave gameplay
- Dirt digging
- Gem collection
- Falling rocks and gems
- Basic rolling physics
- Exit unlock logic
- Restart and pause controls
- Programmatically generated graphics
- Generated 8-bit-style WAV sound effects
- ASCII-based level files
- Pytest-based test suite
- Optional Windows executable packaging

## Screenshots

<img width="639" height="413" alt="DBDG gameplay screenshot" src="https://github.com/user-attachments/assets/7965afd6-b55f-4b3d-8af2-15b1c8ccb5c0" />

<img width="642" height="414" alt="DBDG level screenshot" src="https://github.com/user-attachments/assets/052df751-5aad-4ae3-bea2-9d032d47cec7" />

## Controls

- **Arrow keys:** move, dig dirt, collect gems, push rocks
- **R:** restart level
- **P:** pause
- **ESC:** quit

## Game Rules

- Rocks and gems fall downward when unsupported.
- Rocks can roll sideways if blocked below and space is available.
- The player digs through dirt by moving into it.
- Gems increase the score.
- The exit opens when enough gems have been collected.

## Tech Stack

- Python
- Pygame
- Pytest
- PyInstaller optional

## Quick Start

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### Install and run

```bash
pip install -e ".[dev]"
python -m dbdg
```

## Tests

```bash
pytest -q
```

## Packaging

Example Windows build with PyInstaller:

```bash
pyinstaller -F -n dbdg --clean -i NONE -w -m dbdg
```

## Project Structure

```text
src/dbdg/
  engine/        # grid and physics logic
  game.py        # Pygame loop and rendering
  __main__.py    # python -m dbdg
assets/sfx/      # generated WAV files
levels/          # ASCII levels
tests/           # pytest tests
.vscode/         # editor setup
```

## Notes

DBDG is a small completed side project. It was built as an LLM-/agent-friendly Python codebase with separated game logic, simple rendering, generated assets, and tests.

## License

MIT
