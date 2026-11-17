# Prompt для нового чата — продолжение CAD Agent Team

Мы продолжаем проект CAD Agent Team. Сначала изучи репозиторий целиком по индексам, особенно:

- `docs/00_START_HERE.md`
- `docs/CURRENT_STATE_2026-11-17.md`
- `docs/ARCHITECTURE.md`
- `docs/AGENTS_AND_PROMPTS.md`
- `docs/ORCHESTRATION_AND_ROUTING.md`
- `docs/INFRASTRUCTURE.md`
- `docs/VERSIONING.md`
- `docs/SKILLS.md`
- `docs/KNOWN_GAPS.md`
- `docs/incidents/2026-11-17-coordinator-overrun-summary.md`

Считай документы архивным baseline, не live truth. Различай подтверждённое, сообщённое, план, неизвестное и конфликт.

Текущий важный инцидент: CAD Coordinator получил read-only задачу изучить external CAD package, но потратил значительное время на собственные повторные измерения, не вызвал Analyst, не смог открыть изображения и не завершил отчёт. Сырой execution trace не публикуется; его агрегированные результаты сохранены в incident summary. В нём 24 tool calls, 17 FreeCAD MCP, 5 failed read_file, 2 output-page, 0 Subagent calls. Предыдущий разбор в чате ошибочно посчитал 26/19 — использовать исправленную статистику из документа.

Не начинай исправлять prompts/Skills/tools/модели/MCP/ACL или перезапускать сервисы. Сначала предложи read-only план проверки live состояния и дождись отдельного согласования на любые изменения.

Особенно важно: не восстанавливай отсутствующие Analyst/Builder/Reviewer v3 prompts из hash. Получи точные live prompt texts и сверяй SHA. Не меняй рабочие CAD-документы.
