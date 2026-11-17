# Агенты, модели и инструкции

## Состав команды

| Роль | Deployment identifier | Модель (последняя известная) | Назначение |
|---|---|---|---|
| CAD Coordinator | `<COORDINATOR_AGENT_ID>` | `anthropic/claude-sonnet-5.5` | Пользовательская точка входа, контекст, маршрутизация, итоговый отчёт |
| CAD Analyst | `<ANALYST_AGENT_ID>` | `deepseek/deepseek-v4.1-flash` | Read-only фактическая инспекция CAD, измерения, выявление противоречий |
| CAD Builder | `<BUILDER_AGENT_ID>` | `deepseek/deepseek-v4.1-flash` | Создание/изменение геометрии, ревизии, экспорт |
| CAD Reviewer | `<REVIEWER_AGENT_ID>` | `deepseek/deepseek-v4.1-flash` | Независимая проверка модели, ревизий и экспортов |

Per-install Agent IDs are intentionally redacted in this public release; role names and model assignments are preserved.

## Роли и границы

### Coordinator

- Единственный пользовательский интерфейс команды.
- Выбирает следующий шаг по состоянию проекта, сложности и риску.
- Не вызывает Analyst автоматически перед каждым ходом.
- По v3 не изменяет геометрию/CAD-документ самостоятельно; передаёт любые такие операции Builder.
- Передаёт subagent ограниченную задачу и минимально достаточный контекст.
- Не заявляет PASS без evidence.

### Analyst

- Независимая read-only инспекция живого документа.
- Проверяет active document, object tree, TypeId, Placement, Shape validity, размеры, объёмы, constraints, feature errors.
- Отделяет факты от гипотез и указывает единицы/источники.
- Не создаёт, не изменяет, не пересчитывает и не сохраняет модель по ролевой инструкции.
- **Ограничение:** read-only не технически enforced; у Analyst есть произвольный Python MCP.

### Builder

- Единственный исполнитель геометрических изменений в команде по v3.
- Сам исследует нужную часть модели, выполняет ограниченную задачу, recompute, проверяет результат.
- Перед изменением обязан сделать before checkpoint; после — after checkpoint.
- Не закрывает/переоткрывает активный документ без необходимости: это может сбросить Undo history.

### Reviewer

- Независимо получает фактические метрики из FreeCAD и проверяет FCStd/STL/STEP.
- Не исправляет модель и не подменяет Builder.
- Проверяет не только Shape validity, но и acceptance criteria, экспорт, hashes, revision log.
- **Ограничение:** read-only не технически enforced; у Reviewer есть произвольный Python MCP.

## Версии prompts

| Версия | Источник | Статус |
|---|---|---|
| v1 | `agents/v1/` | Исходные single-writer prompts, сохранены как история |
| v2 | `agents/v2/` | Исходные prompts из CAD Agent Team Package v2 |
| v3 Coordinator | `agents/v3/coordinator-v3.md` | Точный файл сохранён; SHA совпадает с поздним handoff |
| v3 Analyst/Builder/Reviewer | Не доступны как файлы в текущей Library | Поздний отчёт подтверждает подготовку/применение, но сохранены только SHA-256 |

### SHA-256 v3 prompts из позднего deployment report (17 Nov, 13:22 UTC)

- Analyst: `446097500189ce8b10800e7e8a0c9d697ec6e3ed3f7327f706c7a4cbb3f10d11`
- Builder: `59a3b1ceee388f2f72421af35b17ae5a593356e8b8c7327a5781352217f43abc`
- Coordinator: `916225e9475122888e059f8f6e68baba7ac3bbb238646dfaa51567147fec0ea4`
- Reviewer: `45ebf3643ebd6cb48cca2174d54e99a927d855be1ca7ede46d10bfb6225d8877`

Не пытаться восстановить недостающие тексты из hash. Получить их из live Agent Builder или исходного workspace и сверить hash.

## MCP tools

- Сервер возвращает `execute_python`, `execute_python_file`, `get_output_page`.
- LibreChat aliases: `execute_python_mcp_freecad`, `execute_python_file_mcp_freecad`, `get_output_page_mcp_freecad`.
- Явный toolset v2: `execute_python_mcp_freecad` + `get_output_page_mcp_freecad`.
- `execute_python_file_mcp_freecad` исключён из явного MVP toolset.
- В одном успешном runtime Coordinator видел `subagent` плюс MCP tools; `subagent` динамически предоставляется LibreChat.

Перед изменениями проверить текущий runtime toolset, не полагаться только на MongoDB snapshot.
