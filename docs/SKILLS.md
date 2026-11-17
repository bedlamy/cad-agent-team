# LibreChat Skills v0.1

## Six Skills

| Skill | ID from later deployment report | Assignment |
|---|---|---|
| `cad-project-revisions` | `6afc54cd8053c120ec96ff97` | All four agents |
| `freecad-document-lifecycle` | `6afc54cd8053c120ec96ffb0` | All four agents |
| `cad-task-orchestration` | `6afc54cd8053c120ec96ffc9` | Coordinator |
| `freecad-geometry-inspection` | `6afc54cd8053c120ec96ffe2` | Analyst |
| `freecad-parametric-modeling` | `6afc54cd8053c120ec96fffb` | Builder |
| `cad-independent-verification` | `6afc54cd8053c120ec970014` | Reviewer |


## Intended assignment matrix

Each agent receives exactly three Selected Skills: two common + one role-specific.

| Agent | Selected Skills |
|---|---|
| Coordinator | `cad-project-revisions`, `freecad-document-lifecycle`, `cad-task-orchestration` |
| Analyst | `cad-project-revisions`, `freecad-document-lifecycle`, `freecad-geometry-inspection` |
| Builder | `cad-project-revisions`, `freecad-document-lifecycle`, `freecad-parametric-modeling` |
| Reviewer | `cad-project-revisions`, `freecad-document-lifecycle`, `cad-independent-verification` |

The assignment matrix comes from the Skills bundle README. The later deployment summary confirms exactly three Skills per agent, `skills_enabled=true`, `skills_scope=selected`, and that all four agents were updated. Exact read-back matrix from the live API was not preserved in the available handoff; verify it live before future changes.

## Status chronology

- Initial bundle README: “Not deployed” — accurate when package was first prepared.
- `HANDOFF_skills_early_2026-11-17.md` and follow-up handoff: describe failed/rolled-back attempts and zero active Skills at those times.
- Later report at 2026-11-17 13:22 UTC: six Skills imported, IDs returned, all four agents updated, post-PATCH JSON 200; models/provider/MCP/tool options/Subagents/edges/IDs unchanged.
- The later report supersedes the earlier zero-Skills status, but the full final deployment transcript is not present here.

## Source files

`skills/v0.1/` contains the six SKILL.md files, references, six import ZIPs, role instruction addenda, benchmark and README. `source-archives/CAD_Agent_Team_Skills_v0.1_bundle.zip` is the original bundle.

## Permissions note

Skills do not grant or restrict tool permissions. They teach procedures. The FreeCAD MCP `execute_python` capability remains arbitrary Python; Analyst/Reviewer read-only remains prompt-level.
