"""
Board rendering — produces Discord embed-ready emoji grids.
"""
from game import BattleshipGame, GRID_SIZE

# ── Cell emoji ────────────────────────────────────────────────────────────────
OCEAN   = "🟦"   # unknown water
HIT     = "💥"   # confirmed hit
MISS    = "⬜"   # confirmed miss
SHIP    = "🚢"   # revealed intact ship (post-game)
SUNK    = "🔥"   # revealed sunk ship cell (post-game)

# ── Header labels ─────────────────────────────────────────────────────────────
NUM_EMOJI = [
    "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",
    "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟",
]
CORNER = "↘️"   # top-left corner cell


def render(game: BattleshipGame, reveal: bool = False) -> str:
    """
    Return an emoji grid string suitable for a Discord embed field value.

    If *reveal* is True, show all ship positions (used on game-over / surrender).
    """
    # Pre-compute a lookup of sunk cells for reveal mode
    sunk_cells: set[tuple] = set()
    ship_cells: set[tuple] = set()
    if reveal:
        for ship in game.ships:
            ship_cells.update(ship.cells)
            if ship.is_sunk:
                sunk_cells.update(ship.cells)

    lines: list[str] = []

    # Column header row
    lines.append(CORNER + "".join(NUM_EMOJI[:GRID_SIZE]))

    for r in range(GRID_SIZE):
        row = NUM_EMOJI[r]
        for c in range(GRID_SIZE):
            cell = game.grid[r][c]
            if cell == 'X':
                row += HIT
            elif cell == 'O':
                row += MISS
            elif reveal and (r, c) in sunk_cells:
                row += SUNK
            elif reveal and (r, c) in ship_cells:
                row += SHIP
            else:
                row += OCEAN
        lines.append(row)

    return "\n".join(lines)


def fleet_status_text(game: BattleshipGame) -> str:
    """One-line summary of remaining ships."""
    parts = []
    for info in game.fleet_status():
        icon = "💀" if info["sunk"] else "🚢"
        parts.append(f"{icon} {info['name']} ({info['size']})")
    return "\n".join(parts)
