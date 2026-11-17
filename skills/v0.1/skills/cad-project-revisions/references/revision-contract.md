# CAD revision contract and known limits

Source baseline: Computer agent report supplied by the user, November 2026. The implementation was inspected remotely but its full source is not bundled here. Treat code excerpts as *API notes*, not a replacement for the actual helper.

`checkpoint(doc, project_root, phase, note='') -> dict`: saves a snapshot using FreeCAD `doc.saveCopy()`, under `<project_root>/revisions/<UTC>-<uuid8>-<phase>.FCStd`, appends a JSON record to `<project_root>/revision_log.json`, and may affect project state. Phases currently used: `before` and `after`. Verify returned fields from actual running helper rather than assuming dictionary keys.

`read_project_state(project_root) -> dict`: reads the project state. `update_project_state(project_root, patch) -> dict`: performs an atomic merge/update of `project_state.json` with `schema=1`, `facts`, `decisions`, `open_questions`. Exact patch substructure must be confirmed at integration.

`quick_status(doc, project_root) -> dict` and `lightweight_fingerprint(doc) -> str` provide lightweight status; they are not full independent validation.

Important observed tests: before/after of `Part::Box` 10→25 and of nested `Part::Cylinder` 12→30, ZIP integrity and SHA consistency passed, and `saveCopy()` did not change `doc.FileName`. The *working* FCStd on disk remained at its earlier geometry until an explicit save.

Limitations: caller must invoke checkpoints; no parallel-write lock; no automatic revision pruning; damaged revision log is intentionally not overwritten; project-root guard only checks containment in `/projects`, not the CAD workspace; headless FreeCAD tests are not proof the live GUI's MCP tool is on.

Rollback is a **separate, explicit procedure**, not automatically accomplished by the presence of a snapshot. No destructive restore until the target and source revisions have been named and a recoverable copy retained.
