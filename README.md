# Ocarina Cards 3D Generator

This project generates **3D printable learning cards for Ocarinas** using OpenSCAD and Python. 
It creates **optimized Multi-Part STL files** designed for seamless multi-color printing.

## Project Structure

*   `assets/fonts/`: Contains the Ocarina TTF fonts.
*   `src/`: Core Python source code.
    *   `main.py`: CLI entry point (`uv run generate-cards`).
    *   `generator.py`: OpenSCAD wrapper logic.
    *   `mapping.json`: User-defined mapping between notes and font characters.
*   `scripts/`: Utility scripts (mapper, cheat sheet).
*   `templates/`: OpenSCAD templates.
*   `output/`: Generated STL files appear here.

## Prerequisites

*   **Python 3.12+**
*   **uv** (Recommended package manager)
*   **OpenSCAD** (Must be in your system PATH)

## Installation & Configuration

1.  **Sync dependencies:**
    ```bash
    uv sync
    ```

2.  **Map your font:**
    ```bash
    uv run scripts/interactive_mapper.py
    ```

## Usage

### Basic Generation
Generates a **Common Base** for the instrument, and separate **Relief** files for each note.

```bash
uv run generate-cards
```

### Testing
*   **Single Card:**
    ```bash
    uv run generate-cards --test
    ```
*   **Full Range Test:**
    ```bash
    uv run generate-cards --test-full
    ```

### Customization
*   **Scaling:** `uv run generate-cards --scale 0.8`
*   **Colors (Preview only):** `uv run generate-cards --color-base "Red"`

## 3D Printing Instructions (Bambu Studio / PrusaSlicer)

The script optimizes generation. For a folder (e.g., `12H_AltoC`), you will see:
1.  `base.stl` (The card body, shared by all notes).
2.  `C.stl`, `D.stl`, etc. (The content/relief).

**To print a specific card (e.g., C Major):**
1.  Open your Slicer.
2.  Select **TWO** files: `base.stl` AND `C.stl`.
3.  Drag and drop them **together** into the Slicer window.
4.  When asked **"Load these files as a single object with multiple parts?"**, click **YES**.
5.  Assign different colors to the parts.
