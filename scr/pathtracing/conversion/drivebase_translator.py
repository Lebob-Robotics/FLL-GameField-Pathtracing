"""Convert an A* grid path into Lebob LebobDriveBase commands.

Compresses consecutive same-direction grid cells into one drive segment,
emits turn-then-straight pairs.
"""

import math

from pathtracing.missions import CELL_X_MM, CELL_Y_MM


def _direction(p1, p2):
    """Compass heading in degrees from p1 to p2 in grid space.

    0 deg = north (-y), positive = clockwise (matches Lebob db.turn convention
    where positive turn_rate turns right).
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # atan2 with -dy because grid y grows downward but we want "up = north".
    return math.degrees(math.atan2(dx, -dy))


def _angle_diff(target_deg, current_deg):
    """Shortest signed angle from current to target, in (-180, 180]."""
    d = (target_deg - current_deg + 180) % 360 - 180
    return d


def _segment_length_mm(p1, p2):
    dx = (p2[0] - p1[0]) * CELL_X_MM
    dy = (p2[1] - p1[1]) * CELL_Y_MM
    return math.hypot(dx, dy)


def compress_path(path):
    """Collapse colinear runs of grid cells into endpoints.

    `path` is the A* output: list of (x, y) ordered start -> end.
    Returns the same list with intermediate colinear points removed.
    """
    if len(path) < 3:
        return list(path)
    out = [path[0]]
    last_dir = _direction(path[0], path[1])
    for i in range(1, len(path) - 1):
        d = _direction(path[i], path[i + 1])
        if abs(_angle_diff(d, last_dir)) > 0.5:
            out.append(path[i])
            last_dir = d
    out.append(path[-1])
    return out


def path_to_commands(path, start_heading_deg=0):
    """Yield (op, value) tuples for a single mission path.

    op in {"turn", "straight"}. value is degrees or millimetres.
    Skips zero-magnitude operations.
    """
    if len(path) < 2:
        return
    waypoints = compress_path(path)
    heading = start_heading_deg
    for a, b in zip(waypoints, waypoints[1:]):
        dist = _segment_length_mm(a, b)
        if dist < 1.0:
            continue
        target = _direction(a, b)
        turn = _angle_diff(target, heading)
        if abs(turn) > 0.5:
            yield ("turn", round(turn, 1))
            heading = target
        yield ("straight", round(dist, 1))


def commands_to_python(commands, indent="    "):
    """Render a list of (op, value) tuples as pybricks db.* calls."""
    lines = []
    for op, value in commands:
        if op == "turn":
            lines.append(f"{indent}db.turn({value})")
        elif op == "straight":
            lines.append(f"{indent}db.straight({value})")
    return "\n".join(lines) if lines else f"{indent}pass"
