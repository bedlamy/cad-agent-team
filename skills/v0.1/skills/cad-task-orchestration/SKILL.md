---
name: cad-task-orchestration
description: Use when coordinating CAD Analyst, Builder and Reviewer through LibreChat Subagents, selecting which expert to call, defining acceptance criteria, and tracking handoffs for complex CAD tasks.
---
# CAD Task Orchestration (Coordinator only, v0.1)

## Intent classifier
- **Discussion / ideation / explanation:** respond conversationally. Do not touch FreeCAD unless current geometric facts are needed and not known.
- **Read-only question with known fresh facts:** answer from confirmed context and cite source revision; do not automatically call Analyst.
- **Unknown document or changed state:** call Analyst for focused measurements.
- **Simple atomic, low-risk inspection:** Coordinator may use its MCP read-only queries.
- **Any new geometry, multiple dependent features, changes on multiple faces, sketch constraints, boolean operation, complex placement, mesh regeneration, or significant parameter edit:** delegate to **Builder**, even if the user frames it as a small tweak.
- **High-impact geometry, export, mating fit, ambiguous result, or a milestone of delegated modeling:** call **Reviewer** after Builder completes. Reviewer must independently inspect facts.

## Handoff format to Builder
`objective`, `project_root`, `exact document`, `known revision`, `allowed objects`, `constraints`, `units`, `acceptance metrics`, `non-goals`, `checkpoint requirement`, `MCP availability`, `what to return`.

## Handoff format to Analyst
`question`, `exact document/revision`, `required read-only facts`, `measurements and tolerances`, `do-not-modify requirement`.

## Handoff format to Reviewer
`user's original acceptance criteria`, `document and revision`, `requested independently verifiable metrics`, `source files and exports`, `risk areas`. Do not let Builder's narrative substitute for acceptance evidence.

## Sequential access
All Subagents can reach the same live FreeCAD session. Do not run model-changing tasks concurrently; delegate/await sequentially. Reviews only after Builder has finished its writes and state is stable.

## State handling
Before new work, identify current project and revision from the latest trusted report or `project_state.json`. Small contextual follow-ups can reuse fresh state with a minimal identity check. If stale or contradictory, call Analyst.

## Availability and provider failure
- If no model text or first tool event arrives, do **not** assume FreeCAD or ACL is failing.
- EZ AI has previously returned `503 Subscription unavailable; Paid OpenRouter fallback is disabled`. A silent streaming provider can leave LibreChat in Generating.
- Do not spin repeated Subagent calls after a provider error. Surface a clear blocker and preserve the project state.

## User-facing closure
`done`, `checked independently?`, `before/after revision`, `working FCStd/export locations`, `open risks`, `what needs user decision`. Do not claim end-to-end success when Builder or Reviewer was skipped.

See [references/routing-examples.md](references/routing-examples.md).
