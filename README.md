# Martian Robots (Coding Challenge)
- Clean, well-tested implementation of the Mars robots problem.
- No frameworks. Standard library only (Python 3 + unittest).

## Why these choices?
- **Python 3**: clear, concise, batteries-included ('unittest').
- **Separation of concerns**: 'Grid' manages bounds/scents; 'Robot' owns movement/heading; 'main.py' is pure I/O.
- **Extensible commands**: new instructions can be added via a simple command map.
- **Deterministic & testable**: business logic is isolated and covered by unit tests.

## Project layout
martian-robots/
├─ main.py          # CLI: read input, print results
├─ mars.py          # Core domain: Grid, Robot, parsing
├─ README.md
├─ sample_input.txt
└─ tests/
   └─ test_mars.py  # Unit tests (unittest)

## Running

## 1) Environment (what I used)
•	macOS (MacBook Pro)
•	VS Code
•	Python 3.9+

Works with Python 3.9+ on Linux/macOS/Windows.

2) Run the program

From the project root:

python3 main.py < sample_input.txt

Expected output (from the challenge statement):

1 1 E
3 3 N LOST
2 3 S

To use your own input, replace sample_input.txt with a file in the same format.

## Testing
Run unit tests:

python3 -m unittest discover -s tests -p "test_*.py"

OR

python3 -m unittest discover -s tests -p "test_mars.py"

OR

python3 -m unittest

## Input format

. Grid definition

- The first line contains the grid’s upper-right coordinates.
- The lower-left corner is always assumed to be (0, 0).

•	Robots

Each robot is described using two lines (with optional blank lines between robots):

1.	Position → X Y O
•	X, Y are integers.
•	O is orientation: one of {N, E, S, W}.

2.	Instructions → a string of commands, each one in {L, R, F}.
•	L = turn left 90°
•	R = turn right 90°
•	F = move forward one cell in the current orientation

## Example
5 3
1 1 E
RFRFRFRF

## LOST & Scent Rule
•	If a forward move would take a robot off the grid, the robot is considered LOST.
•	When this happens, the robot leaves a scent at its last safe position.
•	Any future robot reaching that same cell and facing the same off-grid move will ignore the move and continue executing the rest of its program.

## Design Notes
•	Scent granularity → scents are stored per grid coordinate (not per orientation). This follows the challenge’s wording: “from a grid point.”
•	Extensible commands → new commands can be added by extending Robot.apply(...).
•	Validation → inputs are assumed valid per the spec. If they aren’t, a ValueError is raised immediately (fail fast).
•	Dependencies → none beyond the Python standard library, to keep things easy to run and review.

##  Approach (Implementation Overview)

1. Parse input
•	Read grid size.
•	For each robot, parse starting position + instruction string.
•	Construct a Grid(max_x, max_y) object.

2. Simulate robots sequentially
•	Create a Robot(x, y, orientation) for each robot.
•	Execute its instructions one by one.

3.	Movement & turning
•	Turning uses an orientation ring: "NESW".
•	Movement uses (dx, dy) deltas for each orientation.

4.	Handle off-grid moves
•	If next move goes off the grid, check if the current position is scented.
•	If scented → ignore the move.
•	If not scented → mark robot as LOST, add the scent, stop executing its program.