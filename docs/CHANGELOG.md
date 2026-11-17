# Changelog

## 2026-11-17 — archive baseline

- Consolidated v1 and v2 original packages and exact agent prompts.
- Preserved Skills v0.1 bundle, six SKILL.md files, references, import ZIPs and role addenda.
- Preserved v3 Coordinator prompt and hashes for all four reported v3 prompts.
- Added full historical handoff, screenshots, Skills deployment handoffs and EZ AI hang report.
- Added an anonymized incident summary; raw conversation/tool export and customer CAD input were excluded from the public release.
- Corrected incident tool-call counts after parsing the source execution trace: 24 total / 17 FreeCAD MCP / 5 failed read_file / 2 output-page calls / 0 Subagent calls.
- Documented conflicting ACL, Skills and revision-root states rather than silently reconciling them.
- No live LibreChat, FreeCAD, Docker, MCP, ACL or agent configuration was changed during this archive build.
- Revalidated the internal SHA-256 manifests: all 14 files in v2 and all 11 files in v1 matched their package manifests.
- Ran the archived v2 offline `test_revision.py` against the preserved helper copy; result: `Offline cad_revision tests: OK` (this does not test the live FreeCAD/VM installation).
