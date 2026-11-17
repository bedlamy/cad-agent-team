# Parametric construction and risk checklist

Reference themes: official FreeCAD Feature editing and Topological naming problem documentation; experimental yonosoft FreeCAD MCP research; CADPilot's practical failure reports.

### Minimize topological naming risk
- Attach sketches to base planes/axes or datum planes derived from them when possible.
- Avoid depending on transient generated `FaceN` and `EdgeN` indices; re-resolve topology after significant mutation if unavoidable.
- Use master sketches and expressions when appropriate, avoid gratuitous dependencies.

### Solver quality
- Meaningful dimensional constraints; avoid redundant/over-constrained solutions.
- Confirm remaining degrees of freedom only when known to be supported by the build. Not every sketch must be fully constrained for every exploratory task, but parametric production features generally should be controlled intentionally.
- Geometry and constraints should keep their intent under normal parameter changes.

### Primitive and boolean caveats
- `Part::Box` is useful for a calibration test but doesn't automatically give a rich sketch-based parametric feature history.
- Boolean cuts that remove zero material are failures against a cutting requirement, even if the resulting shape is `isValid()`.
- PartDesign feature outputs can be entire bodies; copying or patterning the wrong object can generate duplicates of the entire solid rather than only a cut feature.
- Curves/fillets and generated edge indices are high-risk; test shape output after each stage.
- Multiple solids in a Body may be incorrect unless specifically allowed; check `len(shape.Solids)`.
- An error-free recompute is a necessary signal, not proof of correct geometry.

### 3D-printing specific concerns
- If designing for FDM, distinguish a closed manifold STL from a mechanically printable feature; printer/material/orientation/tolerance information may be needed to assess overhangs, bridges, holes and clearances.
- Do not assume heat-set inserts or bolt counterbores fit a manufacturer's part from generic dimensions; ask for part specification or mark defaults clearly.
- Validate bounding box and tessellation of exports independently when possible.

### Source reading list
- https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Feature_editing.md
- https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Topological_naming_problem.md
- https://github.com/ghbalf/freecad-ai
- https://github.com/LBurny/cadpilot
- https://github.com/yonosoft/freecad-mcp
