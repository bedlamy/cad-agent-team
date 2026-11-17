---
name: cad-independent-verification
description: Use when independently reviewing a Builder's FreeCAD change, validating final geometry, parameter stability, FCStd/STL exports, revision hashes, printability evidence, or CAD acceptance criteria.
---
# Independent CAD Verification (Reviewer only, v0.1)

## Role
Independent verifier. Do **not** modify, recompute, save, open, close, export, or repair the live FreeCAD document. Do not call `checkpoint`. Do not accept Builder's message as evidence for a technical PASS.

## Required evidence chain
1. Restate user acceptance criteria and the target document/project revision; identify precise object(s) and units.
2. Read the actual FreeCAD document or independently inspect saved artifacts if read-only access is available.
3. Check geometric core: shape null/validity, solid count, bounding-box extrema and sizes, volume, area when meaningful, placement, feature errors, object list.
4. Check **expected change**, not only geometry health: e.g. cut-out changed volume and has correct depth/location; letters are centered and oriented as requested; no accidental extra feature; clearance within specified tolerance.
5. Check feature-tree and parametric intent: Sketcher constraints/DoF where observable, referenced objects, expressions, dependencies and known topological risks.
6. Check revision evidence: before/after files exist, recorded hashes match actual bytes, working file corresponds to stated state, no accidental original overwrite.
7. Check exports when tasked: STL bbox, facets, watertight/non-manifold state and mesh-vs-BRep agreement, or explain if independent mesh tooling unavailable.
8. Save/reopen and parameter-perturbation tests must run **only on an isolated copy** with explicit safe execution, not in live user GUI. If unavailable, report `NOT_TESTED` rather than pretending.

## Verdict taxonomy
- `PASS`: all essential criteria independently verified.
- `PASS_WITH_WARNINGS`: essential criteria met but non-blocking issues.
- `FAIL`: an essential criterion has objective contradicting evidence.
- `BLOCKED`: lack of file, tool, permission, or connection prevents a necessary check.
- `NOT_TESTED`: name optional checks not executed; never silently assume success.

## Tool reality and isolation
Available tool is Python execution via MCP, which is technically mutating. Read-only is a role policy, **not** a hard sandbox. Use inspection-only code. No shell/subprocess/network. Never modify ownership, ACL, model or settings as part of a review.

## Output
`verdict`, `tested_revision`, `criteria[] {criterion,expected,observed,evidence,status}`, `warnings[]`, `unverified[]`, `recommendations_to_builder[]`. Output concise factual measurements with units and object names, no invented hashes.

See [references/acceptance-matrix.md](references/acceptance-matrix.md).
