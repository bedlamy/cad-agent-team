# COMPUTER TASK — применить CAD Agent Team Package

Ты — исполнитель. Архитектура, роли, промпты, модели и права доступа уже определены в этом архиве. Не переосмысливай их.

## 0. Распаковка
Распакуй ZIP во временную папку workspace `computer-admin`. Прочитай полностью README, MANIFEST, MODEL_POLICY, MCP_SAFETY, ACCEPTANCE_TESTS и все четыре файла `agents/*.md`. Это пакет инструкций, не запускай его как инсталлятор.

## 1. Read-only preflight
Последняя подтверждённая конфигурация:
- LibreChat `v0.8.9-rc1` (проверь фактическую версию, не обновляй);
- custom endpoint `ez-ai`;
- MCP server `freecad`;
- FreeCAD MCP Bridge `0.1.30`;
- FreeCAD `<FREECAD_CONTAINER_IP>:39280`, LibreChat API `<LIBRECHAT_CONTAINER_IP>`, сеть `cad_mcp`;
- Bridge Permission mode `Ask`;
- известные tool keys: `execute_python_mcp_freecad`, `execute_python_file_mcp_freecad`, `get_output_page_mcp_freecad`.

Проверь фактическое состояние read-only. Не меняй инфраструктуру ради совпадения с этими значениями.

### Найти агентов
Используй штатный пользовательский API/Agent Builder, не Management API и не прямую MongoDB:
- CAD Analyst — `<ANALYST_AGENT_ID>`
- CAD Builder — `<BUILDER_AGENT_ID>`
- CAD Reviewer — `<REVIEWER_AGENT_ID>`
- CAD Coordinator — `<COORDINATOR_AGENT_ID>`

Проверь IDs и точные имена. Если ID изменился — найди по точному имени. Если есть дубликаты/неоднозначность — остановись. Новых агентов не создавай.

### Backup обязателен до первой записи
Создай `<LIBRECHAT_CONFIG_ROOT>/backups/agent-team-preapply-<timestamp>/` (или фактический каталог backup LibreChat) и сохрани безопасные JSON-экспорты четырёх агентов, expanded representations и метаданные tools/subagents/models. Удали из backup секретные поля. Не включай `.env`, ключи, cookies, JWT, Bearer token, private keys или connection strings. Проверь, что backup читается и содержит все четыре агента.

## 2. Проверить модели
Получить актуальный каталог моделей EZ AI через реальный авторизованный маршрут установленной версии. Не угадывать URL; сверить с маршрутами/клиентским кодом или ранее использованным рабочим методом. Не выводить ключ.

Специалисты: подтвердить `deepseek/deepseek-v4.1-flash` (этот ID уже был возвращён каталогом в предыдущей сессии).

Coordinator: приоритет выбора из `MODEL_POLICY.md`, точный model ID брать только из актуального каталога. Ранее `anthropic/claude-sonnet-5.5` был записан в create payload, но тогда не был подтверждён каталогом. Не считать его доступность доказанной.

Не выполнять платный Chat Completion ради проверки модели.

Reasoning: проверь фактический `customParams.reasoningFormat` endpoint `ez-ai` и поддержку параметра выбранной моделью. Если формат неизвестен/не задан — оставь reasoning unset. Не меняй `librechat.yaml`, endpoint `customParams`, `reasoningFormat`, `interface.parameters` или глобальные настройки EZ AI.

## 3. Обновить существующие агенты
Вставь полные тексты из:
- `agents/CAD_COORDINATOR.md`
- `agents/CAD_ANALYST.md`
- `agents/CAD_BUILDER.md`
- `agents/CAD_REVIEWER.md`

Не сокращай промпты и не заменяй их своими версиями. Обнови descriptions. Добавь starters Coordinator, если поле поддерживается, не удаляя полезные metadata.

Provider всех агентов остаётся `ez-ai`. Модели и reasoning — строго по MODEL_POLICY.md.

## 4. Инструменты и права
### Coordinator
Должен иметь:
- native Tool Library card **Subagents**;
- MCP `freecad` tools: `execute_python_mcp_freecad`, `get_output_page_mcp_freecad`.

`execute_python_file_mcp_freecad` по умолчанию не подключать: это дополнительный путь запуска локального файла. Если версия не позволяет выбирать tools отдельно, оставь штатную конфигурацию сервера, не обходи это MongoDB-правкой и укажи ограничение.

Subagents:
```yaml
enabled: true
allowSelf: false
shareFiles: true
agent_ids:
  - <ANALYST_AGENT_ID>
  - <BUILDER_AGENT_ID>
  - <REVIEWER_AGENT_ID>
```
Если IDs изменились, используй только фактически подтверждённые IDs по точным именам.

Проверь обе части: subagents settings включены И native Subagents tool реально прикреплён. В предыдущей конфигурации сначала сохранялся subagents object, затем tools PATCH массивом MCP keys; возможно, native Subagents tool был потерян.

### Analyst, Builder, Reviewer
Убрать у них все tools сервера `freecad`. Не удалять unrelated tools без причины. Не добавлять shell, Code Interpreter, filesystem, Actions, другие MCP или Skills.

Причина: `execute_python` — произвольный Python в живом процессе FreeCAD; текстовый запрет не превращает его в read-only инструмент. Поэтому единственный исполнитель — Coordinator.

### Не включать
Unrestricted, allowSelf, Agent Chain, auto-approval, background MCP, дополнительные MCP servers, Skills/Actions.

## 5. Внести изменения
Только через штатный пользовательский Agents API/Agent Builder (`PATCH /api/agents/{id}` или фактический update route версии). Сначала backup. Используй точечные поля и сохраняй несвязанные metadata. После каждого PATCH перечитай объект и проверь.

Не меняй MongoDB напрямую. Не меняй credentials, `.env`, Compose, TLS, token, сеть, FreeCAD preferences. Не перезапускай контейнеры.

Если PATCH одного агента провалился — остановись и откати уже изменённые записи через штатный API из backup. Не продолжай частично.

## 6. Тесты
Выполни `ACCEPTANCE_TESTS.md`. Сначала API/read-only, затем содержательная делегация Coordinator → каждый из трёх специалистов без MCP вызовов. FreeCAD smoke test — только read-only. Если Ask показывает диалог, Computer не нажимает Allow автоматически. Если нет активного документа, результат `DOCUMENT None` нормален.

## 7. Отчёт
Сохрани `reports/cad-agent-team-deployment-2026-11-16.md` в workspace. Укажи IDs, provider/models, reasoning, Subagents settings и tool card, MCP tools Coordinator, отсутствие FreeCAD MCP у специалистов, результаты делегации, read-only smoke test, backup path, расхождения и ограничения. Секреты не включать.

Задача завершена только после повторного чтения API и подтверждения целевого состояния.
