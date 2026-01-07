// Ocarina Font Mapper
// Usage: Open this in OpenSCAD to see which keyboard character maps to which Ocarina finger chart.

use <../assets/fonts/Open-12-Hole-Ocarina-1.ttf>

font_name = "Open 12 Hole Ocarina 1";
rows = 10;
cols = 12;
spacing_x = 25;
spacing_y = 35;

// Generate a grid of characters from ASCII 33 (!) to 126 (~)
translate([-10, 20, 0]) text("Ocarina Font Mapping", size=10);

for(i = [0 : 93]) {
    val = i + 33; // Start at '!'
    char_str = chr(val);
    
    col = i % cols;
    row = floor(i / cols);
    
    x = col * spacing_x;
    y = -row * spacing_y;
    
    translate([x, y, 0]) {
        // 1. The Key to press (Standard Font)
        color("Black")
        translate([0, 10, 0])
        text(char_str, size=6, font="Liberation Sans:style=Bold", halign="center");
        
        // 2. The Resulting Symbol (Ocarina Font)
        color("Blue")
        text(char_str, size=12, font=font_name, halign="center");
        
        // Grid marker for clarity
        %translate([-10, -5, -1]) cube([20, 25, 0.1]);
    }
}
