# Project 4 — Virtual Museum Room (Blender)

A procedurally generated 3D museum environment built entirely with Blender's Python API.

## What gets created
- A complete museum room — floor, walls, ceiling, skirting boards
- 5 framed paintings on the walls, each with a unique canvas colour and title
- Overhead spotlights aimed precisely at each painting
- Two museum benches in the centre of the room
- A camera set up for a cinematic walkthrough (100-frame animation)
- Render settings pre-configured (Cycles, 1920×1080)

## How to run
1. Open Blender (any version ≥ 3.0)
2. Switch to the **Scripting** workspace (top menu bar)
3. Click **New** to create a new script
4. Paste the contents of `virtual_museum.py`
5. Press **Alt + P** or click the ▶ Run Script button
6. Press **Numpad 0** to enter the camera view
7. Press **F12** to render a still frame

## Controls after running
| Action | Shortcut |
|--------|----------|
| Camera view | Numpad 0 |
| Render still | F12 |
| Play animation | Space (in Timeline) |
| Orbit scene | Middle mouse button |

## Scene overview
```
Museum_Camera        ← cinematic walkthrough camera
Floor / Ceiling      ← room geometry
Wall_Back/Front/Left/Right
Skirting_*           ← decorative trim
Frame_Painting_[1-5] ← wooden frames
Canvas_Painting_[1-5]← coloured canvases
Light_Ambient        ← warm fill light
Spot_Painting_[1-5]  ← gallery spotlights
Bench_[1-2]          ← seating
```

## Tools
Blender 3.x+ · Python (bpy API)
