# Acceptance matrix for CAD review

| Layer | Minimum signal | Important failure mode |
|---|---|---|
| Request | Exact requested features and units | Valid model that does not satisfy user brief |
| Topology | Shape validity, expected solids | Open/empty shape, unintended solids |
| Geometry | Bounding box, volume, placement | Boolean cut misses target; feature placed on wrong face |
| Sketch | Constraint count, solver/DoF when available | Hidden freedom, redundant constraints, unstable datum |
| Dependencies | Feature base and in/out links | Feature depends on accidental face index |
| Revision | Before/after FCStd, hashes and journal | Wrong path, unsaved working file, missing revision |
| Export | STL watertightness, bbox, volume | Export mismatch or bad tessellation |
| Robustness | Perturbation on isolated copy | Fragile parametric model that breaks on edit |
| Printability | Known material/process and clearances | Generic geometric checks misrepresented as guaranteed printable |

Example: nominal 20×20×20 cube, user tolerance not provided. A reviewer can report measured 20.0000 × 20.0000 × 20.0000 mm and 8000 mm³, but should not invent arbitrary 0.1 mm tolerance.

BRep validity is one signal. Some OCCT/FreeCAD operations show discrepancies between status and `Shape.isValid()`; treat contradictory results as a diagnostic issue, never as automatic PASS.
