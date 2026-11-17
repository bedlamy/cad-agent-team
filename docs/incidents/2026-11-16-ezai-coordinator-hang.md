# CAD Coordinator «Generating» — диагностика зависания (EZ AI), 2026-11-16

Статус: **диагностика завершена, изменений не вносилось.**
Хост: <LAN_HOST_IP> (LibreChat + cad-freecad). Время UTC.

## Симптом

Агент CAD Coordinator (`<COORDINATOR_AGENT_ID>`, provider `ez-ai`,
model `anthropic/claude-sonnet-5.5`) зависает в «Generating» даже на запросе
«Ответь ровно READY». Ранее тот же агент работал.

## Точка зависания (установлена по логам)

Запрос доходит до EZ AI. Провайдер (`https://api.ez-ai.ru/v1`) принимает
`POST /v1/chat/completions`, но не отдаёт поток:

- либо через ~77 с возвращает
  `503 Subscription unavailable (unavailable). Paid OpenRouter fallback is disabled in your subscription settings.`
- либо не отвечает вообще.

LibreChat не имеет таймаута на «тишину» в стриме генерации, поэтому UI остаётся
в «Generating» бесконечно. Срабатывает только watchdog генерации заголовка:
`Title generation timeout` + `#titleConvo Error`.

## Доказательства

1. **Ошибка пришла от провайдера, не от LibreChat.** В сообщении 22:45:01
   сохранён content:
   `{"type":"upstream_model_error","status":503,"message":"503 Subscription unavailable (unavailable). Paid OpenRouter fallback is disabled in your subscription settings."}`
   В `logs/error-2026-11-16.log`:
   `errorCode=UPSTREAM_MODEL_ERROR, errorOrigin=model_provider, errorType=503, traceId=0ce180b4…`
2. **Локально ничего не менялось в окне отказа.** Контейнер `LibreChat`
   `StartedAt=20:39:23`, `RestartCount=0`. Конфиг endpoint `ez-ai`
   (`configs`, principal `__base__`) — `updatedAt=13:17:53`.
   `librechat.yaml` — mtime 20:10:54. Агент — `updatedAt=18:49:15`.
3. **Тот же агент и модель работали за 8 минут до отказа:** завершённые ответы
   22:33:56 и 22:35:34.
4. **Все зависания — `unfinished:true` с пустым `content: []`** (ни текста, ни
   ошибки): 19:00:33, 19:20:35, 22:53:44, 22:55:51, 22:55:54, 22:55:57.
   Два первых — до изменения ACL (22:42:51) и до старта текущего контейнера.
5. **Прямой чат (endpoint `ez-ai`, не агент) зависает так же** — 22:55:07 «тест».
   Значит причина не в агенте, инструментах или Subagents.
6. **MCP не при чём.** MCP Bridge активен: `initialize` с токеном → HTTP 200
   (listener `<FREECAD_CONTAINER_IP>:39280` в cad-freecad). Ранее считался неактивным.
7. **Нет залипших блокировок LibreChat:** `resourcelocks=0`,
   `agentqueuedturns=0`, `generations=0`.
8. **Сеть и доступ в порядке:** DNS `api.ez-ai.ru` → <PUBLIC_IP_REDACTED>, TCP/443 OPEN 2 мс,
   `GET /v1/models` → HTTP 200 за 42 мс, 24 модели, `anthropic/claude-sonnet-5.5`
   присутствует.
9. **Ключ и бюджет не проблема:** `GET /v1/key` → `is_free_tier=false`,
   `limit 18.0700`, `remaining 18.0396`, `expires_at=null`,
   `is_management_key=false`. Метка ключа `API:cad`.

## Что НЕ является причиной

- Изменение POSIX ACL 22:42:51 (`<HOST_CAD_WORKSPACE>`) —
  совпало по времени, но LibreChat этот путь не использует; идентичные
  зависания были в 19:00 и 19:20, до ACL.
- MCP Bridge / инструменты / Subagents.
- Ключ API, баланс, лимиты.
- Залипшие блокировки или очередь внутри LibreChat.

## Возможные действия (не выполнялись, требуют согласования)

1. На стороне EZ AI: проверить статус подписки и включить «Paid OpenRouter
   fallback» в настройках подписки (именно на это указывает текст 503).
2. Временно перевести CAD Coordinator на `deepseek/deepseek-v4.1-flash`
   (как остальные агенты), если этот маршрут не идёт через тот же subscription-роут.
3. Учесть, что при молчащем провайдере LibreChat висит бесконечно — это
   ожидаемое поведение, а не сбой UI.
