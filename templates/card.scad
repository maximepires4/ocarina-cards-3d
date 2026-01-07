// Ocarina Learning Card - Font Based
// Dimensions: 70x100mm (Base)

// --- Parameters (Overridden by CLI) ---
note_letter = "C";
note_fr = "Do";
instrument_label = "12-Hole Alto C";
ocarina_font_char = "c"; // Default char
ocarina_font_name = "Ocarina"; // Internal font name
staff_note_position = 0; 
is_sharp = false; // New parameter logic

// Physical overrides (Base values)
base_width = 70;
base_height = 100;
base_thickness = 2.0;
base_relief = 1.0;

// Global Scale Factor
scale_factor = 1.0;

// Colors
color_base = "Blue";
color_relief = "Yellow";

// --- Calculated Constants ---
card_width = base_width * scale_factor;
card_height = base_height * scale_factor;
card_thickness = base_thickness * scale_factor;
relief_thickness = base_relief * scale_factor;
corner_radius = 3.0 * scale_factor;

// Load the font from the project root
use <../assets/fonts/Open-12-Hole-Ocarina-1.ttf>

$fn = 60; 

// --- Modules ---

module rounded_rect(w, h, r, z) {
    linear_extrude(z)
    hull() {
        translate([r, r, 0]) circle(r);
        translate([w-r, r, 0]) circle(r);
        translate([w-r, h-r, 0]) circle(r);
        translate([r, h-r, 0]) circle(r);
    }
}

module base_card() {
    difference() {
        color(color_base) rounded_rect(card_width, card_height, corner_radius, card_thickness);
        // Bind hole (Top Left)
        translate([6 * scale_factor, card_height - (6 * scale_factor), -1]) 
            cylinder(h=card_thickness + 2, d=4 * scale_factor);
    }
}

module text_label(txt, x, y, size, align="center", font="Liberation Sans:style=Bold") {
    translate([x, y, card_thickness])
    linear_extrude(relief_thickness)
    text(txt, size=size * scale_factor, font=font, halign=align, valign="center");
}

module musical_staff(x, y, width) {
    // Robust printable dimensions
    line_thick = 0.8 * scale_factor;
    line_spacing = 3.0 * scale_factor; 
    
    translate([x, y, card_thickness]) {
        // 5 lines
        for(i=[0:4]) {
            translate([0, i*line_spacing, 0])
            cube([width, line_thick, relief_thickness]);
        }
        
        // Note Head
        note_y = (staff_note_position * line_spacing) + (line_thick / 2); 
        
        translate([width/2, note_y, 0])
        cylinder(h=relief_thickness, d=4.0 * scale_factor);
        
        // Stem
        translate([width/2 + (1.5 * scale_factor), note_y, 0])
        cube([1.0 * scale_factor, 10 * scale_factor, relief_thickness]);

        // Sharp Symbol (#) - REMOVED per user request to avoid clashes
        /*
        if (is_sharp) {
            translate([width/2 - (6 * scale_factor), note_y - (3 * scale_factor), 0])
            linear_extrude(relief_thickness)
            text("#", size=8 * scale_factor, font="Liberation Sans:style=Bold", halign="center");
        }
        */
    }
}

module ocarina_diagram() {
    translate([card_width/2, card_height/2 - (5 * scale_factor), card_thickness])
    linear_extrude(relief_thickness)
    // We use the specific ocarina font here
    text(ocarina_font_char, size=40 * scale_factor, font=ocarina_font_name, halign="center", valign="center");
}

// --- Assembly ---

// "all" = Preview colors in OpenSCAD
// "base" = Generate only the card body
// "relief" = Generate only the text/staff/diagram

part_type = "all"; 

if (part_type == "base" || part_type == "all") {
    base_card();
}

if (part_type == "relief" || part_type == "all") {
    // We apply color only if in preview mode ("all")
    // In export mode, color doesn't matter for STL, geometry separation does.
    if (part_type == "all") {
        color(color_relief) content_group();
    } else {
        content_group();
    }
}

module content_group() {
    // Labels
    text_label(note_letter, 10 * scale_factor, card_height - (15 * scale_factor), 10, "left");
    text_label(note_fr, 10 * scale_factor, card_height - (25 * scale_factor), 5, "left");
    text_label(instrument_label, card_width - (10 * scale_factor), 10 * scale_factor, 4, "right");
    
    // Staff
    musical_staff(
        card_width - (30 * scale_factor), 
        card_height - (20 * scale_factor), 
        20 * scale_factor
    );
    
    // Ocarina Diagram
    ocarina_diagram();
}
