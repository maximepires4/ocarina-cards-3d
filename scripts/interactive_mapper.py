import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys
import json
from pathlib import Path
from typing import NamedTuple

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "assets" / "fonts" / "Open-12-Hole-Ocarina-1.ttf"
OUTPUT_JSON = BASE_DIR / "src" / "mapping.json"
FONT_SIZE = 100


class NoteTarget(NamedTuple):
    name: str  # Intl Name (e.g. A, C#², etc.)
    fr_name: str  # French Name (e.g. La, Do#², etc.)
    staff_pos: float
    default_char: str


# Helper to build the list
def create_targets():
    # Base pattern (12-Hole Alto C)
    # Range: A4 to F6
    # We map A4, B4 as base. C5-G5 as base. A5-B5 as ². C6-F6 as ².

    raw_data = [
        ("A", "La", -2.0, "a"),
        ("A#", "La#", -2.0, ""),
        ("B", "Si", -1.5, "b"),
        ("C", "Do", -1.0, "c"),
        ("C#", "Do#", -1.0, ""),
        ("D", "Ré", -0.5, "d"),
        ("D#", "Ré#", -0.5, ""),
        ("E", "Mi", 0.0, "e"),
        ("F", "Fa", 0.5, "f"),
        ("F#", "Fa#", 0.5, ""),
        ("G", "Sol", 1.0, "g"),
        ("G#", "Sol#", 1.0, ""),
        ("A²", "La²", 1.5, "h"),
        ("A#²", "La#²", 1.5, ""),
        ("B²", "Si²", 2.0, "i"),
        ("C²", "Do²", 2.5, "j"),
        ("C#²", "Do#²", 2.5, ""),
        ("D²", "Ré²", 3.0, "k"),
        ("D#²", "Ré#²", 3.0, ""),
        ("E²", "Mi²", 3.5, "l"),
        ("F²", "Fa²", 4.0, "m"),
    ]

    targets = []
    for r in raw_data:
        targets.append(NoteTarget(r[0], r[1], r[2], r[3]))
    return targets


NOTES_TO_MAP = create_targets()


class MapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ocarina Font Mapper")
        self.root.geometry("500x600")

        self.current_index = 0
        self.mapping_data = []
        self.current_char = ""

        if not FONT_PATH.exists():
            print(f"Error: Font not found at {FONT_PATH}")
            sys.exit(1)

        try:
            self.pil_font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
        except Exception as e:
            print(f"Error loading font: {e}")
            sys.exit(1)

        # UI Elements
        self.lbl_instruction = tk.Label(
            root, text="Press a key (Backspace to clear)", font=("Arial", 12)
        )
        self.lbl_instruction.pack(pady=10)

        self.lbl_note = tk.Label(root, text="Note...", font=("Arial", 30, "bold"))
        self.lbl_note.pack(pady=5)

        self.lbl_fr = tk.Label(
            root, text="...", font=("Arial", 16, "italic"), fg="gray"
        )
        self.lbl_fr.pack(pady=5)

        self.canvas = tk.Canvas(
            root, width=200, height=200, bg="white", relief="sunken", borderwidth=2
        )
        self.canvas.pack(pady=20)

        self.lbl_char = tk.Label(root, text="Current Key: ", font=("Arial", 14))
        self.lbl_char.pack(pady=5)

        self.btn_next = tk.Button(
            root, text="Confirm & Next (Enter)", command=self.next_note, bg="#dddddd"
        )
        self.btn_next.pack(pady=20, fill="x", padx=50)

        self.root.bind("<Key>", self.on_key)
        self.load_note()

    def load_note(self):
        if self.current_index >= len(NOTES_TO_MAP):
            self.finish()
            return

        target = NOTES_TO_MAP[self.current_index]
        self.lbl_note.config(text=target.name)
        self.lbl_fr.config(text=target.fr_name)

        self.current_char = target.default_char
        self.update_preview()

    def on_key(self, event):
        if event.keysym == "Return":
            self.next_note()
            return

        if event.keysym == "BackSpace" or event.keysym == "Delete":
            self.current_char = ""
            self.update_preview()
            return

        if len(event.char) == 1 and ord(event.char) > 31:
            self.current_char = event.char
            self.update_preview()

    def update_preview(self):
        self.lbl_char.config(text=f"Current Key: '{self.current_char}'")

        img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        bbox = self.pil_font.getbbox(self.current_char)
        if bbox:
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (200 - w) / 2 - bbox[0]
            y = (200 - h) / 2 - bbox[1]
            draw.text((x, y), self.current_char, font=self.pil_font, fill="black")

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(100, 100, image=self.tk_img)

    def next_note(self):
        target = NOTES_TO_MAP[self.current_index]

        entry = {
            "name": target.name,
            "fr_name": target.fr_name,
            "font_char": self.current_char,
            "staff_position": target.staff_pos,
        }
        self.mapping_data.append(entry)

        self.current_char = ""
        self.current_index += 1
        self.load_note()

    def finish(self):
        self.root.destroy()
        try:
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump(self.mapping_data, f, indent=4, ensure_ascii=False)
            print(f"SUCCESS! Mapping saved to: {OUTPUT_JSON}")
        except Exception as e:
            print(f"Error saving JSON: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MapperApp(root)
    root.mainloop()

