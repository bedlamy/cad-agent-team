# v3 prompt set — provenance and gaps

The later 2026-11-17 deployment report records these SHA-256 values for four v3 prompts, prepared from v2 prompts plus role addenda:

| Role | File | SHA-256 | Availability here |
|---|---|---|---|
| Analyst | `analyst-v3.md` | `446097500189ce8b10800e7e8a0c9d697ec6e3ed3f7327f706c7a4cbb3f10d11` | Source text not present in current Library snapshot |
| Builder | `builder-v3.md` | `59a3b1ceee388f2f72421af35b17ae5a593356e8b8c7327a5781352217f43abc` | Source text not present in current Library snapshot |
| Coordinator | `coordinator-v3.md` | `916225e9475122888e059f8f6e68baba7ac3bbb238646dfaa51567147fec0ea4` | Included; local SHA-256 verified against report |
| Reviewer | `reviewer-v3.md` | `45ebf3643ebd6cb48cca2174d54e99a927d855be1ca7ede46d10bfb6225d8877` | Source text not present in current Library snapshot |

Do not synthesize missing prompts from the v2 prompt plus addendum. The resulting hashes do not match naive concatenation, and the exact merge/edit process is unknown. Retrieve the actual prompt bodies from LibreChat Agent Builder or the original `/workspaces/computer-admin/.build/cad-skills-v0.1-review/v3-prompts/` workspace, then verify SHA-256 before using them.

`coordinator-v3.md` is the exact available file. It changes v2 routing by requiring every geometry/CAD document mutation to go through Builder and calling Analyst when the document/geometry state is unknown, changed or contradictory.
