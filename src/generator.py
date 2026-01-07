import subprocess
import shutil
from pathlib import Path
from typing import Any


def is_openscad_installed() -> bool:
    return shutil.which("openscad") is not None


def format_openscad_value(value: Any) -> str:
    """Formats a Python value into an OpenSCAD string literal."""
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def generate_card(
    template_path: Path,
    output_path: Path,
    note_letter: str,
    note_fr: str,
    instrument_label: str,
    font_char: str,
    font_name: str,
    staff_pos: float,
    # Physical dimensions (BASE)
    width: float = 70.0,
    height: float = 100.0,
    thickness: float = 2.0,
    relief: float = 1.0,
    scale: float = 1.0,
    # Colors
    color_base: str = "Blue",
    color_relief: str = "Yellow",
    # Part selection
    part_type: str = "all",
):
    """
    Generates an STL file using OpenSCAD.
    """

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Prepare Defines
    defines = {
        "note_letter": note_letter,
        "note_fr": note_fr,
        "instrument_label": instrument_label,
        "ocarina_font_char": font_char,
        "ocarina_font_name": font_name,
        "staff_note_position": staff_pos,
        # Physical overrides
        "base_width": width,
        "base_height": height,
        "base_thickness": thickness,
        "base_relief": relief,
        "scale_factor": scale,
        # Colors
        "color_base": color_base,
        "color_relief": color_relief,
        # Music logic
        "is_sharp": "#" in note_letter,
        # Geometry split
        "part_type": part_type,
    }

    cmd = ["openscad", "-o", str(output_path)]

    for key, value in defines.items():
        cmd.append("-D")
        cmd.append(f"{key}={format_openscad_value(value)}")

    cmd.append(str(template_path))

    # Run OpenSCAD
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating {output_path}:")
        print(e.stderr)
        raise e

