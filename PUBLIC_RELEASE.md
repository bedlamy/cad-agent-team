# Public release and redaction notes

This repository is intentionally public. The 2026-11-17 archive was prepared from project documents and handoffs, then sanitized for publication.

## Redacted or omitted

- LAN and Docker-network IP addresses, public host addresses, and host-specific service endpoints.
- Per-install LibreChat Agent IDs, conversation/message IDs, UUIDs, and tool-call identifiers.
- Host-specific data roots and container filesystem paths where they reveal the installation layout. Generic `/projects` paths remain in reusable code/examples where they are part of the documented interface.
- The raw 2026-11-17 conversation/tool export. It contained a full execution trace, filesystem enumeration output, local file paths, and details of a customer CAD package. The aggregate statistics and behavior findings are preserved in the anonymized incident report.
- The customer CAD archive, source STEP files, prototype photo, design renders, and customer-specific engineering handoff.
- Original ZIP copies that contained the unredacted handoff. Public source bundles are rebuilt from sanitized extracted files.

## What remains

The repository retains reusable agent prompts, Skills, revision tooling, acceptance criteria, architecture decisions, reported deployment versions, generalized topology, and anonymized incident evidence. The original source artifacts remain identifiable by their source names and checksums where documented, but the published bundles are not byte-for-byte copies.

## Secrets policy

Never commit API keys, bearer tokens, passwords, cookies, private keys, `.env` files, database dumps, or unredacted service logs. A role prompt saying read-only is not a technical sandbox; FreeCAD MCP Python execution must be treated as privileged access to the FreeCAD process.

## License

No license file is included. Until the repository owner selects a license, reuse rights are not granted merely by making the repository public.
