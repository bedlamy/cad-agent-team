# Current known state — 2026-11-17

This is the latest assembled archive state, not a live read of dedicated VM.

## Agents

- Four agents exist: Coordinator, Analyst, Builder, Reviewer.
- IDs and model assignments are in `AGENTS_AND_PROMPTS.md`.
- Coordinator Subagents reported enabled; `allowSelf=false`, `shareFiles=true`, three child IDs.
- A genuine Coordinator → Analyst Subagent execution was previously confirmed by MongoDB<RUNTIME_TMP>time evidence and a screenshot.
- The incident summary refers to the Coordinator role; per-install IDs are redacted.

## Prompts and Skills

- v1 and v2 exact prompts are preserved.
- Exact v3 Coordinator prompt is preserved; its SHA matches the later reported hash.
- Later deployment summary reports all four v3 prompts applied; only Coordinator text is available here. Other three v3 prompt texts must be retrieved from live Agent Builder or source workspace.
- Six Skills reported active with IDs and intended matrix in `SKILLS.md`.
- Later summary reports `skills_enabled=true`, `skills_scope=selected`, exactly three Skills per agent.

## Models / provider

- Coordinator: `anthropic/claude-sonnet-5.5` via `ez-ai`.
- Specialists: `deepseek/deepseek-v4.1-flash` via `ez-ai`.
- Base URL `https://api.ez-ai.ru/v1`.
- Exact EZ AI tariffs, tokenConfig and reasoning format remain unverified.

## MCP / FreeCAD

- FreeCAD MCP Bridge `v0.1.30`.
- FreeCAD MCP endpoint `<FREECAD_CONTAINER_IP>:39280`; LibreChat API `<LIBRECHAT_CONTAINER_IP>` on `cad_mcp`.
- Tools: `execute_python`, `execute_python_file`, `get_output_page`; explicit v2 assignment two tools: execute_python + get_output_page.
- Last historical GUI profile reported `PermissionMode=1` (Unrestricted), manually selected by user.
- Bridge autostart was not implemented; it was manually enabled in FreeCAD.

## Workspace / revision state

- Intended Workspace: `<CAD_WORKSPACE>`.
- Helper installed by report at `<CAD_AGENT_HOME>/bin/cad_revision.py`.
- `team-v2-scratch` and `team-v2-final-acceptance` revision tests reported successful.
- Latest Coordinator export lists `/projects/xyz-calibration-cube-test` with `revision_log.json`, `project_state.json` and four revision FCStd files. This is outside the intended `<CAD_WORKSPACE>` path.
- ACL state conflicts between older handoff (unresolved) and later Tool Roadmap (global UID 1000 ACL described). Live ACL/GID not established in this archive.

## Latest incident

- User asked for a read-only review of `external-cad-input-package.zip`.
- The task was run by Coordinator ID above.
- No Subagent calls occurred; no final report was produced before stop.
- No source CAD modifications are visible in export; it did extract image files to `<TEMP_DIR>/cad-audit/img` and read STEP geometry through `Part.read`.
- The raw execution trace is not published; its aggregate findings are in the incident summary.

## Must verify live before next implementation step

1. exact v3 prompts and SHA for all four agents;
2. actual Skills catalog and assignment matrix;
3. current models/provider/tools/Subagents and runtime tool list;
4. FreeCAD Bridge mode, listener and GUI state;
5. live `cad_revision.py` source and API;
6. actual `<CAD_WORKSPACE>` ACL, UID/GID and bind mount;
7. whether `/projects/xyz-calibration-cube-test` is intentionally outside Workspace.
