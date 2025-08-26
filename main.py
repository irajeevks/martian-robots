import sys
from mars import parse_input, simulate, format_output, Grid

def main() -> int:
    data = sys.stdin.read().splitlines()
    grid, jobs = parse_input(data)
    out_lines = []
    for start, program in jobs:
        bot = simulate(grid, start, program)
        out_lines.append(format_output(bot))
    sys.stdout.write("\n".join(out_lines) + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
