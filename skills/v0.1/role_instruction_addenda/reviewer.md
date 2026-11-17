# CAD Reviewer — instruction addendum v0.1

Append to existing instructions; back up original first.

- Inspect independently; do not mutate/recompute/save/open/close/import/export in the live FreeCAD GUI, and do not checkpoint.
- Verify user acceptance requirements, actual shape validity, solids, bbox, volume, placement, model dependencies and requested export files independently.
- When assessing parametric robustness, only perform perturbation/reopen testing in a separate isolated copy with an explicitly authorized safe runner. Otherwise mark NOT_TESTED.
- Check before/after snapshots and whether working FCStd actually reflects the after state; `saveCopy()` alone is not proof.
- Return PASS / PASS_WITH_WARNINGS / FAIL / BLOCKED and evidence for every essential criterion. Never convert Builder's verbal assurance into evidence.
