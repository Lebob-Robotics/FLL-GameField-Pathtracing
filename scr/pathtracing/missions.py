"""Hardcoded mission positions for FLL Unearthed game field.

Coordinates are grid cells (x, y) on a 70 x 40 grid covering the playing
surface. (0, 0) is top-left, (69, 39) is bottom-right.

FLL Unearthed field is 2362 mm wide x 1143 mm tall.
    cell_x_mm = 2362 / 70 = 33.74
    cell_y_mm = 1143 / 40 = 28.58

Robot launches from the bottom-right (blue) home base, facing north
(toward -y). Lebob's mission groupings are derived from
Projects/Lebob-Unearthed/src/main.py and PathV3-V5 path diagrams in
Projects/Lebob-Unearthed/resources/.

FLL Unearthed (2024-25) official missions referenced below:
    M01 Surface Brushing       M09 Forge
    M02 Careful Recovery       M10 Heavy Lift
    M03 Who Lived Here         M11 Silo
    M04 Forum                  M12 What's On Sale
    M05 Tip the Scales         M13 Send It Over
    M06 Angler Artifacts       M14 Site Marking
    M07 Salvage Operation      M15 Precision Tokens
    M08 Statue Rebuild
"""

GRID_LENGTH = 70
GRID_HEIGHT = 40

FIELD_WIDTH_MM = 2362
FIELD_HEIGHT_MM = 1143

CELL_X_MM = FIELD_WIDTH_MM / GRID_LENGTH
CELL_Y_MM = FIELD_HEIGHT_MM / GRID_HEIGHT

# Bottom-right blue home base, just inside the arc. Robot faces north.
# Grid cell mapping derived from official Map.pdf (10 cols x 6 rows,
# columns A-J, rows 1-6 with row 6 = top, each cell 20 cm).
#   col x: A=3.5  B=10.5 C=17.5 D=24.5 E=31.5
#          F=38.5 G=45.5 H=52.5 I=59.5 J=66.5
#   row y (top=6): 6=3.3  5=10  4=16.7 3=23.3 2=30  1=36.7
HOME_POS = (62, 32)  # I2 area, inside blue arc
HOME_HEADING_DEG = 0

# (mission_id, lebob_grouping_name, (grid_x, grid_y))
# Positions cross-referenced against:
#   - Map.pdf wireframe (Lebob-Unearthed/resources/Map.pdf)
#   - unearthed-gamefield.jpeg photo landmarks
#   - PathV3/PathV5 labels in Lebob-Unearthed/resources/
UNEARTHED_MISSIONS = [
    # Map.pdf I6 cluster: M10 Heavy Lift big red+grey building, top-right.
    # PathV5 labels "Collect heavy lifting".
    ("m1", "Heavy + Rocks (M10)",       (62,  4)),

    # Map.pdf J5 small upright structure on far right edge = M11 Silo drum.
    ("m2", "Silo (M11)",                (66,  8)),

    # Map.pdf E4/F4 dark structure beside the round disk = M05 Tip the Scales.
    # PathV5 labels "Scale" + "Roof" in this region.
    ("m3", "Scales + Pan (M05)",        (35, 16)),

    # Map.pdf G4 white ship-shaped structure = M07 Salvage Operation.
    ("m4", "Ship (M07)",                (45, 14)),

    # Map.pdf A6/B6 top-left cluster = M01 Surface Brushing + map figurine.
    # PathV5 labels "Collect Map" + "Collect Brush".
    ("m5", "Brush + Map (M01)",         ( 5,  3)),

    # Map.pdf D6/E6 top-center cart-on-track structure = M02 Careful Recovery.
    # PathV5 labels "Careful recovery + Minecart" at top-center.
    ("m6", "Minecart (M02)",            (24,  4)),

    # Map.pdf C4/D4 round oval = M04 Forum (6-column scoring disk).
    # PathV5 labels "6 Items in forum". Lebob bundles Statue (A3) + Flags.
    ("m7", "Forum + Statue (M04+M08)",  (18, 16)),
]

MISSIONS_BY_FIELD = {
    "unearthed": UNEARTHED_MISSIONS,
    "submerged": [],
}
