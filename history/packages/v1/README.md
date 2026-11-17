# CAD Agent Team Package 1.0

Дата: 2026-11-16. Назначение: настройка четырёх уже созданных LibreChat Agents для инженерной работы в FreeCAD.

## Применение
1. Передай ZIP в workspace `computer-admin`.
2. Отправь Computer: **«Прочитай COMPUTER_TASK.md из приложенного архива и выполни его целиком. Это спецификация архитектора: не создавай новых агентов, не меняй архитектуру. Сделай backup, примени настройки через штатный Agents API/Agent Builder, проверь ACCEPTANCE_TESTS.md и верни один итоговый отчёт».**
3. Computer сам распакует пакет, внесёт изменения и проверит результат. Не нужно вручную копировать промпты по одному.

## Содержимое
- `COMPUTER_TASK.md` — единое задание Computer.
- `MANIFEST.yaml` — целевая конфигурация и известные IDs.
- `MODEL_POLICY.md` — модели и reasoning.
- `MCP_SAFETY.md` — границы FreeCAD MCP.
- `ACCEPTANCE_TESTS.md` — приёмочные проверки.
- `agents/` — четыре полных system prompts.
- `SOURCES.md` — официальные источники.

## Не трогать
`.env`, `CREDS_KEY`, `CREDS_IV`, API-ключ EZ AI, MongoDB напрямую, Docker Compose, TLS, Bearer token, сеть, FreeCAD preferences и документы. Не обновлять LibreChat/Bridge. Не перезапускать контейнеры. Bridge остаётся в `Ask`.

Архитектура: Coordinator — единственный управляющий агент и единственный исполнитель FreeCAD MCP. Analyst, Builder и Reviewer работают с переданными данными, кодом и результатами, но не имеют прямого доступа к живой CAD-сессии.
