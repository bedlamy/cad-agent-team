# Tools and capability gaps — architectural recommendations

## Installed now (do not replace)
- LibreChat v0.8.9-rc1 with real Subagents.
- FreeCAD 1.1.4 (container `cad-freecad`).
- MCP Bridge v0.1.30: `execute_python`, `execute_python_file`, `get_output_page`; agent explicit assignment historically limited to first and last.
- Revision helper under `<CAD_AGENT_HOME>/bin` and global UID 1000 ACL for `<CAD_WORKSPACE>`.

## Priority 1: improve correctness, not quantity of tools
1. **Read-only structured inspection**: dedicated bounded tool returning doc identity, object tree, solids, shape validity, bounding boxes, sketch solver state, feature errors. Could be wrapped in a narrow helper, tested in a scratch session; avoid running arbitrary read-only prompts through unrestricted Python when hard isolation is possible.
2. **Guarded mutation / transaction wrapper**: project-root allowlist, single-writer lock, mandatory before/after checkpoint, expected object IDs, timeout/error report, rollback strategy. Needs design and separate authorization; the current revision helper is not automatic.
3. **Export verification helper**: inspect FCStd/STEP/STL on isolated copy, hashes, mesh watertightness and dimensions without changing live GUI.
4. **Viewport screenshot/visual inspection**: useful to catch mirrored letters and design appearance defects that bbox/volume miss. Requires a verified read-only viewport API; do not assume current Bridge tool provides screenshots.

## Priority 2: process memory and artifacts
- Structured per-project manifest / design brief and acceptance JSON; consistent handoffs to avoid repeated inspections.
- Serialized project revision journal to avoid `revision_log.json` lost updates.
- Optional CAD library skills later: enclosures, mounting hardware, heat-set inserts, printable overhang test geometry. Supplier and material-specific tolerances must be verified, not invented.

## Third-party projects studied (design references only)
- https://github.com/ghbalf/freecad-ai — detailed construction skill recipes and testing.
- https://github.com/LBurny/cadpilot — step journal, controlled rollback, quantitative geometry feedback, testing of silent geometry errors.
- https://github.com/yonosoft/freecad-mcp — typed Sketcher operations, solver DoF/constraint diagnostics; experimental.
- https://github.com/Getopir/AgentCAD — controlled gateway and CAD-IR direction; pre-alpha.
- https://github.com/CREATeNG/freecad-mcp-bridge — current installed bridge.

**Recommendation:** no new MCP server or extra arbitrary shell/file tools until these needs are benchmarked. Skills teach how to use tools; they do not technically restrict unrestricted Python capability.
