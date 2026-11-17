# EZ AI provider, streaming and cost notes

## Endpoint

- LibreChat endpoint key: `ez-ai`.
- Base URL: `https://api.ez-ai.ru/v1`.
- OpenAI-compatible custom endpoint.

## 16 Nov Coordinator hang

The archived diagnostic report says `POST /v1/chat/completions` reached EZ AI but the provider sometimes returned after ~77 seconds:

`503 Subscription unavailable (unavailable). Paid OpenRouter fallback is disabled in your subscription settings.`

Other times the stream did not respond. LibreChat had no timeout for a silent generation stream, so UI could remain “Generating”. The same behavior happened in direct chat and agent chat; MCP/Subagents were not the root cause in that incident. Report says API key/balance were not the cause.

See `docs/incidents/2026-11-16-ezai-coordinator-hang.md`.

## Cost display

`interface.contextUsage=true` and `interface.contextCost=true` were enabled. `tokenConfig` was not added because EZ AI rates were not reliably verified. Do not substitute upstream Anthropic/DeepSeek prices as EZ AI rates.

## 17 Nov overrun

User-reported spend was approximately 100 RUB before stopping the run. The source execution trace contained tool calls and reasoning text but did not include exact billed tokens, a tariff snapshot, or a billing ledger. The raw trace is not published; exact charge attribution cannot be reconstructed from the preserved aggregate evidence.

The correct technical lesson is not “FreeCAD calls are expensive”; most observed wall-clock time was local tool execution, while model cost likely came from repeated long reasoning/context and very large tool outputs. Billing data is required to quantify the exact split.
