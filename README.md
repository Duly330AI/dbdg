# DBDG – Duly's Boulder Dash Game (Python + Pygame)

Ein minimaler, **LLM-/Agent-freundlicher** Boulder-Dash-Klon mit **Pygame**.
- **Einfache Grafiken**: werden **programmgeneriert** (keine PNG-Assets nötig).
- **SFX**: einfache **8‑Bit‑Style WAVs** werden mit Python erzeugt (liegen in `assets/sfx`).

## 🚀 Schnellstart

```bash
# Python 3.10+ empfohlen
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -e ".[dev]"         # Spiel + Dev-Tools
python -m dbdg                  # Spiel starten (oder: dbdg)
```

### Tasten
- **Pfeile**: bewegen (Erde graben, Edelsteine einsammeln, Felsen schieben)
- **R**: Level neu starten
- **P**: Pause
- **ESC**: Beenden

## 🧱 Regeln (vereinfacht)
- **Schwerkraft**: Felsen/Edelsteine fallen nach unten.
- **Rollen**: Liegt unterhalb ein Block und links/rechts ist frei, rollen Steine zur Seite.
- **Graben**: Spieler ersetzt Erde durch Leerraum.
- **Edelsteine**: erhöhen den Score; **Exit** öffnet sich, wenn genug gesammelt sind.

## 🧪 Tests
```bash
pytest -q
```

## 🧰 VS Code (empfohlen)
- Installiere empfohlene Extensions (Dialog erscheint beim Öffnen) oder manuell:
  - Python (ms-python.python), Pylance, Ruff, Black Formatter, Even Better TOML
- F5: Debug-Konfiguration „Run DBDG (module)“
- **Tasks**: „Run Game“, „Run Tests“

## 📦 Packaging (optional, Windows-Beispiel)
```bash
pyinstaller -F -n dbdg --clean -i NONE -w -m dbdg
```
Das erzeugt eine `dist/dbdg.exe`. Für macOS notarization/signing beachten.

## 📁 Projektstruktur
```
dbdg/
  ├─ src/dbdg/
  │   ├─ engine/           # reine Logik (grid, physics)
  │   ├─ game.py           # Pygame-Loop + Rendering
  │   └─ __main__.py       # python -m dbdg
  ├─ assets/sfx/           # generierte WAVs
  ├─ levels/               # ASCII-Levels
  ├─ tests/                # pytest
  └─ .vscode/              # Editor-Setup
```

## 🔧 Nächste Schritte / Ideen
- Rock-Explosionen, Gegner, mehr Level, Tiled-Import
- Partikel/Shader (optional), Menü/HUD-Verbesserungen
- CI (GitHub Actions) ist bereits enthalten (pytest)

**Lizenz:** MIT
