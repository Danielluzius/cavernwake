"""Extracts the room/position graph from assets/world/logic-map.png and
prints ready-to-paste text blocks: the Sass $positions map, the HTML
position radio inputs, and the HTML direction-button edge labels.

The map is a clean, non-anti-aliased 32px-tile schematic: every tile is
one of five flat legend colors, or fully transparent (no tile / not
part of the map yet).

Legend:
  white  (255,255,255) = room floor
  green  (34,177,76)   = character standing point ("position" node)
  purple (163,73,164)  = walkable connector (normal exit)
  orange (255,127,39)  = elevator connector
  yellow (255,242,0)   = ladder connector

Not part of the build pipeline — a one-off data-extraction tool, re-run by
hand whenever logic-map.png changes; its output is pasted by hand into
scss/base/_graph.scss and html/partials/position-radios.html,
edge-radios.html, and direction-edge-buttons.html.
"""

from pathlib import Path

from PIL import Image

TILE = 32

LEGEND = {
    (255, 255, 255, 255): "room",
    (34, 177, 76, 255): "green",
    (163, 73, 164, 255): "purple",
    (255, 127, 39, 255): "orange",
    (255, 242, 0, 255): "yellow",
}

CONNECTOR_KINDS = {"purple": "walk", "orange": "elevator", "yellow": "ladder"}

DIRECTIONS = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}

ARROWS = {"up": "▲", "right": "▶", "down": "▼", "left": "◀"}


def classify(img, col, row):
    px = img.getpixel((col * TILE + TILE // 2, row * TILE + TILE // 2))
    return LEGEND.get(px)


def build_graph():
    path = Path(__file__).resolve().parent.parent / "assets" / "world" / "logic-map.png"
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    cols, rows = width // TILE, height // TILE

    grid = [[classify(img, c, r) for c in range(cols)] for r in range(rows)]

    greens = [
        (c, r) for r in range(rows) for c in range(cols) if grid[r][c] == "green"
    ]

    def trace(c, r, dc, dr):
        kind = None
        c, r = c + dc, r + dr
        while 0 <= c < cols and 0 <= r < rows:
            cell = grid[r][c]
            if cell == "green":
                return (c, r), (kind or "walk")
            if cell in CONNECTOR_KINDS:
                found = CONNECTOR_KINDS[cell]
                if kind is None or found != "walk":
                    kind = found
                c, r = c + dc, r + dr
                continue
            return None
        return None

    nodes = {
        (c, r): idx
        for idx, (c, r) in enumerate(sorted(greens, key=lambda p: (p[1], p[0])), start=1)
    }

    result = {}
    for (c, r), idx in nodes.items():
        exits = {}
        for direction, (dc, dr) in DIRECTIONS.items():
            hit = trace(c, r, dc, dr)
            if hit:
                target_pos, kind = hit
                target_idx = nodes.get(target_pos)
                if target_idx:
                    exits[direction] = {"to": target_idx, "kind": kind}
        result[idx] = {"col": c, "row": r, "exits": exits}
    return result


def print_scss(graph):
    print("$positions: (")
    for idx in sorted(graph):
        node = graph[idx]
        exits = node["exits"]
        exits_str = ", ".join(
            f"{d}: (to: {e['to']}, kind: {e['kind']})" for d, e in exits.items()
        )
        print(f"  {idx}: (col: {node['col']}, row: {node['row']}, exits: ({exits_str})),")
    print(");")


def print_html_inputs(graph):
    for idx in sorted(graph):
        checked = " checked" if idx == 1 else ""
        print(
            f'    <input type="radio" name="position" id="position-{idx}" '
            f'class="world-position-input"{checked} />'
        )


def print_html_facing_inputs(graph):
    # One extra radio per edge (position-<to>--from-<source>), unchecked —
    # lets the player sprite face the direction of the button actually
    # clicked (see player/_player.scss), instead of always the plain
    # position-<to> id which can be reached from several directions.
    for idx in sorted(graph):
        for _direction, exit_ in graph[idx]["exits"].items():
            print(
                f'    <input type="radio" name="position" '
                f'id="position-{exit_["to"]}--from-{idx}" '
                f'class="world-position-input" />'
            )


def print_html_labels(graph):
    for idx in sorted(graph):
        for direction, exit_ in graph[idx]["exits"].items():
            arrow = ARROWS[direction]
            print(
                f'                    <label class="direction-controls__button '
                f'direction-controls__button--{direction} direction-controls__button--edge" '
                f'data-position="{idx}" for="position-{exit_["to"]}--from-{idx}">{arrow}</label>'
            )


if __name__ == "__main__":
    graph = build_graph()
    print(f"-- {len(graph)} nodes --\n")
    print("---- SCSS ($positions) ----")
    print_scss(graph)
    print("\n---- HTML (position inputs) ----")
    print_html_inputs(graph)
    print("\n---- HTML (facing inputs) ----")
    print_html_facing_inputs(graph)
    print("\n---- HTML (edge labels) ----")
    print_html_labels(graph)

