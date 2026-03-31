"""
Battleship Game Engine
Pure logic — no Discord dependencies.
"""
import random

GRID_SIZE = 10

SHIPS = [
    ("Carrier",    5),
    ("Battleship", 4),
    ("Cruiser",    3),
    ("Submarine",  3),
    ("Destroyer",  2),
]

# Shoot result constants
RESULT_ALREADY_SHOT = "already_shot"
RESULT_MISS         = "miss"
RESULT_HIT          = "hit"
RESULT_SUNK         = "sunk"
RESULT_WIN          = "win"
RESULT_INVALID      = "invalid"


class Ship:
    def __init__(self, name: str, size: int, cells: list[tuple]):
        self.name  = name
        self.size  = size
        self.cells = set(cells)       # {(r, c), …}
        self.hits  = set()

    @property
    def is_sunk(self) -> bool:
        return self.hits >= self.cells

    def try_hit(self, r: int, c: int) -> bool:
        if (r, c) in self.cells:
            self.hits.add((r, c))
            return True
        return False

    def __repr__(self):
        return f"<Ship {self.name} size={self.size} sunk={self.is_sunk}>"


class BattleshipGame:
    """One game instance (one player vs. hidden fleet)."""

    def __init__(self):
        # What the player can see: '~' hidden, 'X' hit, 'O' miss
        self.grid: list[list[str]] = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships:   list[Ship]   = []
        self.shots:   set[tuple]   = set()
        self.over:    bool         = False
        self._place_ships()

    # ──────────────────────────────────────── Ship placement ─────────────────

    def _place_ships(self):
        occupied: set[tuple] = set()
        for name, size in SHIPS:
            placed = False
            attempts = 0
            while not placed:
                attempts += 1
                if attempts > 1000:
                    raise RuntimeError("Ship placement exceeded retry limit")
                horizontal = random.choice((True, False))
                if horizontal:
                    r = random.randint(0, GRID_SIZE - 1)
                    c = random.randint(0, GRID_SIZE - size)
                    cells = [(r, c + i) for i in range(size)]
                else:
                    r = random.randint(0, GRID_SIZE - size)
                    c = random.randint(0, GRID_SIZE - 1)
                    cells = [(r + i, c) for i in range(size)]

                # Also check one-cell buffer around ship
                buffer: set[tuple] = set()
                for (br, bc) in cells:
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            buffer.add((br + dr, bc + dc))

                if not buffer & occupied:
                    occupied.update(cells)
                    self.ships.append(Ship(name, size, cells))
                    placed = True

    # ──────────────────────────────────────── Shooting ───────────────────────

    def shoot(self, row: int, col: int) -> tuple[str, Ship | None]:
        """
        row, col are 0-indexed.
        Returns (result_constant, ship_or_None).
        """
        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return RESULT_INVALID, None

        if (row, col) in self.shots:
            return RESULT_ALREADY_SHOT, None

        self.shots.add((row, col))

        for ship in self.ships:
            if ship.try_hit(row, col):
                self.grid[row][col] = 'X'
                if ship.is_sunk:
                    if all(s.is_sunk for s in self.ships):
                        self.over = True
                        return RESULT_WIN, ship
                    return RESULT_SUNK, ship
                return RESULT_HIT, ship

        self.grid[row][col] = 'O'
        return RESULT_MISS, None

    # ──────────────────────────────────────── Helpers ────────────────────────

    @property
    def ships_remaining(self) -> int:
        return sum(1 for s in self.ships if not s.is_sunk)

    @property
    def ships_sunk(self) -> int:
        return sum(1 for s in self.ships if s.is_sunk)

    @property
    def total_shots(self) -> int:
        return len(self.shots)

    @property
    def hit_count(self) -> int:
        return sum(1 for r in range(GRID_SIZE)
                   for c in range(GRID_SIZE) if self.grid[r][c] == 'X')

    def accuracy(self) -> float:
        if self.total_shots == 0:
            return 0.0
        return self.hit_count / self.total_shots * 100

    def fleet_status(self) -> list[dict]:
        """Return list of {name, size, sunk} for all ships."""
        return [{"name": s.name, "size": s.size, "sunk": s.is_sunk}
                for s in self.ships]
