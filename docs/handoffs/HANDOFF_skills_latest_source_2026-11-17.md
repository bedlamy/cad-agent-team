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

## Follow-up authorization check — 2026-11-17

The previously used login method was checked: the installed application exposes
`POST /api/auth/login`, with JSON `{ "email": "...", "password": "..." }`,
and requires the normal same-origin/auth middleware. No usable email/password
credential is present in the available Computer secret store, environment, or
temporary runtime paths. The VM contains a protected LibreChat `.env`, but its
contents were not read or exposed because it is not an account credential
source and may contain service secrets.

The installed v0.8.9-rc1 code confirms:

- Skills import: `POST /api/skills/import` (multipart upload), listing:
  `GET /api/skills`;
- agent management routes are mounted by this build under
  `/api/agents/v1/agents`, not as a root `GET/PATCH /api/agents` pair;
- the root `/api/agents` router is primarily chat/agent execution routes.

No login request was sent with guessed or empty credentials, so no rate-limit
or account state was affected. Continuation requires the previously agreed
LibreChat email/password to be made available through the authorized secret
source or supplied for one in-memory login attempt. Do not send the password
in chat or place it in the workspace.

## Follow-up implementation attempt — 2026-11-17

The supplied credentials authenticated successfully. The six ZIP files were
imported through `POST /api/skills/import` and each returned HTTP 201. The
official list then showed six Skills with IDs recorded in the transient
process only. Agent changes were not attempted because this build does not
provide the requested CRUD API at the root `/api/agents` path: that path is an
agent execution/SSE router. The only CRUD routes in the installed source are
mounted under `/api/agents/v1/agents` and protected by separate management
authentication, which was explicitly out of scope.

To avoid partial deployment, all six imported Skills were rolled back using
the official `DELETE /api/skills/:id` route; each returned HTTP 200 and
`GET /api/skills` returned zero active Skills. The API implements this as a
tombstone: MongoDB now contains six internal documents named
`__deleted__<id>`. They are not visible in the official Skills catalog. No
direct MongoDB cleanup was performed.

JWT, login response, cookies, and temporary request files were removed from
`<RUNTIME_TMP>` after the rollback. Final active configuration remains unchanged: 4
agents and 0 active Skills. Prompt v2/v3 integration and agent assignments
remain pending.

## Immediate deployment attempt — 2026-11-17

The user authorized one in-memory login using the credentials already supplied
in this task. Login succeeded with HTTP 200; no credential, JWT, or cookie was
written to the workspace or included in output.

The pre-change backup was rechecked with privileged read-only access. The
directory remains `700 root:root`; all four agent files and the BSON archive
passed SHA-256 verification.

Four v3 prompt files were prepared locally from the preserved v2 prompts plus
the four role addenda:
`.build/cad-skills-v0.1-review/v3-prompts/`. Their SHA-256 values are:

- `analyst-v3.md`: `446097500189ce8b10800e7e8a0c9d697ec6e3ed3f7327f706c7a4cbb3f10d11`
- `builder-v3.md`: `59a3b1ceee388f2f72421af35b17ae5a593356e8b8c7327a5781352217f43abc`
- `coordinator-v3.md`: `916225e9475122888e059f8f6e68baba7ac3bbb238646dfaa51567147fec0ea4`
- `reviewer-v3.md`: `45ebf3643ebd6cb48cca2174d54e99a927d855be1ca7ede46d10bfb6225d8877`

The active Skills catalog returned zero entries. Before any import or PATCH,
all four requested user API reads (`/api/agents` and each
`/api/agents/:id/expanded`) returned HTTP 200 with an SSE error envelope:
`event: error`, `{"message":"Illegal request"}`. The same result occurred
with Bearer JWT alone and with the login cookie added. Thus the runtime did not
return JSON agent configurations, so the required preflight and safe
post-PATCH verification could not be performed.

No Skills were imported in this attempt. No agent, prompt, model, provider,
MCP, Subagent, Docker, ACL, or FreeCAD setting was changed. No rollback was
needed. The deployment is blocked on the installed runtime returning the
confirmed JSON CRUD responses for the user Agent Builder API; Management API
authentication was not used as a workaround.
