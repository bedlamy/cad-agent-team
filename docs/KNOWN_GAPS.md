# Known gaps and next verification needs

## Highest priority

1. Retrieve exact live v3 prompt text for Analyst, Builder and Reviewer; compare SHA-256 with reported hashes.
2. Read back live Skill catalog and per-agent Selected Skills; confirm all six IDs and three-per-agent matrix.
3. Verify runtime tool list for Coordinator and each specialist; do not infer `subagent` from stored MongoDB fields.
4. Read live `<CAD_AGENT_HOME>/bin/cad_revision.py` and establish exact API/behavior versus archived v2 helper.
5. Verify `<CAD_WORKSPACE>` UID/GID, mount and ACL without changing them.
6. Explain whether `/projects/xyz-calibration-cube-test` is intentionally outside the target Workspace.
7. Establish provider timeouts/stream behavior and EZ AI tariffs/tokenConfig only from authoritative API evidence.

## Other gaps

- Full Compose, `librechat.yaml`, `.env`, MongoDB export and live agent JSON are not included; secrets must remain excluded.
- Exact FreeCAD version was initially unknown; later bundle says 1.1.4, not live verified here.
- GID and host/container user mapping are not established.
- Full EZ AI `/v1/models` catalogue and model-specific Chat Completions/tool calling/reasoning behavior are not fully verified.
- Exact current ACL policy is conflicting between sources.
- Skills deployment final transcript is not included; later status summary is available but not full raw API read-back.
- v3 prompt contents for Analyst/Builder/Reviewer are missing; only hashes are available.
- The latest external CAD CAD input archive is referenced in the incident but its raw bytes could not be materialized from the current Library item; see `examples/external CAD-remote-2026-11-17/README.md`.
- The latest Coordinator run ended unfinished; no completed design understanding report exists.
