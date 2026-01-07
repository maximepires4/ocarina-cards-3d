from typing import List, NamedTuple
import json
from pathlib import Path


class Note(NamedTuple):
    name: str  # International Name (e.g., "C", "F#")
    fr_name: str  # French Name (e.g., "Do", "Fa#")
    font_char: str  # The character in the font that represents this fingering
    staff_position: float  # 0=Bottom Line (E4 usually), 0.5=Space, 1=Line, etc.


class OcarinaDefinition(NamedTuple):
    id: str  # Unique ID for folder generation (e.g., "12H_AltoC")
    label: str  # Display name on card (e.g., "12-Hole Alto C")
    font_name: str  # The internal name of the font (e.g., "OcarinaFont")
    notes: List[Note]  # List of notes with their corresponding font characters


def load_mapping_from_json() -> List[Note]:
    """Loads note mapping from src/mapping.json if it exists."""
    mapping_path = Path(__file__).parent / "mapping.json"
    notes = []

    if mapping_path.exists():
        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    notes.append(
                        Note(
                            name=item["name"],
                            fr_name=item["fr_name"],
                            font_char=item["font_char"],
                            staff_position=item["staff_position"],
                        )
                    )
            return notes
        except Exception as e:
            print(f"Warning: Failed to load mapping.json: {e}")
            return []
    else:
        return []


# Try to load from JSON first
loaded_notes = load_mapping_from_json()

if loaded_notes:
    NOTES_12H_ALTOC = loaded_notes
else:
    # Fallback default if no mapping generated yet
    NOTES_12H_ALTOC = [
        Note("C", "Do", "c", -1.0),
    ]

OCARINA_LIBRARY: List[OcarinaDefinition] = [
    OcarinaDefinition(
        id="12H_AltoC",
        label="12-Hole Alto C",
        font_name="Open 12 Hole Ocarina 1",
        notes=NOTES_12H_ALTOC,
    ),
]


def get_all_variants() -> List[OcarinaDefinition]:
    return OCARINA_LIBRARY

