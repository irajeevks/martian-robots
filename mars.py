from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Iterable, Set

# Orientation order (clockwise). Index math makes L/R trivial.
ORIENTS = "NESW"
DELTA = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}

@dataclass
class Grid:
    max_x: int
    max_y: int
    scents: Set[Tuple[int, int]]

    def __init__(self, max_x: int, max_y: int):
        if max_x < 0 or max_y < 0:
            raise ValueError("Grid coordinates must be >= 0")
        if max_x > 50 or max_y > 50:
            raise ValueError("Coordinates exceed maximum allowed (50)")  # Spec: maximum value for any coordinate is 50
        self.max_x = max_x
        self.max_y = max_y
        self.scents = set()

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y


@dataclass
class Robot:
    x: int
    y: int
    orient: str
    lost: bool = False

    def turn_left(self) -> None:
        idx = ORIENTS.index(self.orient)
        self.orient = ORIENTS[(idx - 1) % len(ORIENTS)]

    def turn_right(self) -> None:
        idx = ORIENTS.index(self.orient)
        self.orient = ORIENTS[(idx + 1) % len(ORIENTS)]

    def forward(self, grid: Grid) -> None:
        if self.lost:
            return
        dx, dy = DELTA[self.orient]
        nx, ny = self.x + dx, self.y + dy

        if grid.in_bounds(nx, ny):
            self.x, self.y = nx, ny
            return

        # Off-grid move: check scent at current position
        if (self.x, self.y) in grid.scents:
            # Ignore this dangerous move
            return

        # Become lost and leave a scent at the last valid cell
        grid.scents.add((self.x, self.y))
        self.lost = True

    def apply(self, cmd: str, grid: Grid) -> None:
        if self.lost:
            return
        # Command dispatch; extend here for future commands
        if cmd == 'L':
            self.turn_left()
        elif cmd == 'R':
            self.turn_right()
        elif cmd == 'F':
            self.forward(grid)
        else:
            raise ValueError(f"Unknown command: {cmd}")


def simulate(grid: Grid, start: Tuple[int, int, str], program: str) -> Robot:
    x, y, o = start
    if o not in ORIENTS:
        raise ValueError("Invalid orientation; expected one of N,E,S,W")
    bot = Robot(x, y, o)
    for c in program.strip():
        bot.apply(c, grid)
        if bot.lost:
            break
    return bot


def parse_input(lines: Iterable[str]) -> Tuple[Grid, List[Tuple[Tuple[int, int, str], str]]]:
    lines = [ln.strip() for ln in lines if ln.strip() != ""]
    if not lines:
        raise ValueError("Empty input")

    # First line: grid upper-right
    try:
        gx, gy = map(int, lines[0].split())
    except Exception as e:
        raise ValueError("Invalid grid line; expected 'X Y'") from e

    grid = Grid(gx, gy)

    pairs: List[Tuple[Tuple[int, int, str], str]] = []
    i = 1
    while i < len(lines):
        # Position line
        try:
            x_str, y_str, o = lines[i].split()
            x, y = int(x_str), int(y_str)
        except Exception as e:
            raise ValueError("Invalid robot position; expected 'X Y O'") from e

        # Instruction line
        if i + 1 >= len(lines):
            raise ValueError("Missing instruction line for robot")

        prog = lines[i + 1].strip()
        # Basic validation
        if not prog or any(c not in {"L","R","F"} for c in prog):
            # We restrict to L/R/F per spec; easy to extend later
            invalids = ''.join(sorted(set(c for c in prog if c not in {"L","R","F"})))
            raise ValueError(f"Invalid instruction(s): {invalids!r}")


        pairs.append(((x, y, o), prog))
        i += 2

    return grid, pairs


def format_output(robot: Robot) -> str:
    base = f"{robot.x} {robot.y} {robot.orient}"
    return base + (" LOST" if robot.lost else "")

