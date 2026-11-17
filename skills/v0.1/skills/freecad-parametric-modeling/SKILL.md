---
name: freecad-parametric-modeling
description: Use when creating or editing parametric FreeCAD parts with Sketcher, PartDesign, expressions, patterns, holes, cutouts, booleans, datum references, or reproducible engineering dimensions.
---
# FreeCAD Parametric Modeling (Builder only, v0.1)

## Method
Model **design intent** rather than only shape appearance. A shape that looks right after one build is not sufficient: it must recompute, save and survive expected parameter edits.

## Workflow
1. Parse user constraints: dimensions, units, design relationships, fit, manufacturing process and unknowns. Do not invent tolerances/material standards.
2. Choose parametric feature strategy: for a single connected engineered part prefer `PartDesign::Body` + `Sketcher` + Pad/Pocket and datum-plane based references. Use direct `Part` primitives/booleans for bounded quick prototypes when editable feature history is not required or to combine separate solids intentionally.
3. Pick a stable coordinate system and reference planes. Prefer origin planes, datum geometry and expressions over hard-coded `Face1`/`Edge5` references on generated geometry.
4. For sketches: meaningful horizontal/vertical/coincident/tangent/equal/dimensional constraints; check solver for redundant or conflicting constraints and remaining DoF. Do not apply `Block`/`Fix` everywhere to fake design intent.
5. Before any geometric mutation create valid **before checkpoint** in the canonical project root. If this fails, stop.
6. Build one meaningful stage at a time; `doc.recompute()`, inspect output (`Shape.isValid`, number of solids, volume, BoundingBox), and compare against expected material change.
7. For cuts/pockets verify that **some material was actually removed**; for fuses/pads ensure no unexpected detached solids. Avoid returning success on a cut that missed the model.
8. Check parameterization, dependency links, feature errors, spatial relationships and export constraints. If tests require risky perturbation/reopening, use isolated copies rather than altering the user's live document.
9. Create **after checkpoint**, explicitly save the intended working FCStd, export requested formats, update project state, hand evidence to Reviewer.

## Tool reality
The installed Bridge exposes only `execute_python_mcp_freecad`, `get_output_page_mcp_freecad` to the agents (runtime assignment must be rechecked). It does not expose FreeCAD AI's `create_sketch`, `pad_sketch`, `pocket_sketch` or CADPilot's `cad` operations. Implement using the real installed FreeCAD Python API, not foreign MCP names.

## Recovery
- If intermediate shape is invalid, do not forge an after PASS. Preserve live state and checkpoint evidence, report the failing operation, and stop before new changes.
- Do not close the source document to test file reopening.
- Do not use network, shell, package installation, FreeCAD preferences, or project paths outside the canonical workspace.

See [references/stability-and-testing.md](references/stability-and-testing.md).
