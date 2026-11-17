# Официальные источники

Проверены 2026-11-16.

- LibreChat Agents: https://www.librechat.ai/docs/features/agents
  Создание агента, system instructions, model settings, Tool Library, MCP, approvals и subagents.
- LibreChat Subagents: https://www.librechat.ai/docs/features/subagents
  Отдельный контекст дочернего агента; `enabled`, `allowSelf`, `agent_ids`.
- LibreChat Custom Endpoint Object Structure: https://www.librechat.ai/docs<FREECAD_CONFIG_ROOT>uration/librechat_yaml/object_structure/custom_endpoint
  `customParams.reasoningFormat`: `reasoning_effort`, `reasoning_object`, `disabled`.
- LibreChat Model Specs: https://www.librechat.ai/docs<FREECAD_CONFIG_ROOT>uration/librechat_yaml/object_structure/model_specs
  `reasoning_effort` и provider-specific параметры.
- FreeCAD MCP Bridge: https://github.com/CREATeNG/freecad-mcp-bridge
  `execute_python`, `execute_python_file`, `get_output_page`; Ask/Unrestricted; выполнение кода в живой сессии FreeCAD.

Архитектурные выводы:
- Subagents работают в отдельном контексте и возвращают результат родителю.
- Проверять нужно и subagents settings, и наличие native Subagents tool card.
- FreeCAD `execute_python` — не read-only sandbox. Поэтому применяется single-writer модель: MCP только у Coordinator.
- `reasoning_effort` не включается для EZ AI наугад: сначала проверяется фактический `reasoningFormat`.
