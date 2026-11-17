# Testing and acceptance

## Confirmed historical tests

### Subagents

- A real Coordinator → Analyst call completed and returned content to parent context.
- A screenshot shows the child Analyst panel.
- One successful run completed in roughly 7 seconds; earlier attempts sometimes stopped before tool call with `unfinished:true` and no child agent.

### Analyst direct MCP

- A separate test reported four sequential `execute_python_mcp_freecad` calls, all completed.

### XYZ Calibration Cube

- Builder created `Part::Box` 20×20×20 mm at `(0,0,0)`.
- Volume ~8000 mm³; one Solid, six Faces, twelve Edges, eight Vertices; Shape valid.
- Binary STL: 12 facets, bounding box 20×20×20 mm, solid, no non-manifold/self-intersection reported.
- Reviewer independently recalculated hashes and confirmed files matched Builder report.
- A Builder reopen check closed/reopened the document and lost Undo history; geometry itself did not change.
- Latest export lists revision files under `/projects/xyz-calibration-cube-test`.

### Revision helper

- `team-v2-scratch`: before/after FCStd snapshots, ZIP integrity, SHA and `doc.FileName` checks reportedly passed.
- `team-v2-final-acceptance`: source 10×20×30 (6000 mm³), modified 12×20×35 (8400 mm³), Shape valid, four revisions and acceptance report.

## Baseline benchmark

See `benchmarks/CAD_AGENT_TEAM_ACCEPTANCE.md`. Tasks T0–T8 cover:
- design options without editing;
- read-only inspect known cube;
- create cube;
- engraved letters on three faces;
- parametric plate/bolt pattern;
- modify sketch-driven part;
- intentional invalid parameter;
- ambiguous provenance;
- provider 503/silent stream with no paid call.

Evidence per run: exact prompt, model/API, timing, tool/Subagent calls, retries, revisions, hashes, geometry metrics, Reviewer verdict, estimated token charge. Distinguish model/API/MCP/filesystem/fixture failures.

## Quality gates

A weighted score is not allowed to hide hard failures. Automatic fail conditions include accidental user-document mutation, missing required before revision, or claiming unverified PASS.
