# CAD Agent Team — Skills Pack v0.1 deployment handoff

Date: 2026-11-17 UTC
Workspace: `/workspaces/computer-admin`
Target: LibreChat on dedicated VM (`<LAN_HOST_IP>`, `cad-studio`)

## Status

Deployment was stopped before any LibreChat write. No Skills were imported, no
agent assignments were changed, and no system prompts were changed. No
containers were restarted.

The blocker is authorization: the штатный LibreChat API returned `401 No auth
token` for both `/api/skills` and `/api/agents`. `/api<FREECAD_CONFIG_ROOT>` returned HTTP
200. No authorized UI session or LibreChat credential was available, and
MongoDB was not used as a write path.

## Completed backup

Protected backup on dedicated VM:

`<LIBRECHAT_CONFIG_ROOT>/backups/pre-skills-v0.1-20261117T104057Z/`

- directory mode: `700 root:root`
- files: mode `600`, owner `root:root`
- selected MongoDB BSON archive: `librechat-agents-skills.archive`
- full current agent documents: `agents-full.json`
- full current Skills documents: `skills-full.json`
- non-secret count/identity summary: `manifest-summary.json`
- file checksums: `SHA256SUMS.txt`
- backup checksum manifest SHA-256: `42f9837fd977e7a18d3463598795c143a15bbd32f367efc0a3bdcab035b6504e`

Verification passed:

- all five backup files passed `sha256sum -c`;
- `mongorestore --archive --dryRun` passed;
- pre-change state was 4 agents and 0 Skills.

The existing read-only snapshot remains the additional baseline:
`artifacts/cad-librechat-snapshot-20261117T102657Z/`.

## Source integrity

The only selected import source is
`.build/cad-skills-v0.1-review/final-import-candidate/`. Its six ZIP files
match the supplied `SHA256SUMS.txt`; the original source and original archive
were not changed.

## Prepared but not applied

The v2 prompt sources are preserved in
`artifacts/cad-librechat-snapshot-20261117T102657Z/prompts/`. The four v0.1
role addenda are preserved in
`.build/cad-skills-v0.1-review/bundle/CAD_Agent_Team_Skills_v0.1/role_instruction_addenda/`.
No v3 prompt was written to LibreChat because the authorized API session was
not available.

## Required continuation

Provide an authorized LibreChat UI/API session for dedicated VM. Then, using the
official Skills and Agents API only:

1. import the six ZIP files;
2. read back their actual IDs and content;
3. append the four addenda to the corresponding existing prompts;
4. set exactly three selected Skills per agent;
5. read back and compare models, provider, MCP assignments, Coordinator
   Subagents, prompt content, and Skill assignments against the baseline;
6. write a post-change checksum and verification report.

No CAD generation test is authorized in this handoff.
