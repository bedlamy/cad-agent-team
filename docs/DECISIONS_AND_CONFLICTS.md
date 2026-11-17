# Decisions, rejected options and conflicting records

## Accepted design decisions

1. LibreChat is the interface and orchestration layer.
2. EZ AI is the custom OpenAI-compatible provider.
3. Keep four roles: Coordinator, Analyst, Builder, Reviewer.
4. Use real LibreChat Subagents, not simulated delegation in prose.
5. Coordinator is the main user-facing agent.
6. Analyst is read-only by role policy; Builder mutates; Reviewer independently verifies.
7. Do not call Analyst before every operation if the documented state is fresh and unchanged.
8. Preserve previous revisions; use before/after checkpoints.
9. Use existing FreeCAD MCP Bridge v0.1.30; do not replace without research.
10. All operations against one live FreeCAD session must be sequential.
11. Do not change source STEP/FCStd; do not use `chmod 777` or blind recursive `chown`.
12. Do not infer EZ AI pricing or reasoning parameters; do not add tokenConfig with guessed prices.

## Evolution / changed decisions

- v1: single-writer Coordinator only; Bridge Ask.
- v2: direct MCP assigned to all four; actual runtime used Unrestricted after user manually selected it.
- v2 Coordinator could do small obvious changes itself.
- v3 Coordinator must delegate any geometry/CAD document mutation to Builder. This supersedes the v2 small-fix exception.
- Skills v0.1 were initially marked “not deployed”; later deployment summary reports six imported and assigned.

## Conflicts to retain, not silently reconcile

### Skills state

Earlier handoff snapshots say import was rolled back / zero active Skills. Later 13:22 UTC deployment summary says six Skills imported and four agents updated, with post-PATCH JSON 200. Later summary is newer and should be treated as the last reported state, but live read-back is still required.

### Workspace ACL

Earlier archival handoff says `<CAD_WORKSPACE>` was `root:root 0755`, FreeCAD UID 1000 could not write, and global ACL was not confirmed. `TOOL_ROADMAP.md` later describes global UID 1000 ACL as installed. No exact ACL command/read-back is preserved. Verify live.

### Cube project location

Earlier handoff says XYZ cube remained in `<TEMP_DIR>` because target workspace write failed. Latest incident export lists four revision files under `/projects/xyz-calibration-cube-test`, outside `<CAD_WORKSPACE>`. Treat later listing as progress, but project-root location needs explanation.

### FreeCAD version

Early handoff marked exact version unknown. Skills bundle README/Tool Roadmap use FreeCAD 1.1.4. Confirm live before version-dependent operations.

### v3 prompt files

All four v3 prompt hashes were reported. Only `coordinator-v3.md` is available as a full source file in this Library snapshot. Do not reconstruct other prompts from hashes.

## Rejected / not applied

- third-party Docker registry mirrors;
- direct MongoDB edits instead of official Agent/Skills API;
- replacing FreeCAD MCP Bridge;
- `chmod 777` or blind recursive `chown`;
- switching Coordinator to Haiku without controlled tests;
- adding unverified reasoning parameters or EZ AI tokenConfig;
- automatic Bridge startup macro (not implemented).
