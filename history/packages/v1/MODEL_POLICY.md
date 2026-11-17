# Model policy

## Специалисты
Для Analyst, Builder и Reviewer использовать `ez-ai / deepseek/deepseek-v4.1-flash`, если точный ID присутствует в текущем каталоге. Этот ID был подтверждён предыдущей авторизованной проверкой каталога и использован при создании специалистов.

Reasoning targets, только если EZ AI и Agent Builder поддерживают настройку:
- Analyst: `low`
- Builder: `medium`
- Reviewer: `medium`

## Coordinator
Это главный reasoning-узел: разбивает задачу, выбирает стратегию, синтезирует ответы специалистов, принимает инженерные решения и контролирует FreeCAD.

Приоритет по текущему live-каталогу EZ AI:
1. Display label `GPT-6.1 Sol`, если он действительно присутствует в каталоге (точный ID взять из каталога).
2. Exact ID `anthropic/claude-sonnet-5.5`, если он присутствует в каталоге. Он был назначен ранее, но доступность не была проверена.
3. Display label `GPT-6 Astra`, если присутствует.
4. Fallback `deepseek/deepseek-v4.1-flash`.

Не угадывать ID по названию. Provider остаётся `ez-ai`. Reasoning target Coordinator — `high`, но только если подтверждена поддержка.

## Reasoning — важное ограничение
LibreChat умеет передавать `reasoning_effort` custom OpenAI-like endpoints, но формат зависит от `customParams.reasoningFormat` (`reasoning_effort`, `reasoning_object` или `disabled`). Сам факт наличия параметра в LibreChat не доказывает, что EZ AI его принимает.

Поэтому:
- сначала прочитать текущую конфигурацию EZ AI;
- если `reasoningFormat` не задан или неизвестен — оставить reasoning unset;
- не менять endpoint global config, `customParams`, `reasoningFormat` или `interface.parameters`;
- не делать платный test completion;
- не менять temperature/context/max output без причины.
