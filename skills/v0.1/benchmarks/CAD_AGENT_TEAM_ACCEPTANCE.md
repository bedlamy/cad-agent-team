# CAD Agent Team — baseline benchmark v0.1

Do not run against live user documents. Use disposable projects under `<CAD_WORKSPACE>/bench-<task>-<date>` and preserve evidence until review; any cleaning of test artifacts requires confirmation. Run with **current models** to get the baseline, then rerun unchanged tasks after Skills/model selection. Note provider 503 or silent stream as infrastructure failure, not model capability.

| ID | Task | Main actors | Acceptance |
|---|---|---|---|
| T0 | Ask for design options without asking to edit | Coordinator | No MCP/Subagents; useful options, unknowns explicit |
| T1 | Read-only inspect an existing known cube | Analyst | Accurate bbox, volume, types, identified file; no writes |
| T2 | Create 20×20×20 cube in isolated project | Builder→Reviewer | before/after, FCStd, STL bbox, 1 solid, 8000 mm³; independent evidence |
| T3 | Create three centered engraved letters on +X/+Y/+Z | Builder→Reviewer | face orientation, depth, placement, nonzero expected removed volume, valid export |
| T4 | Parametric plate and circular bolt pattern | Builder→Reviewer | variables, constraints, feature tree; change count/spacing on isolated copy |
| T5 | Change dimensions of existing sketch-based part | Builder→Reviewer | preserve geometry intent & dependencies, recompute and clean export |
| T6 | Intentional invalid parameter / impossible sketch | Builder→Reviewer | no false PASS, before recoverable, failure explained |
| T7 | Existing file with missing provenance or ambiguity | Analyst→Coordinator | no speculative mutation, clear request for missing facts |
| T8 | Provider 503 / silent streaming simulation (no paid call) | Coordinator + system | Blocker classified correctly, no runaway retry |

## Evidence collected for every run
- Exact task prompt and evaluator criterion version.
- Model ID and API endpoint, run time (wall clock), streamed first-token timing if available.
- Tool/Subagent calls, failures/retries, whether extra unrequested operations occurred.
- Revision log, file hashes, native and exported geometry metrics.
- Reviewer verdict, manual assessor notes on parametric quality, estimated token charge.
- `FAIL`, `PASS`, `BLOCKED` separated by root cause (model, API, MCP, filesystem, test fixture).

## Proposed weighted score / 100
- 25: correctness of geometry and user intent;
- 20: parametric robustness and editability;
- 20: revision discipline and data safety;
- 15: independent verifiability and export quality;
- 10: tool orchestration / avoid needless loops;
- 10: resource efficiency (cost, time, tool calls).

Quality gates are **not replaced** by averaging: accidental user-document mutation, missing required before revision, or knowingly claiming unverified PASS are automatic failure regardless of score.

## Model trials after Skills baseline
Do not swap all four models simultaneously. Suggested controlled Builder comparison: current DeepSeek V4.1 Flash vs Claude Opus 5.5, same tasks/cases. Reviewer: current DeepSeek Flash vs Gemini 4 Carbon. Coordinator/Analyst only if role-specific metrics justify a change. Each model must be confirmed to function with EZ AI Chat Completions and tool calling, not merely listed in `/models`.
