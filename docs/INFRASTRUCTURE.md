# Infrastructure — archived deployment profile (redacted)

> Historical report only; not a live inventory. Network addresses, host-specific paths, and per-install identifiers were intentionally removed for this public release.

## Runtime layout

- Hypervisor: Proxmox.
- Guest: Debian Linux VM; reported profile was 2 vCPU and 4 GiB RAM.
- CPU passthrough (`host`) was enabled; AVX/AVX2 were reported available in the guest.
- Persistent CAD/Docker data was placed on a dedicated host data volume.

## LibreChat stack

- LibreChat `v0.8.9-rc1`.
- MongoDB `8.0.20`.
- Meilisearch `v1.35.1` in the deployment report.
- PostgreSQL/pgvector and RAG API; exact image tags were not recorded.
- Admin Panel enabled.
- Compose project contained separate API, database, search, vector, and RAG services.

## Network topology

A dedicated Docker network `cad_mcp` was created for stable service-to-service addressing. FreeCAD and LibreChat API used static container addresses; the MCP listener was published on the LAN host interface. Exact addresses and port-to-host mappings are intentionally redacted. MongoDB, Meilisearch, PostgreSQL, and RAG API were not published externally in the reported configuration.

## FreeCAD MCP Bridge

- Upstream project: https://github.com/CREATeNG/freecad-mcp-bridge
- Version: `v0.1.30`.
- Transport: TLS + Bearer token.
- Reported handshake: `initialize` HTTP 200, `notifications/initialized` HTTP 202, `tools/list` HTTP 200.
- Bridge was enabled manually from the FreeCAD status bar; autostart was not implemented in the inspected version.
- Permission mode was reported as `Unrestricted` after explicit user selection. This is a trust decision, not a sandbox.

## Provider

- LibreChat custom endpoint name: `ez-ai`.
- Base URL: `https://api.ez-ai.ru/v1`.
- OpenAI-compatible endpoint.
- Exact tariffs, tokenConfig, and model-specific reasoning behavior were not verified.

## Workspace and revision helper

- Intended CAD workspace: `/projects/cad-agent-projects` (adapt this path to the local deployment).
- Revision helper was installed under a hidden helper directory adjacent to `/projects`.
- A historical permission issue blocked the FreeCAD process user from creating workspace folders. Later reports claimed an ACL was applied, but the archive does not contain sufficient live ACL evidence. Treat permissions as unknown until checked.
