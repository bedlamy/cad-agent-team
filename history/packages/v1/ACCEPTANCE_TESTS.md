# Acceptance tests

## 1. Agent records
- [ ] Найдены ровно четыре существующих агента.
- [ ] IDs/name совпадают с manifest либо расхождение разрешено однозначно.
- [ ] Instructions совпадают с файлами пакета.
- [ ] Provider всех четырёх — `ez-ai`.
- [ ] Все model IDs присутствуют в live catalog.
- [ ] Reasoning выставлен только при доказанной поддержке.
- [ ] Дубликатов нет.

## 2. Subagents
- [ ] Coordinator: `subagents.enabled=true`.
- [ ] `allowSelf=false`, `shareFiles=true`.
- [ ] Allowlist содержит ровно Analyst, Builder, Reviewer.
- [ ] Native Subagents Tool Library card действительно прикреплена. Проверить отдельно от settings object.
- [ ] Agent Chain не используется.

## 3. MCP least privilege
- [ ] Coordinator имеет FreeCAD MCP `execute_python` и `get_output_page`.
- [ ] `execute_python_file` не выбран, если per-tool selection доступен.
- [ ] Analyst/Builder/Reviewer не имеют FreeCAD MCP.
- [ ] Bridge остаётся Ask; Unrestricted и auto-approval выключены.

## 4. Delegation
Через Coordinator без MCP-вызовов выполнить содержательный тест:
- Analyst анализирует переданный простой структурированный CAD snapshot.
- Builder готовит параметрический план детали и описывает код, но не исполняет.
- Reviewer независимо проверяет план и указывает недостающие критерии.
Подтвердить отдельный вызов каждого subagent, полезный результат и синтез Coordinator. Ответ «агент на связи» не считается достаточным.

## 5. FreeCAD read-only smoke test
Только если MCP доступен. Код должен быть только такого смысла:

```python
doc = App.ActiveDocument
print("DOCUMENT", doc.Name if doc else None)
if doc:
    print("OBJECT_COUNT", len(doc.Objects))
    for obj in doc.Objects:
        print(obj.Name, obj.Label, obj.TypeId)
```

Не добавлять create/delete/change/recompute/save/open/close/file/network/shell operations. Ask должен показать код. Computer не нажимает Allow автоматически. `DOCUMENT None` — нормальный результат, не открывать и не создавать документ.

## 6. Final
Отчёт содержит backup path, agent IDs, models, reasoning status, tools/subagents status, delegation test, smoke test, ограничения. Ни одного секрета в отчёте. Контейнеры не перезапускались, MongoDB напрямую не менялась.
