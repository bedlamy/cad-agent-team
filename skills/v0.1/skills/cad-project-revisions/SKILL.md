---
name: cad-project-revisions
description: Use when creating or updating a FreeCAD CAD project, making before/after checkpoints, recording decisions, locating revisions, or recovering project state in CAD Agent Team.
---
# CAD Project & Revision Management (v0.1)

## Scope
This skill teaches the **existing** CAD Agent Team layout and revision helper. It does not provide file access by itself. Available FreeCAD tools are `execute_python_mcp_freecad` and `get_output_page_mcp_freecad`; do not hallucinate separate `create_body`, shell, or filesystem MCP tools.

## Canonical locations
- Container workspace root: `<CAD_WORKSPACE>` (host: `<HOST_CAD_WORKSPACE>`).
- Revision helper: `<CAD_AGENT_HOME>/bin/cad_revision.py`.
- Working files, revisions, `revision_log.json` and `project_state.json` are located in the dedicated project root.
- The helper permits paths elsewhere under `/projects`, but **our team policy is stricter**: new or changed projects must be under `<CAD_WORKSPACE>`.
- Do not silently use `<TEMP_DIR>`, `/projects/<other-name>` or another writable directory to bypass failures.

## When to inspect vs write
- Coordinator: find the project, use known state, delegate writes to Builder; no speculative file creation.
- Analyst / Reviewer: **read-only** inspection of project state and revisions. Never call `checkpoint` or `update_project_state`.
- Builder: perform revision lifecycle during authorized model edits.

## Authoritative API (from Computer agent source inspection; verify on deployment)
```python
import sys
if '<CAD_AGENT_HOME>/bin' not in sys.path:
    sys.path.insert(0, '<CAD_AGENT_HOME>/bin')
from cad_revision import checkpoint, read_project_state, update_project_state, quick_status
# checkpoint(doc, project_root, phase, note='') -> dict
# read_project_state(project_root) -> dict
# update_project_state(project_root, patch) -> dict
# quick_status(doc, project_root) -> dict
```

## Write lifecycle — Builder only
1. Confirm user-approved project root and identify the exact document (`App.getDocument(name)` or an explicitly new document). Do not rely on `App.ActiveDocument` if ambiguous.
2. Read `project_state.json` and the last successful revision if present. Detect untracked changes before modifying.
3. Confirm write access to the canonical project directory. If absent, stop and report; do not select a different root.
4. Create **before** checkpoint with `checkpoint(doc, project_root, 'before', note)` and verify returned success/path. Without a valid before snapshot, **do not mutate geometry**.
5. Make the approved change and inspect state/geometry. If the operation fails, stop; do not claim the document was restored simply because `Undo` exists.
6. Create **after** checkpoint and validate its file/journal entry. If the after checkpoint fails, stop subsequent changes and preserve the current live state for recovery.
7. Save the intended *working* `.FCStd` explicitly at the agreed project path **when required**; `saveCopy` snapshots alone do not update the working file. Do not overwrite user originals implicitly.
8. Update `project_state.json` only after the completed, verified change; record facts, design decisions, unresolved questions, and revision references.
9. Report paths, changed objects, validation results, and any incomplete stages. Never invent SHA values.

## Concurrency and durability
- Only one mutating actor works on a FreeCAD document at once.
- Current helper has a read-modify-write race on `revision_log.json`: serialize checkpoint writes per project.
- Snapshots contain `.FCStd` copies; verify filesystem presence, SHA-256 and ZIP integrity if acceptance requires it.
- No automatic pruning of revisions. Preserve audit history.
- `lightweight_fingerprint` is heuristic and **not** a proof of identical CAD semantics.
- Both `before` and `after` snapshots may be valid even if the working `.FCStd` has not been saved to the same state. State which was verified.

## Read-only reporting schema
`project_root`, `document_name`, `working_file`, `last_revision_id`, `last_revision_phase`, `state_known`, `untracked_changes_suspected`, `verified_facts`, `blockers`.

More detail: [references/revision-contract.md](references/revision-contract.md).
