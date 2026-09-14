"""Generates two permanent, pre-rendered debug overlays derived from
assets/world/logic-map.png, toggled by two independent buttons/checkboxes
(see scss/world/_room.scss):

- assets/world/logic-map-colors.png: just the logic-map's node/connector
  colors (white/green/purple/orange/yellow), resized to display scale, no
  lines/labels. Toggled by the COLORS button.
- assets/world/logic-map-grid.png: just the per-tile grid, room
  boundaries, floor-anchor line, and 0-based column/row number labels, on a
  fully transparent background. Toggled by the GRID button.

Split out of a single combined "logic-map-debug.png" so grid lines and
map colors can be shown/hidden independently while testing.

Replaces the previous CSS-only overlay (repeating-linear-gradient layers +
counter-based label <span> grids in scss/world/_room.scss), which only
rendered the number labels correctly within the very first room segment.

Re-run this script whenever assets/world/logic-map.png changes:
    python scripts/generate_debug_map.py

All measurements mirror scss/base/_variables.scss - keep both in sync.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from extract_positions import build_graph

# --- mirrors scss/base/_variables.scss ---
TILE_SIZE = 32
DISPLAY_SCALE = 2
TILE_SIZE_DISPLAY = TILE_SIZE * DISPLAY_SCALE  # 64
MOVEMENT_TILES_PER_STEP = 3
MOVEMENT_STEP_DISPLAY = TILE_SIZE_DISPLAY * MOVEMENT_TILES_PER_STEP  # 192
DEBUG_GRID_ROWS = 7
ROOM_HEIGHT_DISPLAY = DEBUG_GRID_ROWS * TILE_SIZE_DISPLAY  # 448
ENVIRONMENT_ANCHOR_ROW = 4.5

SOURCE_PATH = Path(__file__).resolve().parent.parent / "assets/world/logic-map.png"
COLORS_OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent / "assets/world/logic-map-colors.png"
)
GRID_OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent / "assets/world/logic-map-grid.png"
)

GRID_LINE_COLOR = (255, 255, 255, 40)
ROOM_LINE_COLOR = (255, 176, 0, 180)
ANCHOR_LINE_COLOR = (0, 170, 255, 230)
LABEL_COLOR = (0, 255, 136, 255)
LABEL_OUTLINE_COLOR = (0, 0, 0, 255)
NODE_LABEL_COLOR = (255, 60, 220, 255)


def load_label_font() -> ImageFont.FreeTypeFont:
    for candidate in ("consola.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(candidate, 16)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_outlined_text(draw: ImageDraw.ImageDraw, xy, text, font, color=LABEL_COLOR) -> None:
    x, y = xy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), text, font=font, fill=LABEL_OUTLINE_COLOR)
    draw.text((x, y), text, font=font, fill=color)


def main() -> None:
    source = Image.open(SOURCE_PATH).convert("RGBA")
    width, height = source.width * DISPLAY_SCALE, source.height * DISPLAY_SCALE
    colors_map = source.resize((width, height), Image.NEAREST)
    colors_map.save(COLORS_OUTPUT_PATH)
    print(f"Wrote {COLORS_OUTPUT_PATH} ({width}x{height})")

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Per-tile grid.
    for x in range(0, width + 1, TILE_SIZE_DISPLAY):
        draw.line([(x, 0), (x, height)], fill=GRID_LINE_COLOR, width=1)
    for y in range(0, height + 1, TILE_SIZE_DISPLAY):
        draw.line([(0, y), (width, y)], fill=GRID_LINE_COLOR, width=1)

    # Room boundaries.
    for x in range(0, width + 1, MOVEMENT_STEP_DISPLAY):
        draw.line([(x, 0), (x, height)], fill=ROOM_LINE_COLOR, width=2)
    for y in range(0, height + 1, ROOM_HEIGHT_DISPLAY):
        draw.line([(0, y), (width, y)], fill=ROOM_LINE_COLOR, width=2)

    # Floor-anchor line, repeated once per room segment.
    anchor_offset = round(ENVIRONMENT_ANCHOR_ROW * TILE_SIZE_DISPLAY)
    for room_top in range(0, height, ROOM_HEIGHT_DISPLAY):
        y = room_top + anchor_offset
        draw.line([(0, y), (width, y)], fill=ANCHOR_LINE_COLOR, width=2)

    # Column / row index labels (0-based, matches col/row in $positions).
    font = load_label_font()
    for col, x in enumerate(range(0, width, TILE_SIZE_DISPLAY)):
        draw_outlined_text(draw, (x + 3, 1), str(col), font)
    for row, y in enumerate(range(0, height, TILE_SIZE_DISPLAY)):
        draw_outlined_text(draw, (1, y + 1), str(row), font)

    # Position-node ids ($positions in base/_variables.scss), centered on
    # each green standing-point tile, for cross-referencing coordinates in
    # conversation without having to count tiles by hand.
    node_font = load_label_font()
    for idx, node in build_graph().items():
        x = node["col"] * TILE_SIZE_DISPLAY
        y = node["row"] * TILE_SIZE_DISPLAY
        draw_outlined_text(
            draw, (x + 4, y + TILE_SIZE_DISPLAY // 2 - 8), str(idx), node_font, NODE_LABEL_COLOR
        )

    overlay.save(GRID_OUTPUT_PATH)
    print(f"Wrote {GRID_OUTPUT_PATH} ({width}x{height})")


if __name__ == "__main__":
    main()
