import typer
from pathlib import Path
from rich.console import Console
from rich.progress import track

from src.data import get_all_variants
from src.generator import generate_card, is_openscad_installed

app = typer.Typer()
console = Console()


@app.command()
def generate(
    output_dir: Path = Path("output"),
    template_path: Path = Path("templates/card.scad"),
    width: float = typer.Option(70.0, help="Base card width in mm"),
    height: float = typer.Option(100.0, help="Base card height in mm"),
    thickness: float = typer.Option(2.0, help="Base card thickness in mm"),
    relief: float = typer.Option(1.0, help="Base relief thickness in mm"),
    scale: float = typer.Option(
        1.0, help="Global scaling factor (multiplies all dimensions)"
    ),
    color_base: str = typer.Option("Blue", help="Color of the card base"),
    color_relief: str = typer.Option("Yellow", help="Color of the text and relief"),
    test: bool = typer.Option(
        False, "--test", "-t", help="Generate only the first card for testing"
    ),
    test_full: bool = typer.Option(
        False,
        "--test-full",
        help="Generate 4 representative cards (Natural, Sharp, High, High Sharp)",
    ),
):
    """
    Generates 3D printable Ocarina cards using a font for the diagrams.
    Generates a single Common Base per instrument, and separate Relief files for each note.
    """
    if not is_openscad_installed():
        console.print(
            "[bold red]Error:[/bold red] OpenSCAD is not installed or not in PATH."
        )
        raise typer.Exit(code=1)

    if not template_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] Template not found at {template_path}"
        )
        raise typer.Exit(code=1)

    variants = get_all_variants()

    tasks = []
    for variant in variants:
        for note in variant.notes:
            tasks.append({"variant": variant, "note": note})

    console.print(f"Found [bold green]{len(tasks)}[/bold green] potential cards.")
    if scale != 1.0:
        console.print(
            f"[blue]Info:[/blue] Applying scale factor x{scale} (Final Size: {width * scale:.1f}x{height * scale:.1f}mm)"
        )

    valid_tasks = [t for t in tasks if t["note"].font_char]

    if test_full:
        console.print(
            "[yellow]TEST FULL MODE:[/yellow] Generating 4 representative cards."
        )
        examples = []
        found = {"normal": False, "sharp": False, "high": False, "high_sharp": False}

        for task in valid_tasks:
            name = task["note"].name
            is_sharp = "#" in name
            is_high = "²" in name

            if not is_sharp and not is_high and not found["normal"]:
                examples.append(task)
                found["normal"] = True
            elif is_sharp and not is_high and not found["sharp"]:
                examples.append(task)
                found["sharp"] = True
            elif not is_sharp and is_high and not found["high"]:
                examples.append(task)
                found["high"] = True
            elif is_sharp and is_high and not found["high_sharp"]:
                examples.append(task)
                found["high_sharp"] = True

            if all(found.values()):
                break
        tasks = examples

    elif test:
        console.print("[yellow]TEST MODE:[/yellow] Generating only A#² card.")
        # Try to find A#²
        specific_task = [t for t in valid_tasks if t["note"].name == "A#²"]
        if specific_task:
            tasks = [specific_task[0]]
        elif valid_tasks:
            console.print("[bold red]Warning:[/bold red] A#² not found, falling back to first available card.")
            tasks = [valid_tasks[0]]
        else:
            tasks = []

    # --- Phase 1: Identify required Variants (Folders) ---
    # We need to generate the Base STL once for each variant involved in the tasks
    active_variants = {t["variant"].id: t["variant"] for t in tasks}

    for var_id, variant in active_variants.items():
        base_filename = "base.stl"
        base_path = output_dir / var_id / base_filename

        console.print(f"Generating Base for {variant.label}...")

        # We use dummy note data for the base, it doesn't affect geometry
        generate_card(
            template_path=template_path,
            output_path=base_path,
            note_letter="C",
            note_fr="Do",
            instrument_label=variant.label,
            font_char="c",
            font_name=variant.font_name,
            staff_pos=0,
            width=width,
            height=height,
            thickness=thickness,
            relief=relief,
            scale=scale,
            color_base=color_base,
            color_relief=color_relief,
            part_type="base",
        )

    # --- Phase 2: Generate Reliefs ---
    for task in track(tasks, description="Generating Relief STLs..."):
        variant = task["variant"]
        note = task["note"]

        folder_name = variant.id
        safe_name = note.name.replace("#", "_sharp").replace("²", "_high")

        file_relief = output_dir / folder_name / f"{safe_name}.stl"

        generate_card(
            template_path=template_path,
            output_path=file_relief,
            note_letter=note.name,
            note_fr=note.fr_name,
            instrument_label=variant.label,
            font_char=note.font_char,
            font_name=variant.font_name,
            staff_pos=note.staff_position,
            width=width,
            height=height,
            thickness=thickness,
            relief=relief,
            scale=scale,
            color_base=color_base,
            color_relief=color_relief,
            part_type="relief",
        )

    console.print(
        f"[bold green]Success![/bold green] Generated {len(tasks)} relief files + Common Bases in {output_dir}"
    )


if __name__ == "__main__":
    app()

