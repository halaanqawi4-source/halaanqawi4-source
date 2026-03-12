"""
Virtual Museum Room — Blender Python Script
============================================
Author : Hala Anqawi
Tool   : Blender (Python API / bpy)

How to run:
  1. Open Blender
  2. Go to Scripting workspace (top tab)
  3. Click "New" to create a new script
  4. Paste this entire file
  5. Click "Run Script" (▶ button) or press Alt+P
  6. The scene will be built automatically in about 5–10 seconds

What gets created:
  - A complete museum room (floor, walls, ceiling, skirting boards)
  - 5 framed paintings on the walls with coloured canvases
  - Overhead spotlights aimed at each painting
  - A warm ambient fill light + skylight
  - A camera set up for a cinematic walkthrough angle
  - All objects named clearly in the outliner

After running:
  - Press Numpad 0 to see the camera view
  - Press F12 to render a still frame
  - Use Timeline (Space) to preview camera animation (100 frames)
"""

import bpy
import math
from mathutils import Vector, Color

# ─────────────────────────────────────────────
#  SETUP — clear default scene
# ─────────────────────────────────────────────
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

# ─────────────────────────────────────────────
#  MATERIAL HELPERS
# ─────────────────────────────────────────────
def make_material(name, color, roughness=0.8, metallic=0.0, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value  = roughness
    bsdf.inputs["Metallic"].default_value   = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value  = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 2.0
    return mat

def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# ─────────────────────────────────────────────
#  OBJECT HELPERS
# ─────────────────────────────────────────────
def add_box(name, location, scale, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if mat:
        assign_material(obj, mat)
    return obj

def add_plane(name, location, scale, rotation=(0,0,0), mat=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rotation
    if mat:
        assign_material(obj, mat)
    return obj

# ─────────────────────────────────────────────
#  ROOM DIMENSIONS
# ─────────────────────────────────────────────
ROOM_W = 12.0   # X  width
ROOM_D = 9.0    # Y  depth
ROOM_H = 4.0    # Z  height
T      = 0.15   # wall thickness

# ─────────────────────────────────────────────
#  1. ROOM GEOMETRY
# ─────────────────────────────────────────────
def build_room():
    # Materials
    mat_floor   = make_material("Floor_Parquet",  (0.55, 0.38, 0.22), roughness=0.6)
    mat_wall    = make_material("Wall_Plaster",   (0.94, 0.91, 0.86), roughness=0.95)
    mat_ceiling = make_material("Ceiling",        (0.97, 0.96, 0.93), roughness=1.0)
    mat_skirting= make_material("Skirting",       (0.85, 0.82, 0.76), roughness=0.7)

    # Floor
    add_plane("Floor", (0, 0, 0), (ROOM_W, ROOM_D, 1), mat=mat_floor)

    # Ceiling
    add_plane("Ceiling", (0, 0, ROOM_H),
              (ROOM_W, ROOM_D, 1), rotation=(math.pi, 0, 0), mat=mat_ceiling)

    # Back wall  (far Y)
    add_box("Wall_Back",
            (0, ROOM_D/2 + T/2, ROOM_H/2),
            (ROOM_W, T, ROOM_H), mat=mat_wall)

    # Front wall (near Y) — with gap for entrance feel
    add_box("Wall_Front",
            (0, -ROOM_D/2 - T/2, ROOM_H/2),
            (ROOM_W, T, ROOM_H), mat=mat_wall)

    # Left wall
    add_box("Wall_Left",
            (-ROOM_W/2 - T/2, 0, ROOM_H/2),
            (T, ROOM_D + T*2, ROOM_H), mat=mat_wall)

    # Right wall
    add_box("Wall_Right",
            ( ROOM_W/2 + T/2, 0, ROOM_H/2),
            (T, ROOM_D + T*2, ROOM_H), mat=mat_wall)

    # Skirting boards (decorative base trim)
    for name, loc, sc in [
        ("Skirting_Back",  (0, ROOM_D/2 - 0.08,    0.08), (ROOM_W, 0.04, 0.16)),
        ("Skirting_Front", (0, -ROOM_D/2 + 0.08,   0.08), (ROOM_W, 0.04, 0.16)),
        ("Skirting_Left",  (-ROOM_W/2 + 0.08, 0,   0.08), (0.04, ROOM_D, 0.16)),
        ("Skirting_Right", ( ROOM_W/2 - 0.08, 0,   0.08), (0.04, ROOM_D, 0.16)),
    ]:
        add_box(name, loc, sc, mat=mat_skirting)

    print("  ✓ Room built")

# ─────────────────────────────────────────────
#  2. PAINTINGS
# ─────────────────────────────────────────────
PAINTINGS = [
    # name            canvas_color           x     wall   height  title
    ("Painting_1",  (0.12, 0.28, 0.55),    -4.0,  "back",  2.0,  "The Open Sea"),
    ("Painting_2",  (0.72, 0.18, 0.14),     0.0,  "back",  2.0,  "Memory in Red"),
    ("Painting_3",  (0.22, 0.52, 0.28),     4.0,  "back",  2.0,  "Garden of Thought"),
    ("Painting_4",  (0.62, 0.44, 0.16),    -2.5,  "left",  2.0,  "Golden Afternoon"),
    ("Painting_5",  (0.30, 0.22, 0.44),     2.5,  "right", 2.0,  "Violet Hours"),
]

def build_paintings():
    mat_frame = make_material("Frame_Wood", (0.30, 0.20, 0.08), roughness=0.5, metallic=0.05)

    for p_name, canvas_col, x_or_side, wall, z, title in PAINTINGS:
        mat_canvas = make_material(f"Canvas_{p_name}", canvas_col, roughness=0.9)

        W, H = 1.6, 1.1   # painting dimensions
        D_frame = 0.06     # frame depth
        margin  = 0.07     # frame margin around canvas

        if wall == "back":
            # Against back wall
            y_wall = ROOM_D/2 - T - 0.02
            frame_loc   = (x_or_side, y_wall,            z)
            canvas_loc  = (x_or_side, y_wall - 0.02,    z)
            frame_sc    = (W + margin*2, D_frame, H + margin*2)
            canvas_sc   = (W,           0.01,    H)
            frame_rot   = (math.pi/2, 0, 0)
            canvas_rot  = (math.pi/2, 0, 0)

        elif wall == "left":
            x_wall = -ROOM_W/2 + T + 0.02
            frame_loc   = (x_wall,            x_or_side, z)
            canvas_loc  = (x_wall + 0.02,     x_or_side, z)
            frame_sc    = (D_frame, W + margin*2, H + margin*2)
            canvas_sc   = (0.01,   W,             H)
            frame_rot   = (math.pi/2, 0, 0)
            canvas_rot  = (math.pi/2, 0, 0)

        elif wall == "right":
            x_wall = ROOM_W/2 - T - 0.02
            frame_loc   = (x_wall,            x_or_side, z)
            canvas_loc  = (x_wall - 0.02,     x_or_side, z)
            frame_sc    = (D_frame, W + margin*2, H + margin*2)
            canvas_sc   = (0.01,   W,             H)
            frame_rot   = (math.pi/2, 0, 0)
            canvas_rot  = (math.pi/2, 0, 0)

        # Frame
        add_box(f"Frame_{p_name}", frame_loc, frame_sc, mat=mat_frame)
        # Canvas
        add_box(f"Canvas_{p_name}", canvas_loc, canvas_sc, mat=mat_canvas)

    print("  ✓ Paintings placed")

# ─────────────────────────────────────────────
#  3. MUSEUM BENCHES
# ─────────────────────────────────────────────
def build_benches():
    mat_bench = make_material("Bench_Wood", (0.28, 0.18, 0.10), roughness=0.55)
    mat_metal = make_material("Bench_Metal",(0.55, 0.55, 0.55), roughness=0.3, metallic=0.8)

    bench_configs = [
        ("Bench_1", (0, -1.0, 0.22)),
        ("Bench_2", (0,  1.5, 0.22)),
    ]
    for name, loc in bench_configs:
        # Seat
        add_box(f"{name}_Seat", loc, (1.8, 0.45, 0.08), mat=mat_bench)
        # Legs
        for lx in [-0.75, 0.75]:
            add_box(f"{name}_Leg_{lx}",
                    (loc[0]+lx, loc[1], loc[2]-0.22),
                    (0.06, 0.40, 0.38), mat=mat_metal)

    print("  ✓ Benches added")

# ─────────────────────────────────────────────
#  4. LIGHTING
# ─────────────────────────────────────────────
def build_lighting():
    # Ambient fill (soft, warm)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, ROOM_H - 0.1))
    ambient = bpy.context.active_object
    ambient.name = "Light_Ambient"
    ambient.data.energy  = 120
    ambient.data.size    = 8.0
    ambient.data.color   = (1.0, 0.95, 0.85)
    ambient.rotation_euler = (math.pi, 0, 0)

    # Spotlight per painting
    spot_configs = [
        ("Spot_Painting_1", (-4.0,  ROOM_D/2 - 1.5, ROOM_H - 0.3), (-0.4,  0,  0)),
        ("Spot_Painting_2", ( 0.0,  ROOM_D/2 - 1.5, ROOM_H - 0.3), (-0.4,  0,  0)),
        ("Spot_Painting_3", ( 4.0,  ROOM_D/2 - 1.5, ROOM_H - 0.3), (-0.4,  0,  0)),
        ("Spot_Painting_4", (-ROOM_W/2 + 1.2, -2.5, ROOM_H - 0.3), ( 0,  0.4, math.pi/2)),
        ("Spot_Painting_5", ( ROOM_W/2 - 1.2,  2.5, ROOM_H - 0.3), ( 0, -0.4,-math.pi/2)),
    ]
    for s_name, s_loc, s_rot in spot_configs:
        bpy.ops.object.light_add(type='SPOT', location=s_loc)
        spot = bpy.context.active_object
        spot.name = s_name
        spot.data.energy      = 350
        spot.data.spot_size   = math.radians(35)
        spot.data.spot_blend  = 0.25
        spot.data.color       = (1.0, 0.97, 0.88)
        spot.rotation_euler   = s_rot

    print("  ✓ Lighting set up")

# ─────────────────────────────────────────────
#  5. CAMERA + ANIMATION
# ─────────────────────────────────────────────
def build_camera():
    bpy.ops.object.camera_add(location=(0, -ROOM_D/2 + 1.2, 1.7))
    cam = bpy.context.active_object
    cam.name = "Museum_Camera"
    cam.rotation_euler = (math.radians(85), 0, 0)
    cam.data.lens = 28   # slightly wide, cinematic

    bpy.context.scene.camera = cam

    # Animate: slow walk toward the back wall over 100 frames
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end   = 100

    cam.location = (0, -ROOM_D/2 + 1.2, 1.7)
    cam.keyframe_insert(data_path="location", frame=1)

    cam.location = (0, ROOM_D/2 - 2.0, 1.7)
    cam.keyframe_insert(data_path="location", frame=100)

    print("  ✓ Camera and animation ready (100 frames)")

# ─────────────────────────────────────────────
#  6. RENDER SETTINGS
# ─────────────────────────────────────────────
def set_render_settings():
    scene = bpy.context.scene
    scene.render.engine               = 'CYCLES'
    scene.cycles.samples              = 128
    scene.render.resolution_x        = 1920
    scene.render.resolution_y        = 1080
    scene.render.film_transparent     = False

    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value   = (0.05, 0.05, 0.06, 1.0)
    bg.inputs["Strength"].default_value = 0.1

    print("  ✓ Render settings: Cycles 1920×1080, 128 samples")

# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
print("\n── Building Virtual Museum Room ─────────────────")
clear_scene()
build_room()
build_paintings()
build_benches()
build_lighting()
build_camera()
set_render_settings()
print("── Done. Press Numpad 0 for camera view. ────────\n")
print("  Objects created:")
for obj in bpy.context.scene.objects:
    print(f"    • {obj.name}")
