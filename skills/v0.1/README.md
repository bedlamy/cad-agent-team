# CAD Agent Team — Skills Pack v0.1 (draft)

Prepared for: LibreChat v0.8.9-rc1, FreeCAD 1.1.4, MCP Bridge v0.1.30. Based on the CAD historical handoff and current Computer agent diagnostics. **Not deployed**. This directory and import ZIPs are local deliverables, not server changes.

## Six core Skills

| Skill name | Agent selection |
|---|---|
| `cad-project-revisions` | All four |
| `freecad-document-lifecycle` | All four |
| `cad-task-orchestration` | Coordinator |
| `freecad-geometry-inspection` | Analyst |
| `freecad-parametric-modeling` | Builder |
| `cad-independent-verification` | Reviewer |

Each of four agents receives **three** Selected Skills: the two common skills + one role-specific skill. A skill itself does not grant permissions. The common skills are role-aware so Analyst/Reviewer do not treat write workflows as their instructions.

## Import into LibreChat (after review)

1. Back up current four agent instructions, model IDs, tools, Subagents relations and Skills settings.
2. Open the LibreChat **Skills** sidebar and import each ZIP from `import_zips/` separately. Each archive contains one top-level `<name>/SKILL.md` plus a `references/` file. Use the official UI; do not write directly into MongoDB.
3. Inspect the imported name, description and bundled references; verify Available to agent is on where intended.
4. Set Agent Builder → Skills → **Selected**, then add exactly three skills per agent (matrix above). Save each agent without changing its model or tools.
5. Append the role-specific `role_instruction_addenda/<role>.md` to its existing v2 instructions **after** backing them up, resolving any contradictory old rule. Do not replace full prompts with these short addenda.
6. Check every agent can load only appropriate Skills, and that Coordinator still has Subagents and its original FreeCAD tools. Verify skill auto-selection in harmless chat-only test and read-only Analyst inspection.
7. Run the staged benchmark in `benchmarks/` with current models before any model switches.

## Important runtime notes
- `SKILL.md` frontmatter `name`/`description` follows LibreChat docs. No `allowed-tools` elevation or `always-apply` is included: always-on safety rules belong in agent instructions, not optional Skills.
- Bundled `references/` are Markdown-only, no executable skill scripts or `handler.py`; handler semantics from FreeCAD AI **do not** apply to LibreChat.
- Explicit model-dependent Skills invocation requires stable EZ AI streaming; provider 503 can hang even on READY. Do not interpret it as a skill failure.
- FreeCAD `execute_python_mcp_freecad` provides full Python privilege inside the GUI when Bridge is Unrestricted. Read-only agents are currently policy-based, not sandbox-enforced.
- Working `.FCStd`, before/after snapshot and STL export require separate verification.

## Future model trial (not applied)
Coordinator Claude Sonnet 5.5; Analyst DeepSeek V4.1 Flash; candidate Builder Claude Opus 5.5; candidate Reviewer Gemini 4 Carbon. Compare under same test suite before making changes. Reference prices from EZ AI `/models` are provider-reported per-token values; currency not explicit in API.

## Research sources
- https://www.librechat.ai/docs/features/skills
- https://www.librechat.ai/docs/features/agents
- https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Feature_editing.md
- https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Topological_naming_problem.md
- https://github.com/ghbalf/freecad-ai
- https://github.com/LBurny/cadpilot
- https://github.com/yonosoft/freecad-mcp
- https://github.com/Getopir/AgentCAD
- https://github.com/CREATeNG/freecad-mcp-bridge
