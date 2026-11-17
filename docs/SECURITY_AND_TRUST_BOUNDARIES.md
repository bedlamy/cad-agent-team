# Security and trust boundaries

## Critical fact: MCP is not a sandbox

FreeCAD MCP Bridge exposes `execute_python` in the live FreeCAD process. This grants arbitrary Python execution in that process. A role prompt saying “read-only” does not technically prevent mutation, filesystem access or other Python operations.

`Unrestricted` removes per-call Allow prompts; it does not reduce Python capabilities. It means the user has chosen to trust all connected models/tools with the same FreeCAD session.

## Current role safety

- Analyst and Reviewer are logically read-only by prompt/Skills.
- Builder is the intended geometry writer.
- Coordinator has direct MCP but v3 says not to mutate geometry itself.
- The single shared GUI session requires serialized operations.

## Guardrails in v3

- no shell/subprocess/network from FreeCAD Python;
- do not touch credentials, TLS, Docker, plugins, FreeCAD preferences or unrelated files;
- only project data under `/projects`;
- do not overwrite source STEP/FCStd;
- mandatory before/after checkpoints for mutation;
- no parallel mutating MCP calls.

These are prompt-level guardrails, not enforcement at the Bridge layer.

## Secrets excluded from Git

Never commit `.env`, `CREDS_KEY`, `CREDS_IV`, `JWT_SECRET`, `JWT_REFRESH_SECRET`, EZ AI API keys, MCP Bearer token, TLS private key, browser cookies/session credentials, MongoDB backups, credential exports or raw service logs containing secrets.

The archived handoff contains only secret names and configuration descriptions, not secret values. The protected backup itself is not included.

## Filesystem policy from user

- one shared CAD Workspace;
- preserve existing owners;
- no `chmod 777`;
- no blind recursive `chown`;
- no per-project permissions as a permanent architecture;
- future inheritance/default ACL was a desired policy, but current live ACL needs verification.
