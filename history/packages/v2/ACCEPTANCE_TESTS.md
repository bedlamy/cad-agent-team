# Acceptance tests — CAD Team v2

## A. Config
- [ ] Ровно четыре existing agents, IDs проверены, нет дубликатов.
- [ ] Полные system prompts совпадают с пакетом.
- [ ] Каждый агент имеет `execute_python_mcp_freecad` и `get_output_page_mcp_freecad`.
- [ ] Coordinator имеет native Subagents tool, и настройки allowlist содержат ровно три специалиста.
- [ ] EZ AI модели реальны и способны на tool calling; если нет, выбран подтверждённый fallback.
- [ ] Bridge mode не изменён без отдельного согласия пользователя.

## B. Versioning
- [ ] `/projects` — persistent mount; ревизии переживают перезапуск контейнера.
- [ ] Helper установлен, автономные mock tests прошли.
- [ ] На **отдельном тестовом документе** через FreeCAD созданы `before` и `after` FCStd.
- [ ] Оба FCStd проходят ZIP integrity check и открываются в FreeCAD.
- [ ] `doc.FileName` рабочего документа не поменялся после `saveCopy`.
- [ ] В `revision_log.json` две записи с различными IDs/path/hash.
- [ ] После успешного изменения обновлён `project_state.json`.
- [ ] Исходный пользовательский STEP/FCStd не изменён.

## C. Workflow
- [ ] Coordinator не вызывает Analyst для тривиальной известной правки.
- [ ] Analyst самостоятельно делает read-only MCP инспекцию (не через Coordinator как исполнителя).
- [ ] Builder самостоятельно выполняет тестовую правку после before checkpoint.
- [ ] Reviewer самостоятельно получает фактические метрики через MCP после Builder.
- [ ] Субагенты и координатор не делают параллельные изменения общей модели.
- [ ] После изменения существует after checkpoint.
- [ ] На ошибки инструментов агенты реагируют по фактическим status/result, не придумывают успех.

## D. Autonomy
- [ ] Пока Bridge Ask: фиксируем, что каждое выполнение Python требует ручного Run/Allow.
- [ ] Только после информированного решения пользователя: Unrestricted позволяет исполнять Python без диалога; это доверие всем 4 MCP-агентам.
- [ ] Не путать инструкцию read-only с техническим запретом записи.
- [ ] Без rollback и проверки snapshot не переводить рабочую систему в постоянную автономную эксплуатацию.
