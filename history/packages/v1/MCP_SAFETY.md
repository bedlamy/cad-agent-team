# FreeCAD MCP safety and role boundaries

## Почему доступ только у Coordinator
FreeCAD MCP Bridge exposes:
- `execute_python(code)` — Python исполняется в живой сессии FreeCAD;
- `execute_python_file(filepath)` — локальный Python-файл исполняется в том же контексте;
- `get_output_page(job_token, page_no)` — получение продолжения вывода.

Это не read-only API и не sandbox. Текстовая инструкция «не изменять модель» не является техническим ограничением.

## Single-writer architecture
Только Coordinator имеет FreeCAD MCP. Analyst, Builder и Reviewer получают snapshots/метрики/код/результаты от Coordinator и не имеют прямого инструмента изменения.

- Analyst: читает переданные данные.
- Builder: проектирует и готовит код, но не исполняет.
- Reviewer: независимо проверяет требования, код и фактические результаты, но не исполняет.
- Coordinator: единственный исполнитель и единственный writer.

## Минимальный набор Coordinator
Подключить:
- `execute_python_mcp_freecad`
- `get_output_page_mcp_freecad`

Не подключать по умолчанию `execute_python_file_mcp_freecad`. Если версия LibreChat не поддерживает per-tool selection, не редактировать MongoDB ради обхода; оставить штатный вариант и записать ограничение.

## Правила Coordinator
1. Сначала проверить `App.ActiveDocument`; не считать, что документ открыт.
2. Один MCP вызов за раз; никаких параллельных мутаций.
3. Отделять read-only запросы от изменяющих.
4. Не выполнять shell, subprocess, network, произвольный filesystem I/O или чтение secrets из Python FreeCAD.
5. Не открывать/закрывать/создавать/сохранять документы без прямого основания.
6. Не перезаписывать оригинал; путь/имя нового файла согласовать.
7. Не менять preferences, plugins, macros, startup, undo settings.
8. Не выключать undo и не манипулировать undo stack.
9. Для изменений заранее описать план и ожидаемые объекты/параметры.
10. Bridge остаётся `Ask`; пользователь сам нажимает Allow/Run после просмотра кода.
11. Не переключать в Unrestricted и не автоматизировать подтверждения.
12. После изменения получить фактические метрики и передать их Reviewer.
13. Не утверждать об успехе без результата инструмента и проверки.

## Workflow
Inspect → Analyst snapshot review → Builder design/code → Reviewer preflight → Coordinator executes after Ask → Coordinator collects facts → Reviewer post-check → report.

Если MCP недоступен или документ не открыт, сообщить это, не выдумывать результат и не создавать документ ради теста.
