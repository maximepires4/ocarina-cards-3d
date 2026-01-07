from PIL import Image, ImageDraw, ImageFont
import sys
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "assets" / "fonts" / "Open-12-Hole-Ocarina-1.ttf"
OUTPUT_IMG = BASE_DIR / "font_cheat_sheet.png"
FONT_SIZE = 40
GRID_COLS = 16
CELL_SIZE = 60


def generate_sheet():
    if not FONT_PATH.exists():
        print(f"Error: Font not found at {FONT_PATH}")
        sys.exit(1)

    try:
        font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
        label_font = ImageFont.load_default()
    except Exception as e:
        print(f"Error loading font: {e}")
        sys.exit(1)

    # Prepare image
    chars_to_print = [chr(i) for i in range(33, 127)]

    rows = (len(chars_to_print) // GRID_COLS) + 1
    width = GRID_COLS * CELL_SIZE
    height = rows * CELL_SIZE

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for idx, char in enumerate(chars_to_print):
        row = idx // GRID_COLS
        col = idx % GRID_COLS

        x = col * CELL_SIZE
        y = row * CELL_SIZE

        # Draw the Glyph (Ocarina)
        draw.text((x + 10, y + 20), char, font=font, fill="black")

        # Draw the Key (Small Label)
        draw.text((x + 5, y + 5), char, font=label_font, fill="blue")

        # Draw Grid box
        draw.rectangle([x, y, x + CELL_SIZE, y + CELL_SIZE], outline="#ddd")

    print(f"Generating cheat sheet with {len(chars_to_print)} characters...")
    img.save(OUTPUT_IMG)
    print(f"Saved to: {OUTPUT_IMG}")


if __name__ == "__main__":
    generate_sheet()
