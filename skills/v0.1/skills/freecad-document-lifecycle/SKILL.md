---
name: freecad-document-lifecycle
description: Use when identifying the active FreeCAD document, opening or saving a CAD project, examining document state, recomputing after edits, handling undo/reopen, or exporting FCStd/STL/STEP.
---
# FreeCAD Document Lifecycle (v0.1)

## Core rule
Distinguish **live FreeCAD document**, **saved working FCStd**, **checkpoint snapshot**, and **exported mesh/STEP**. They are not interchangeable. Report which artifact was actually verified.

## Determine state before action
- Identify FreeCAD document by internal name, `doc.FileName`, intended project root, and known revision.
- If multiple documents are open or the active one differs from the task, stop and resolve identity; never select a similarly named document by guesswork.
- For read-only agents: querying objects, labels, properties, placements and shapes is permitted; **do not** call `recompute()`, `save()`, `saveAs()`, create a document, or import/export via the live GUI.
- For Builder: only recompute the authorized working document following mutations.

## Safe mutation lifecycle (Builder only)
1. Identify the document and project root; obtain valid **before** snapshot via `cad-project-revisions`.
2. Record object names, parameters and relevant baseline geometry metrics.
3. Make a bounded set of FreeCAD operations; prefer explicit `doc` variables over implicit global state.
4. `doc.recompute()` once per meaningful stage, inspect errors and geometric output. A successful Python call **does not** prove a valid CAD model.
5. Create **after** snapshot, check integrity, save working FCStd deliberately, and export only requested formats.
6. Confirm saved paths and independent measurements. Never overwrite an unrelated source file.

## Live GUI caveats
- Do not close, reopen, or change the active document merely to test a save/restore. This can lose Undo history and disturb the user.
- For destructive parameter perturbation, reopen tests, or import validation, use a **separate copy in an isolated FreeCAD process** only when the runtime provides a verified safe mechanism; otherwise mark as not tested.
- MCP Bridge can execute Python inside the GUI, and in Unrestricted mode grants full process authority. Role instructions are not a security sandbox.
- Keep GUI work serial: no simultaneous Builder and Reviewer writes; Reviewer is read-only.
- Do not use shell, subprocess, network access, or modify FreeCAD preferences from MCP Python.

## Evidence terminology
- `LIVE_VERIFIED`: measured on the currently open document.
- `SNAPSHOT_VERIFIED`: verified `revisions/*.FCStd` exists and passed checks.
- `WORKING_FILE_VERIFIED`: saved `.FCStd` verified on disk.
- `EXPORT_VERIFIED`: mesh/STEP examined independently, not merely produced.
- `UNVERIFIED`: unable to inspect required artifact, explain why.

Detailed checklist: [references/document-checklist.md](references/document-checklist.md).
