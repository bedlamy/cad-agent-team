# CAD Agent Team

**Purpose:** document and develop a multi-agent CAD workflow for LibreChat + FreeCAD MCP: Coordinator, Analyst, Builder, and Reviewer.

**Archive baseline:** 2026-11-17. This repository preserves the architecture, historical prompts, six Skills, revision helper, acceptance tests, handoff notes, and an anonymized incident case study. It is a historical baseline, not a live configuration snapshot.

> **Public repository:** infrastructure addresses, per-install agent/conversation IDs, host-specific paths, raw conversation/tool exports, and customer CAD inputs have been redacted or omitted. See [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).

## Start here

1. [`docs/00_START_HERE.md`](docs/00_START_HERE.md) — project entry point and status conventions.
2. [`docs/CURRENT_STATE_2026-11-17.md`](docs/CURRENT_STATE_2026-11-17.md) — last assembled state (not live-verified).
3. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — architecture and evolution v1 → v2 → v3.
4. [`docs/AGENTS_AND_PROMPTS.md`](docs/AGENTS_AND_PROMPTS.md) — roles, model assignments, and prompt versions.
5. [`docs/ORCHESTRATION_AND_ROUTING.md`](docs/ORCHESTRATION_AND_ROUTING.md) — routing rules and observed failure modes.
6. [`docs/INFRASTRUCTURE.md`](docs/INFRASTRUCTURE.md) — generalized deployment topology and versions.
7. [`docs/VERSIONING.md`](docs/VERSIONING.md) — revision helper and project checkpoints.
8. [`docs/SKILLS.md`](docs/SKILLS.md) — six Skills and assignment intent.
9. [`docs/KNOWN_GAPS.md`](docs/KNOWN_GAPS.md) — unknowns and live verification needs.
10. [`docs/incidents/2026-11-17-coordinator-overrun-summary.md`](docs/incidents/2026-11-17-coordinator-overrun-summary.md) — anonymized incident report.

## Repository layout

- `agents/v1/`, `agents/v2/`, `agents/v3/` — preserved prompt generations.
- `skills/v0.1/` — six Skills, references, import ZIPs, and role addenda.
- `versioning/v2/` — revision helper and unit tests.
- `benchmarks/` — baseline acceptance suite.
- `history/packages/` — extracted historical v1/v2 source packages.
- `docs/` — architecture, deployment, decisions, handoffs, incident analysis.
- `evidence/` — sanitized screenshots from the setup and orchestration tests.
- `source-archives/` — reproducible sanitized source bundles (not byte-identical to private originals).

## Evidence and status discipline

Distinguish confirmed tests, reported actions, prepared-but-not-applied files, unknowns, and conflicting snapshots. Do not claim a live configuration is current without re-reading the deployed system.

## License

No open-source license has been selected yet. Public visibility alone does not grant permission to reuse or redistribute the contents.
