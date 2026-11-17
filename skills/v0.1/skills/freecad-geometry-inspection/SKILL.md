---
name: freecad-geometry-inspection
description: Use for read-only analysis of FreeCAD objects, bounding boxes, volumes, placements, sketches, constraints, feature-tree dependencies, shape validity, or discrepancies with requested dimensions.
---
# FreeCAD Inspection & Geometry Analysis (Analyst only, v0.1)

## Read-only contract
Use `execute_python_mcp_freecad` for **inspection only**; do not create/open/close/save/recompute a document or edit a property, expression, shape, placement or selection. Never perform a `checkpoint`. Do not use arbitrary subprocesses, sockets or shell. You cannot rely on the current Python MCP tool to technically enforce read-only access; obey this explicitly.

## Inspection protocol
1. Identify the exact document, internal name, `FileName`, and related project revision. If identity is ambiguous, stop.
2. List objects with `Name`, `Label`, `TypeId`, visibility (if accessible), and design dependencies (`InList`, `OutList`).
3. For selected shape-bearing objects: measure `BoundBox`, `Volume`, `Area`, numbers of Solids/Shells/Faces/Edges/Vertexes and `Shape.isValid()`.
4. Inspect Placement and units; do not assume mm for arbitrary imported files unless checked.
5. For sketches: enumerate geometry/constraint metadata, solver status, current degrees of freedom if available in that FreeCAD build. Do not infer 'fully constrained' from a picture.
6. Compare actual measurements with stated design requirements. For tolerance checks use a **specified tolerance**; otherwise report numerical deviations without inventing acceptance thresholds.
7. Report stale or unsaved state, missing objects, invalid shape, suspicious zero-volume outputs, broken dependencies and unsupported introspection.

## Evidence
Data are read from the actual FreeCAD document, not from Builder summaries. For each issue name affected document/object/feature, observed value, expected value, units and whether it is confirmed vs suspected.

## Technical notes
- `Shape.isValid()` is a useful signal, not a universal truth oracle; ambiguous cases warrant additional checking and Reviewer escalation.
- Non-empty Shape and no Python exception are insufficient proof that intended material was added/removed.
- Topological `FaceN`/`EdgeN` indices may change after edits. Flag unstable face-based attachments.
- All complex read-only output should be summarized compactly so the Coordinator's context is not flooded.

See [references/inspection-snippets.md](references/inspection-snippets.md).
