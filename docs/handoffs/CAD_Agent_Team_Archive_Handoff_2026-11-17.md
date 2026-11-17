# CAD Agent Team --- архивный технический handoff

**Дата подготовки:** 17 ноября 2026\
**Назначение:** передача проекта в новый координационный чат.\
**Основа:** только доступная история этого чата, три вложенных скриншота
и отчёты Computer/LibreChat, процитированные в переписке.\
**Режим подготовки:** архивное извлечение; подключений к VM, новых
генераций, изменений конфигурации и перезапусков не выполнялось.

------------------------------------------------------------------------

## 0. Границы достоверности и правила чтения

### 0.1. Доступные источники

В доступном контексте присутствуют последовательные сообщения
пользователя и отчёты Computer о dedicated VM, LibreChat, EZ AI, FreeCAD, MCP,
агентах и тестах. В текущих файлах чата обнаружены три пользовательских
изображения:

1.  `image(20261116-163301).png` --- окно Preferences → MCP Bridge в
    FreeCAD.
2.  `image(20261116-193525).png` --- зависший запрос CAD Coordinator.
3.  `image(20261116-210043).png` --- успешный вызов CAD Analyst из
    Coordinator с открытой дочерней панелью.

**Не обнаружены среди файлов текущего чата:** исходники
`cad_revision.py`, Docker Compose, `librechat.yaml`, `.env`, `user.cfg`,
экспорт MongoDB, JSON-экспорт агентов, ZIP с промптами/Skills,
FCStd/STL/STEP-файлы и журналы сервера. Эти файлы могли существовать на
dedicated VM, но их оригиналы не были приложены к текущему чату и не доступны
в текущем рабочем окружении.

История чата частично представлена пропусками/свернутыми блоками.
Поэтому документ максимально полно фиксирует доступные сведения, но **не
является гарантированно исчерпывающей расшифровкой каждого раннего
сообщения или каждого выполненного shell-командного вызова**.

### 0.2. Статусы

-   **ПРИНЯТОЕ РЕШЕНИЕ** --- пользователь явно согласился или прямо
    установил требование.
-   **ВЫПОЛНЕНО** --- действие, согласно отчёту Computer, было
    совершено.
-   **ПРОВЕРЕНО** --- результат подтверждён проверкой, описанной в
    отчёте или видимой на скриншоте.
-   **ВЫПОЛНЕНО, НО НЕ ПРОВЕРЕНО** --- действие заявлено как
    выполненное, но проверка результата отсутствует.
-   **НЕУДАЧНАЯ ПОПЫТКА** --- попытка завершилась ошибкой или не дала
    результата.
-   **ПРЕДЛОЖЕНИЕ / ПЛАН** --- идея или следующий шаг; не считать
    реализованным.
-   **НЕИЗВЕСТНО** --- значение отсутствует, не было прочитано или не
    подтверждено.

Большинство серверных операций известны из отчётов Computer, а не из
прямого доступа к серверу при подготовке этого документа. Там, где есть
только отчёт, это отмечено.

### 0.3. Нельзя домысливать

Не установлены: точная версия FreeCAD; GID пользователя FreeCAD;
фактические ACL всего CAD Workspace; точный состав bind mounts FreeCAD
Compose; полный текст системных инструкций четырёх агентов; полный
исходник и API `cad_revision.py`; полный авторизованный каталог EZ AI;
тарифы и context window моделей EZ AI; наличие или настройки LibreChat
Skills.

------------------------------------------------------------------------

# 1. Краткий паспорт проекта

## 1.1. Цель

CAD Agent Team --- специализированная инженерная команда на базе
LibreChat, FreeCAD и MCP, использующая EZ AI как внешний модельный
endpoint. Цель --- не четыре независимых чата с разными названиями, а
команда, которая получает инженерную задачу, координирует её выполнение,
исследует фактическое состояние CAD-документа при необходимости,
поручает моделирование Builder, передаёт результат на независимую
проверку Reviewer, сохраняет проект и ревизии и возвращает пользователю
проверяемый результат.

## 1.2. Основные компоненты

  --------------------------------------------------------------------------------
  Компонент                           Зафиксированное состояние
  ----------------------------------- --------------------------------------------
  Гипервизор                          Proxmox; рабочая VM --- `121`

  VM                                  Debian, 2 vCPU, 4096 MiB RAM

  CPU VM                              `cpu: host`; AVX и AVX2 видны внутри гостя

  LibreChat                           `v0.8.9-rc1`

  MongoDB                             `8.0.20`

  Meilisearch                         в отчёте pull фигурировал `v1.35.1`

  PostgreSQL                          PostgreSQL/pgvector; точный tag не
                                      зафиксирован

  RAG API                             запущен; точная версия не зафиксирована

  FreeCAD                             Docker-контейнер `cad-freecad`; точная
                                      версия приложения неизвестна

  FreeCAD MCP Bridge                  `v0.1.30`

  Внешний endpoint                    `ez-ai`, Base URL `https://api.ez-ai.ru/v1`

  CAD Workspace                       `<CAD_WORKSPACE>`

  Revision helper                     `<CAD_AGENT_HOME>/bin/cad_revision.py`
  --------------------------------------------------------------------------------

## 1.3. Сеть и порты

  Назначение                        Адрес
  --------------------------------- ----------------------------
  LibreChat API / чат               `http://<LAN_HOST_IP>:3080/`
  LibreChat Admin Panel             `http://<LAN_HOST_IP>:3000/`
  FreeCAD web/HTTPS endpoint        `https://<LAN_HOST_IP>:3001/`
  LAN-публикация MCP                `<LAN_HOST_IP>:39280`
  FreeCAD в Docker-сети `cad_mcp`   `<FREECAD_CONTAINER_IP>`
  LibreChat API в `cad_mcp`         `<LIBRECHAT_CONTAINER_IP>`
  MCP listener FreeCAD              `<FREECAD_CONTAINER_IP>:39280`

Порты 3000, 3080, 3001 и 39280 публиковались на LAN-адрес `<LAN_HOST_IP>`,
а не на `0.0.0.0`, согласно отчётам настройки. WAN-настройки не
изменялись.

## 1.4. Последнее известное состояние

  -----------------------------------------------------------------------
  Область                             Последний известный статус
  ----------------------------------- -----------------------------------
  LibreChat                           запущен, API отвечает

  Admin Panel                         доступна

  EZ AI                               пользователь вручную отправлял
                                      запрос и получил ответ; обычный чат
                                      фактически работает

  Четыре агента                       созданы, обновлены инструкциями v2

  Subagents                           Coordinator → Analyst реально
                                      сработал в нескольких тестах

  MCP                                 handshake и инструменты работают

  Bridge                              активен; пользователь вручную
                                      переключил режим Unrestricted

  MCP PermissionMode                  в активном GUI-профиле подтверждено
                                      значение `1` = Unrestricted

  Analyst                             подтверждены успешный прямой
                                      MCP-анализ и успешный
                                      Subagent-запуск

  Builder                             создал реальный XYZ Calibration
                                      Cube

  Reviewer                            независимо проверил куб и STL

  Ревизии куба                        **не завершены**: файлы пока лежат
                                      в `<TEMP_DIR>`, целевой каталог
                                      недоступен на запись

  CAD Workspace permissions           блокер:
                                      `<CAD_WORKSPACE>`
                                      принадлежит `root:root`, mode
                                      `0755`; FreeCAD UID `1000` не может
                                      создать подкаталог

  Skills                              создание/назначение в доступной
                                      истории не подтверждено

  Глобальные ACL                      не подтверждены; целевое решение
                                      описано пользователем в запросе
                                      архивного извлечения, применение не
                                      подтверждено
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 2. Инфраструктура: VM, Docker, диски

## 2.1. dedicated VM

По отчётам Computer: - VM ID: `121`; - ОС: Debian; - CPU: 2 vCPU; - RAM:
4096 MiB; - первоначальная виртуальная CPU-модель не предоставляла
AVX; - после согласованного изменения установлено `cpu: host`; - внутри
Debian проверены AVX и AVX2.

Изменение CPU-модели было сделано, чтобы использовать штатный MongoDB 8
из LibreChat Compose. После переключения MongoDB 4.4.18 override больше
не требовался.

## 2.2. Диски и миграция CAD data

До миграции старый диск был подключён как `scsi1`, volume
`local:121/vm-121-disk-0.qcow2`, номинальный размер 20 GiB.

После миграции:

  ---------------------------------------------------------------------------------------------
  Слот             Volume                                               Размер Назначение
  ---------------- ------------------------------------- --------------------- ----------------
  `scsi0`          `local:121/vm-121-disk-1.qcow2`                      12 GiB Debian

  `scsi2`          `media-hdd:121/vm-121-disk-0.qcow2`                 100 GiB CAD data /
                                                                               Docker data
  ---------------------------------------------------------------------------------------------

Новый раздел: - устройство в госте: `/dev/sdc1`; - UUID:
`<UUID_REDACTED>`; - точка монтирования:
`<HOST_DATA_ROOT>`.

После reboot проверено: - новый UUID автоматически смонтирован в
`<HOST_DATA_ROOT>`; - старый UUID отсутствует в активном `/etc/fstab`; -
Docker и containerd стартуют автоматически; - Docker Root Dir:
`<DOCKER_ROOT>`; - containerd root: `<CONTAINERD_ROOT>`; -
FreeCAD-контейнер работает.

Старый `scsi1` сначала отсоединили и убрали из boot order, затем
отдельным шагом удалили. Файл старого volume отсутствует, ссылок в
конфигурации VM нет, snapshots отсутствовали, `scsi0` и `scsi2` не
изменялись.

Свободное место NVMe увеличилось с `45,073,912 KiB` до `53,060,692 KiB`,
прирост `7,986,780 KiB` ≈ `7.62 GiB`. Это меньше номинальных 20 GiB
из-за sparse/QCOW2-размещения.

## 2.3. Ресурсы после запуска LibreChat

Исторический post-start отчёт: - доступная RAM --- около 1.4 GiB; - swap
отсутствует; - OOM не обнаружен; - перезапусков из-за OOM не было.

  Контейнер/сервис            Память
  --------------------- ------------
  LibreChat                \~482 MiB
  RAG API                  \~246 MiB
  MongoDB                  \~259 MiB
  Admin Panel               \~46 MiB
  Meilisearch               \~18 MiB
  PostgreSQL/pgvector       \~55 MiB
  FreeCAD                 \~1.05 GiB

Свободное место на момент отчёта: системный SSD около 9.6 GiB;
`<HOST_DATA_ROOT>` около 76 GiB. Это измерения 16 ноября 2026, не
live-проверка на момент передачи.

## 2.4. Docker-сеть

Создана отдельная Docker-сеть `cad_mcp`: - FreeCAD: статический IP
`<FREECAD_CONTAINER_IP>`; - LibreChat API: статический IP `<LIBRECHAT_CONTAINER_IP>`; - LAN
mapping MCP: `<LAN_HOST_IP>:39280:39280`.

Сеть создана для стабильной адресации MCP и устранения зависимости от
динамического IP контейнера.

## 2.5. Compose-файлы и контейнеры

LibreChat Compose: -
`<LIBRECHAT_CONFIG_ROOT>/docker-compose.yml` -
`<LIBRECHAT_CONFIG_ROOT>/docker-compose.override.yml` -
`<LIBRECHAT_CONFIG_ROOT>/librechat.yaml`

Compose project: `librechat`. Сервис API: `api`. MongoDB container name:
`chat-mongodb`. FreeCAD container name: `cad-freecad`.

Полный стек: 1. MongoDB; 2. Meilisearch; 3. PostgreSQL/pgvector; 4. RAG
API; 5. LibreChat API; 6. Admin Panel.

MongoDB, Meilisearch, PostgreSQL и RAG API не публиковались наружу в
приведённой конфигурации.

------------------------------------------------------------------------

# 3. Архитектура CAD Agent Team

## 3.1. Логическая схема

``` text
Пользователь
    |
    v
LibreChat UI
    |
    v
CAD Coordinator (EZ AI / Claude Sonnet 5.5)
    |
    +---- Subagents: CAD Analyst
    +---- Subagents: CAD Builder
    +---- Subagents: CAD Reviewer
    +---- MCP tools (FreeCAD)
                 |
                 v
          LibreChat MCP client
                 |
          TLS + Bearer token
                 |
                 v
       Docker network: cad_mcp
                 |
                 v
       FreeCAD MCP Bridge v0.1.30
                 |
                 v
          FreeCAD GUI session
                 |
                 v
         CAD document / geometry
```

Модель отвечает за рассуждение и планирование; Skills должны содержать
профессиональную методику; MCP даёт реальные инструменты и действия.
Наличие полноценных Skills пока не подтверждено.

## 3.2. Принципы оркестрации

**ПРИНЯТОЕ НАПРАВЛЕНИЕ:** Coordinator --- основной интерфейс
пользователя и диспетчер команды. Он не должен бездумно запускать
Analyst перед каждой операцией.

Пользователь отдельно указал, что повторный анализ неизменённой модели
каждый раз нелогичен. После обсуждения изменённой логики пользователь
ответил «хорошо» и запросил начальный промпт. Рабочий принцип: - Analyst
вызывается, когда нужно установить фактическое состояние, исследовать
незнакомую модель, проверить актуальность данных или диагностировать
расхождение; - если состояние достоверно известно и с тех пор не
менялось, Coordinator может использовать существующие данные и не обязан
повторять полный анализ; - после существенного изменения геометрии
Builder Reviewer должен проверить результат; - Coordinator может сам
выполнять небольшие и очевидные действия, а сложную работу делегировать.

Точный текст начального промпта из ранней части истории в доступном
контексте отсутствует. Не реконструировать его дословно.

Пользователь также указал: - не спрашивать перед каждым обычным
изменением модели/кода, если предыдущая версия сохраняется; - сохранять
предыдущие версии, чтобы обеспечить откат; - не ограничивать доступ
агентов без доказанной необходимости; - не затрагивать чужие документы и
не терять существующие версии.

Это пользовательские требования к рабочему процессу, а не разрешение
удалять исходники или обходить файловые ограничения.

## 3.3. Конфигурация Subagents

Сохранённая конфигурация Coordinator: - `subagents.enabled = true`; -
`allowSelf = false`; - `shareFiles = true`; - `agent_ids` содержит
Analyst, Builder, Reviewer.

Известные ID: - CAD Analyst: `<ANALYST_AGENT_ID>`; - CAD
Builder: `<BUILDER_AGENT_ID>`; - CAD Reviewer:
`<REVIEWER_AGENT_ID>`; - CAD Coordinator: ID в доступной истории
не приведён.

Создание четырёх агентов выполнено через обычный пользовательский
LibreChat API `POST /api/agents`, а не через Management API. Management
API `/api/agents/v1/agents` не был настроен и отвечал `401` без machine
OIDC. Обычный маршрут защищён JWT и permission checks
`AGENTS.USE + AGENTS.CREATE`.

## 3.4. MCP-инструменты и назначения

Фактический `tools/list` MCP Bridge возвращал: - `execute_python`; -
`execute_python_file`; - `get_output_page`.

LibreChat aliases: - `execute_python_mcp_freecad`; -
`execute_python_file_mcp_freecad`; - `get_output_page_mcp_freecad`.

История назначения: 1. Сначала всем четырём агентам назначались три
MCP-инструмента. 2. При внедрении CAD Agent Team v2 всем агентам
назначили `execute_python_mcp_freecad` и `get_output_page_mcp_freecad`.
3. `execute_python_file_mcp_freecad` был намеренно исключён из явного
toolset MVP. 4. `subagent` добавляется LibreChat динамически в runtime
для Coordinator; в MongoDB он не обязательно записан как обычный MCP
tool.

В одном успешном runtime Coordinator был виден набор из четырёх
инструментов: `subagent`, `execute_python_mcp_freecad`,
`execute_python_file_mcp_freecad`, `get_output_page_mcp_freecad`. Это
относится к конкретному успешному запуску и не отменяет более позднее
описание явного toolset v2 из двух MCP-инструментов. Текущий
runtime-набор каждого агента нужно проверять непосредственно перед
изменениями.

------------------------------------------------------------------------

# 4. Четыре агента

## 4.1. CAD Coordinator

**Назначение:** главный координатор, пользовательская точка входа,
постановка задач и сбор результатов.\
**Модель:** `anthropic/claude-sonnet-5.5` через endpoint `ez-ai`.\
**ID:** в доступной истории не найден.

Подтверждённая конфигурация: Subagents включены; `allowSelf=false`;
`shareFiles=true`; связи с Analyst, Builder, Reviewer сохранены;
MCP-инструменты доступны; `subagent` предоставляется LibreChat runtime.

Поведение по принятой архитектуре: - принимает задачу пользователя; -
решает, достаточно ли известного состояния или нужен свежий анализ; -
при необходимости вызывает Analyst; - поручает построение/изменение
Builder; - после изменения поручает независимую проверку Reviewer; -
собирает факты, ограничения и результаты; - формирует итоговый ответ.

Длина инструкции в одном отчёте Computer --- около 7.3 KB. Полный текст
инструкции недоступен.

Успешные проверки: Coordinator реально вызвал Analyst через `subagent`;
Analyst получил отдельную задачу; результат вернулся в родительский
контекст; Coordinator продолжил генерацию; в LibreChat появилась
дочерняя панель Analyst.

Проблемы: несколько запусков зависали до создания tool call; в зависших
сообщениях `unfinished: true`, пустой content, нет tool_calls; один тест
ждал более 74 секунд. Нестабильность EZ AI/Claude была вероятной, но не
доказанной на wire-level. Позднее пользователь получил быстрый ответ и
настоящий Subagent-запуск.

`anthropic/claude-haiku-5.5` предлагалась как более лёгкая модель
Coordinator, но замена не подтверждена; последняя известная назначенная
модель --- Sonnet 5.5.

## 4.2. CAD Analyst

**ID:** `<ANALYST_AGENT_ID>`\
**Модель:** `deepseek/deepseek-v4.1-flash` через `ez-ai`.

Назначение --- независимая read-only диагностика фактического состояния
FreeCAD-модели. По видимому скриншоту и описанию инструкции Analyst: -
читает дерево объектов; - анализирует типы объектов; - проверяет
`Placement`; - измеряет габариты и объёмы; - изучает параметры и
ограничения эскизов; - проверяет валидность Shape; - указывает источники
и единицы измерения; - отделяет факты от предположений; - подтверждает
ревизии и размеры; - ищет расхождения между ожидаемым и фактическим
состоянием; - выполняет точечные измерения по запросу.

Ограничения: не создаёт геометрию, не изменяет модель, не пересчитывает
и не сохраняет документ, не заменяет Builder. Предоставляет Reviewer
объективные измерительные данные.

Подтверждённые действия: прямой тест Analyst с четырьмя
последовательными вызовами `execute_python_mcp_freecad`; успешный
Subagent-вызов от Coordinator; ответ о роли Analyst на русском;
отдельная дочерняя панель.

Полная исходная инструкция недоступна. На скриншоте Analyst описывает
себя как независимого read-only инспектора, который не создаёт, не
изменяет, не пересчитывает и не сохраняет модель.

## 4.3. CAD Builder

**ID:** `<BUILDER_AGENT_ID>`\
**Модель:** `deepseek/deepseek-v4.1-flash` через `ez-ai`.

Назначение --- создание и изменение CAD-геометрии в FreeCAD. Builder
вносит правки в геометрию, создаёт объекты, изменяет параметры/форму,
сохраняет документ и должен применять `cad_revision.py`.

Подтверждённая работа: создал `Part::Box` `CalibrationCube`, 20×20×20
мм, Placement `(0,0,0)`, сохранил FCStd и экспортировал STL в `<TEMP_DIR>`.
Reviewer подтвердил геометрию и STL.

Проблемы: не смог создать проект/ревизии в
`<CAD_WORKSPACE>` из-за `PermissionError`; при проверке
переоткрытия закрыл исходный документ и открыл заново, из-за чего
потерялась история Undo; геометрия не изменилась; before/after
checkpoints не созданы. Полный промпт недоступен.

## 4.4. CAD Reviewer

**ID:** `<REVIEWER_AGENT_ID>`\
**Модель:** `deepseek/deepseek-v4.1-flash` через `ez-ai`.

Назначение --- независимая проверка корректности и качества результата.
Ограничения: read-only, не исправляет модель, не подменяет Builder,
проверяет фактические данные, а не только заявление Builder.

Подтверждённая работа: проверил тестовый куб, Shape validity, топологию,
STL, пересчитал SHA-256 и подтвердил совпадение с данными Builder;
зафиксировал, что геометрия/STL проходят, а ревизии не созданы. Полный
промпт недоступен.

------------------------------------------------------------------------

# 5. История тестирования команды

## 5.1. Первичная проверка Subagents

В тесте Coordinator должен был вызвать CAD Analyst и попросить описать
роль. Один ранний успешный запуск: настоящий инструмент `subagent`,
корректные аргументы, Analyst запущен, ответил «Задача получена, CAD
Analyst на связи», Coordinator получил результат. Длительность дочернего
выполнения --- около 2.5 секунды.

Conversation ID: `<UUID_REDACTED>`.

## 5.2. Зависшие Coordinator

Неуспешные запуски: - `<UUID_REDACTED>`; -
`<UUID_REDACTED>`; - ещё один ID упоминался, но в
доступном тексте приведён не полностью.

Подробности одного зависшего запуска: - Conversation ID:
`<UUID_REDACTED>`; - User message ID:
`<UUID_REDACTED>`; - Assistant message ID:
`<UUID_REDACTED>`; - модель
`anthropic/claude-sonnet-5.5`; - `unfinished: true`, content пустой,
`tool_calls` отсутствуют; - дочерний Analyst не создан; - транзакции
имели контекст `abort`; - для этого conversation указывалось четыре
незавершённых попытки.

Вывод: сбой происходил до фактического `subagent` tool call. Это не
доказывало, что Subagents сломан; вероятнее было ожидание/обрыв
генерации до завершения streaming-ответа.

## 5.3. Успешный Coordinator → Analyst

Последний подробно разобранный успешный запуск: - Conversation ID:
`<UUID_REDACTED>`; - User message ID:
`<UUID_REDACTED>`; - Coordinator response ID:
`<UUID_REDACTED>`; - user timestamp
`20:51:29.780 UTC` (примерно 01:51 17 ноября при UTC+5); - assistant
timestamp `20:51:36.826 UTC`; - общее время около 7 секунд; -
`unfinished: false`.

Подтверждено: - Coordinator вызвал `subagent`; -
`subagentAgentId = <ANALYST_AGENT_ID>`; - статус tool call ---
`completed`; - подготовка инструмента: `1479 ms`; - выполнение Analyst:
`2052 ms`; - полная длительность tool step: `3529 ms`; - результат
встроен в `subagent_content`, две части, текстовая часть около 833
символов; - Coordinator получил результат и продолжил генерацию; -
финальный ответ сохранён.

Отдельных записей в `subagentcontents`, `agentqueuedturns`, `toolcalls`
не обнаружили; связь child → parent была встроена в
`tool_call.subagentIdentity` и `subagent_content` родительского
сообщения.

Модели: Coordinator `ez-ai / anthropic/claude-sonnet-5.5`; Analyst
`ez-ai / deepseek/deepseek-v4.1-flash`.

## 5.4. Визуальное подтверждение

`image(20261116-210043).png` показывает центральную панель CAD
Coordinator, строку вызова CAD Analyst, открытую справа дочернюю панель
Analyst, исходную задачу и самостоятельный ответ. Это визуальное
подтверждение настоящего дочернего запуска и возврата результата.

`image(20261116-193525).png` показывает другой запуск Coordinator,
который ожидал примерно 41 секунду без текста ответа.

## 5.5. Прямой тест Analyst

Conversation ID: `<UUID_REDACTED>`. По отчёту
Computer Analyst выполнил четыре последовательных вызова
`execute_python_mcp_freecad`; все вызовы завершились.

## 5.6. XYZ Calibration Cube

Задание --- создать стандартный XYZ Calibration Cube 20×20×20 мм.

Последовательность: Coordinator получил задачу → вызвал Builder →
Builder создал геометрию через FreeCAD MCP → сохранил FCStd и
экспортировал STL → не смог использовать revision helper из-за прав →
Coordinator вызвал Reviewer → Reviewer независимо проверил модель и STL.

**Геометрия: PASS. STL: PASS. Постоянное версионирование: FAIL / не
завершено.**

### Геометрия

-   Документ: `XYZ_Calibration_Cube`;
-   объект: `CalibrationCube`;
-   тип: `Part::Box`;
-   размеры: 20×20×20 мм;
-   Placement: `(0,0,0)`;
-   объём: `7999.999999999998 мм³` (float-погрешность относительно
    8000);
-   Solid / Shell / Face / Edge / Vertex: `1 / 1 / 6 / 12 / 8`;
-   все шесть граней плоские, площадь 400 мм² каждая;
-   `isValid() = True`, `check()` ошибок не выявил;
-   лишних объектов, фасок и скруглений нет;
-   нижняя грань на `Z=0`.

### STL

-   binary STL;
-   12 фасет;
-   8 точек;
-   bounding box 20×20×20 мм;
-   `isSolid = True`;
-   non-manifold не обнаружен;
-   самопересечений нет;
-   нормали наружу;
-   объём 8000 мм³;
-   площадь 2400 мм².

### Файлы и хеши

-   `<TEMP_DIR>/xyz-calibration-cube-test/XYZ_Calibration_Cube.FCStd`
-   `<TEMP_DIR>/xyz-calibration-cube-test/XYZ_Calibration_Cube.stl`

SHA-256: - FCStd:
`02dbc6da5eacf0a8a35f6ee3ecbf8f9b5ba00dcdd92b9533ba359b16887fd1c7` -
STL: `ba6ec9ce5c36260975e6b26cddbbfdfc2f1c97b60cc4180eb13e9b8076e02ba0`

Reviewer пересчитал хеши и подтвердил совпадение. Эти пути относятся к
VM/контейнеру пользователя; в текущем ChatGPT runtime файлы недоступны.

### Побочный эффект Builder

При проверке переоткрытия Builder закрыл исходный документ и открыл его
заново из файла. Undo history потеряна; геометрия не изменилась.

### Блокер ревизий

-   `<CAD_WORKSPACE>` --- `root:root`, mode `0755`;
-   FreeCAD работает под UID `1000`;
-   GID не указан;
-   `mkdir` завершился `PermissionError`;
-   каталог `<CAD_WORKSPACE>/xyz-calibration-cube-test` не
    создан;
-   before/after snapshots, `revision_log.json`, `project_state.json`
    для этого куба не созданы;
-   файлы остались в `<TEMP_DIR>`.

Последний предложенный, но не выполненный шаг: создать только целевой
каталог, назначить владельцем UID/GID FreeCAD, не менять родительский
каталог рекурсивно, затем Builder должен сохранить существующий документ
и STL в постоянный проект и создать ревизии. Пользователь ещё не сообщил
результат выполнения.

------------------------------------------------------------------------

# 6. EZ AI: подключение, модели и API

## 6.1. Endpoint

Точное имя endpoint в LibreChat: `ez-ai`. Base URL:
`https://api.ez-ai.ru/v1`.

Ранее пользователь сначала назвал `api.yes-ai.ru`, затем уточнил EZ AI.
По диагностическому отчёту `api.yes-ai.ru` не разрешался через DNS, а
`api.ez-ai.ru` был фактическим сохранённым адресом. `/v1/models` без API
key возвращал `401`.

Endpoint настроен как OpenAI-compatible custom endpoint и
зарегистрирован через Admin Panel / MongoDB override, а не как endpoint
в `librechat.yaml`.

В раннем снимке metadata: - `models.fetch: true`; - `customParams`
отсутствовал; - `paramDefinitions` отсутствовал; - явные `modelSpecs` и
`interface` в MongoDB отсутствовали; - модель по умолчанию называлась
`test`.

`test` относится к раннему снимку metadata и не является текущей моделью
агентов.

## 6.2. Credentials

EZ AI API key хранится в конфигурации LibreChat/MongoDB зашифрованным.
Значения ключа, токенов и шифровальных секретов не включаются.

История: 1. Был обнаружен `ez-ai.apiKey` формата `v3:<iv>:<ciphertext>`.
2. Старый `.env` содержал `CREDS_KEY` из 32 hex-символов (16 байт) и
`CREDS_IV` из 16 hex-символов. 3. В отчёте указано, что LibreChat
v0.8.9-rc1 ожидал 64 hex-символа для AES-256-CTR v3. 4. Среди найденных
backup `.env` не было 64-символьного варианта. 5. Старый ciphertext в
ходе диагностики не расшифровывали и не меняли. 6. После согласования
был создан backup и выполнена ротация: `CREDS_KEY` заменён на 64
hex-символа, `CREDS_IV` на 32 hex-символа; пересоздан только LibreChat
API; API вернулся к HTTP 200. 7. Старый EZ AI ciphertext намеренно не
трогали. 8. Пользователь сообщил, что вручную отправил сообщение через
провайдера и получил ответ GPT. Следовательно, обычный чат через EZ AI
фактически работал после этого этапа. Почему ciphertext продолжал
работать, в доступной истории не установлено.

Backup:
`<LIBRECHAT_CONFIG_ROOT>/backups/pre-creds-rotation-20261116T142516Z/`.

Поздний аудит обнаружил `<CONTAINER_APP_ROOT>/data/.env.temp` с временными `CREDS_KEY`,
`CREDS_IV`, `JWT_SECRET`, `JWT_REFRESH_SECRET`. `/app/data` ---
постоянный Docker volume на HDD; файл переживал пересоздание API; его не
удаляли и не меняли. Причина появления и влияние на runtime не
установлены.

## 6.3. Назначенные модели

  --------------------------------------------------------------------------------
  Агент                   Точный model ID                  Статус
  ----------------------- -------------------------------- -----------------------
  CAD Coordinator         `anthropic/claude-sonnet-5.5`    подтверждён в
                                                           конфигурации и успешном
                                                           Subagent-запуске

  CAD Analyst             `deepseek/deepseek-v4.1-flash`   подтверждён в
                                                           конфигурации и реальных
                                                           MCP/Subagent-тестах

  CAD Builder             `deepseek/deepseek-v4.1-flash`   назначение указано в
                                                           отчёте; cube task
                                                           выполнен

  CAD Reviewer            `deepseek/deepseek-v4.1-flash`   назначение указано в
                                                           отчёте; cube проверен
  --------------------------------------------------------------------------------

Другие модели: - `anthropic/claude-haiku-5.5` --- кандидат для более
лёгкого Coordinator; замена не подтверждена; - Claude Opus 5.5 ---
обсуждался; точный ID и доступность через EZ AI не подтверждены; -
DeepSeek V4 Pro --- обсуждался; точный ID и доступность не
подтверждены; - DeepSeek V4 Flash --- встречался в раннем обсуждении;
текущий ID специалистов --- именно `deepseek/deepseek-v4.1-flash`.

Полный авторизованный GET `/v1/models` не подтверждён как успешно
завершённый. Пользовательская ручная генерация доказывает работу
обычного чата, но не заменяет полный каталог.

## 6.4. Протокол и возможности API

Подтверждено: - LibreChat настроен на OpenAI-compatible custom
endpoint; - успешный вызов `subagent` от Claude Sonnet 5.5 доказывает,
что tool calling хотя бы в одном запуске работал; - DeepSeek V4.1 Flash
выполнял реальные MCP-вызовы; - исследовалась точка LangChain OpenAI
integration `@langchain/openai/dist/chat_models/completions.cjs`,
`completionWithRetry()` → `chat.completions.create()`.

Не подтверждено: - полный raw HTTP request к EZ AI; - точный JSON
payload; - фактический wire-level `stream=true` для конкретных
запусков; - точный SSE-поток; - `finish_reason` неуспешных попыток; -
поддержка Responses API EZ AI; - совместимость каждой модели с Chat
Completions и Responses API; - reasoning-параметры EZ AI; - точный
формат `reasoning_effort` или объекта `reasoning`; - все ограничения
tool choice.

Попытка временной трассировки: trace-файл остался пустым; исходный
runtime-файл восстановлен из backup; SHA-256 восстановленного файла
совпал с backup (`05193a92…cb9d55b2b`); trace удалён. Позднее
выяснилось, что прежний вывод «запрос не дошёл до API» был недостаточно
обоснован: `POST /api/agents` и `Title generation timeout` не доказывали
доставку chat-запроса, а трассировка не перехватила нужный маршрут.

## 6.5. Reasoning / Thinking UI

В LibreChat `v0.8.9-rc1` frontend содержит Thinking UI control. В раннем
аудите `interface.parameters` явно не задавался; `customParams` и
`paramDefinitions` для `ez-ai` отсутствовали. Обсуждались
`reasoning_effort`, `reasoning_object`, `disabled`.

Форматы EZ AI не подтверждены. Реальный тест reasoning-параметра не был
успешно завершён. Не добавлять параметры наугад.

## 6.6. Стоимость и tokenConfig

В `librechat.yaml` включено:

``` yaml
interface:
  contextUsage: true
  contextCost: true
```

Runtime-загрузка подтвердила оба флага. В MongoDB EZ AI endpoint не имел
`tokenConfig`; prompt/completion usage-записи присутствовали,
cached-token поля в просмотренных данных не обнаружены. Тарифы EZ AI для
двух назначенных моделей не подтверждены. Нельзя подставлять тарифы
Anthropic/DeepSeek как будто это тарифы EZ AI. `contextCost: true` без
корректного `tokenConfig` не гарантирует достоверную стоимость.

------------------------------------------------------------------------

# 7. LibreChat: версия, Compose, регистрация и настройки

## 7.1. История версий

1.  Первоначально выбран LibreChat `v0.8.7`; `v0.8.8` тогда обозначался
    upstream как pre-release.
2.  Подготовлен официальный стек на HDD.
3.  Из-за отсутствия AVX использовался MongoDB override `mongo:4.4.18`.
4.  Пользователь разрешил сменить CPU-модель VM на `host`; AVX/AVX2
    подтверждены.
5.  Проект переключили на официальный tag `v0.8.8`; override MongoDB
    4.4.18 убрали, использовался `mongo:8.0.20`.
6.  Pull из официальных registry несколько раз давал timeout/reset;
    сторонние зеркала не использовались.
7.  Позднее проект обновлён на официальный tag `v0.8.9-rc1`.
8.  В отчёте указан commit `8d3da9bbb220…` (полный SHA отсутствует).
9.  Обновлён официальный образ Admin Panel; остальные сервисы не
    обновлялись.
10. Последняя известная версия API и frontend --- `v0.8.9-rc1`.

## 7.2. Backup перед v0.8.9-rc1

`<LIBRECHAT_CONFIG_ROOT>/backups/pre-v0.8.9-rc1-20261116T133121Z/`

По отчёту включал MongoDB archive, `.env`, `librechat.yaml`,
Compose-файлы. MongoDB backup прошёл `mongorestore --dryRun`.

## 7.3. Регистрация и Admin

Первичная проблема: - в `.env` были `ALLOW_REGISTRATION=true`,
`ALLOW_EMAIL_LOGIN=true`, `ALLOW_UNVERIFIED_EMAIL_LOGIN=true`; -
`/api<FREECAD_CONFIG_ROOT>` фактически возвращал `registrationEnabled=false`; - API
контейнер работал от UID 1000; - `<CONTAINER_APP_ROOT>/.env` был `root:root`, mode
`0600`; - процесс LibreChat не мог прочитать файл.

Исправление --- в `docker-compose.override.yml` для сервиса `api`
добавили:

``` yaml
environment:
  ALLOW_EMAIL_LOGIN: "true"
  ALLOW_REGISTRATION: "true"
  ALLOW_UNVERIFIED_EMAIL_LOGIN: "true"
```

После пересоздания API `/api<FREECAD_CONFIG_ROOT>` показал `registrationEnabled=true`;
первый пользователь зарегистрировался и получил `ADMIN` в single-tenant
режиме.

После регистрации в MongoDB был один пользователь с ролью ADMIN. Затем
регистрация закрыта: - `ALLOW_REGISTRATION=false`; -
`ALLOW_EMAIL_LOGIN=true`; - `ALLOW_UNVERIFIED_EMAIL_LOGIN=true`.

Пересоздан только API; `/api<FREECAD_CONFIG_ROOT>` подтвердил
`registrationEnabled=false`.

Backup:
`<LIBRECHAT_CONFIG_ROOT>/backups/pre-registration-disable-20261116T130030Z-docker-compose.override.yml`.

## 7.4. Агентский API

-   обычный пользовательский маршрут: `POST /api/agents`;
-   защищён JWT и правами `AGENTS.USE + AGENTS.CREATE`;
-   Management API `/api/agents/v1/agents` не включён; без авторизации
    возвращал `401`;
-   `/api/openapi.json` возвращал `404`;
-   агенты созданы через обычный пользовательский API;
-   прямое редактирование MongoDB вместо Agent Builder/API не
    применялось.

Для первоначального автоматического создания агентов использовалась
пользовательская авторизованная сессия/credentials. Значения секретов не
сохраняются.

## 7.5. Usage UI и стоимость

Включены `interface.contextUsage: true` и `interface.contextCost: true`.
Backup:
`<LIBRECHAT_CONFIG_ROOT>/backups/context-ui-20261116T201054Z/`.
Изменялся только `librechat.yaml`, пересоздавался только API.
MCP-конфигурация после изменения сохранилась; API и frontend отвечали
HTTP 200.

`tokenConfig` не добавлялся из-за отсутствия подтверждённых тарифов EZ
AI.

## 7.6. Сессия после обновления страницы

Пользователь сообщал, что после обновления страницы приходилось заново
авторизовываться. Позднее сообщил: «проблему с перезагрузкой он уже
исправил». Детали исправления и точный diff отсутствуют. Считать
проблему решённой по сообщению пользователя, но не придумывать детали.

------------------------------------------------------------------------

# 8. FreeCAD и MCP Bridge

## 8.1. FreeCAD

-   контейнер: `cad-freecad`;
-   Docker IP: `<FREECAD_CONTAINER_IP>`;
-   web/HTTPS endpoint: `https://<LAN_HOST_IP>:3001/`;
-   точная версия FreeCAD неизвестна;
-   профиль GUI: `<FREECAD_CONFIG_ROOT>/.config/FreeCAD/v1-1/user.cfg`.

`v1-1` в пути профиля --- имя каталога конфигурации, не доказательство
версии FreeCAD.

## 8.2. MCP Bridge

-   проект: `https://github.com/CREATeNG/freecad-mcp-bridge`;
-   версия: `v0.1.30`;
-   listener: `<FREECAD_CONTAINER_IP>:39280`;
-   публикация: `<LAN_HOST_IP>:39280`;
-   сервер в LibreChat: `freecad`;
-   соединение TLS + Bearer token.

На `image(20261116-163301).png` видны исходные/default настройки: -
address `127.0.0.1`; - port `39280`; - поля Certificate (PEM) и Private
key (PEM) пусты; - кнопки Generate self-signed certificate, Generate new
token, Set token; - Permission mode `Ask (default)`; - Bridge
включается/выключается через `MCP Off` / `MCP On` в status bar; - для
адресов вне loopback требуется TLS certificate; - каждый listener
требует Bearer token.

Это изображение относится к раннему состоянию до окончательной
настройки.

## 8.3. Диагностика GUI и headless профиля

1.  Headless-процесс изменил отдельное временное состояние, но не
    GUI-профиль.
2.  В текущем GUI `user.cfg` MCP-параметры отсутствовали.
3.  Сертификат и ключ были проверены и соответствовали друг другу.
4.  SAN сертификата включает `<LAN_HOST_IP>` и `<FREECAD_CONTAINER_IP>`.
5.  LibreChat API доверяет сертификату через `NODE_EXTRA_CA_CERTS`.
6.  TokenHash присутствует в FreeCAD profile и соответствует
    сохранённому токену LibreChat; секрет не раскрывается.
7.  Первая попытка изменить `user.cfg` при работающем GUI была
    перезаписана defaults при завершении процесса.
8.  Правильная последовательность: backup, остановить GUI, изменить
    профиль, запустить FreeCAD, проверить ParamGet и отсутствие
    перезаписи.
9.  После этой процедуры параметры сохранились.

Активный профиль: `<FREECAD_CONFIG_ROOT>/.config/FreeCAD/v1-1/user.cfg`. Точные пути
сертификата, private key и защищённого файла токена не приведены.

## 8.4. Permission mode

По исходникам Bridge v0.1.30 и отчётам: - `PermissionMode=0` --- Ask; -
`PermissionMode=1` --- Unrestricted.

Сначала проверка показывала `0`, потому что профиль был прочитан до
ручного изменения пользователя. Поздняя проверка активного GUI-профиля
показала `PermissionMode=1`; read-only probe выполнился без Allow.
Последний известный режим --- **Unrestricted**, выбран пользователем
вручную.

## 8.5. Запуск Bridge и автозапуск

Встроенный автозапуск Bridge при старте FreeCAD в установленной версии
не нашли. Bridge запускается через MCP On/Off в status bar. Пользователь
вручную включил Bridge; первое предупреждение/окно Accept and Start не
появлялось, после повторного нажатия MCP Bridge включился. Startup macro
предлагался, но не внедрён.

Unrestricted устраняет повторное подтверждение отдельных Python-вызовов,
но не означает автоматический старт самого Bridge.

## 8.6. TLS, token и handshake

Подтверждено: - TLS certificate/key созданы штатными средствами
Bridge/API; - SAN включает LAN и Docker IP; - сертификат и ключ
совпадают; - API доверяет сертификату; - Bearer token создан; - FreeCAD
хранит hash токена, не plaintext token; - токен хранится в защищённом
root-only месте и передан API через env-файл.

Успешный handshake из LibreChat: - `initialize` --- HTTP 200; -
`notifications/initialized` --- HTTP 202; - `tools/list` --- HTTP 200; -
Bridge `0.1.30`.

## 8.7. Инструменты

Сервер возвращает: 1. `execute_python` --- выполнение Python в контексте
FreeCAD; 2. `execute_python_file` --- выполнение Python-файла; 3.
`get_output_page` --- получение страниц/вывода.

LibreChat aliases: - `execute_python_mcp_freecad`; -
`execute_python_file_mcp_freecad`; - `get_output_page_mcp_freecad`.

Фактический tool assignment v2 --- два инструмента на агента:
`execute_python_mcp_freecad` и `get_output_page_mcp_freecad`.
`execute_python_file_mcp_freecad` не назначался в MVP, хотя сам
инструмент есть в `tools/list`.

------------------------------------------------------------------------

# 9. CAD Workspace, Docker mounts и права

## 9.1. Основной каталог

Целевой рабочий каталог: `<CAD_WORKSPACE>`. В отчётах
`/projects` описан как постоянный HDD mount. Точная строка mount/fstab
для `/projects` не приведена.

## 9.2. Обнаруженная проблема прав

Последний отчёт Builder/Reviewer: - `<CAD_WORKSPACE>` ---
владелец `root:root`; - mode `0755`; - FreeCAD работает под UID
`1000`; - GID процесса не указан; - FreeCAD может читать каталог, но не
создавать в нём новый подкаталог; - `mkdir` завершился
`PermissionError`.

Не подтверждены: GID FreeCAD; host UID/GID mapping; user namespace
remapping; точный mount source/target FreeCAD container; filesystem
type; ACL дерева; default ACL; SELinux/AppArmor; владельцы всех
существующих проектов.

## 9.3. Целевая политика общего Workspace

В запросе архивного извлечения пользователь сформулировал целевую
архитектуру: - один общий CAD Workspace; - все четыре агента имеют
доступ ко всей структуре; - не назначать отдельные разрешения каждому
проекту; - не менять существующих владельцев; - постоянные права чтения,
записи и обхода; - наследование для будущих вложенных каталогов и
файлов; - не использовать `chmod 777`; - не выполнять рекурсивный
`chown`.

Это **целевая политика**, а не доказательство применённых ACL. В
доступной истории нет подтверждения backup ACL, команд
`getfacl`/`setfacl`, рекурсивного ACL на всё дерево, default ACL или
проверок наследования.

## 9.4. Последний безопасный план для куба

1.  Определить реальный UID/GID FreeCAD.
2.  Создать только
    `<CAD_WORKSPACE>/xyz-calibration-cube-test`.
3.  Назначить владельцем только этот каталог UID/GID FreeCAD либо
    применить согласованную ACL-политику.
4.  Не менять родительский каталог рекурсивно.
5.  Не использовать `chmod 777`.
6.  Скопировать уже готовые FCStd/STL из `<TEMP_DIR>`.
7.  Прочитать фактический API revision helper.
8.  Создать журнал и project state.
9.  Reviewer проверяет постоянные файлы.

Пользователь ещё не сообщил результат выполнения этого задания Computer.

------------------------------------------------------------------------

# 10. cad_revision.py и система ревизий

## 10.1. Путь

`<CAD_AGENT_HOME>/bin/cad_revision.py`

По отчётам helper установлен; offline-тест прошёл; scratch-тесты
создавали FCStd before/after; проверялись ZIP-целостность и SHA-256;
обновлялся `project_state.json`; в одном тесте `doc.FileName` не
изменился.

## 10.2. Неизвестные детали

Исходника helper в текущем чате нет. Неизвестны точные
функции/сигнатуры, параметры CLI, способ создания проекта, поведение
`saveCopy()`/`saveAs()`, схема `revision_log.json`, схема
`project_state.json`, правила именования, восстановление, поведение при
ошибке записи и поддержка произвольной вложенности. Новый чат должен
прочитать фактический исходник на VM, а не придумывать API.

## 10.3. Подтверждённые тесты

### `team-v2-scratch`

Каталог: `<CAD_WORKSPACE>/team-v2-scratch/`

Ревизии: - `revisions/20261116T185725.062815Z-135fe7e2-before.FCStd` -
`revisions/20261116T185725.276756Z-313af7ae-after.FCStd`

Проверено по отчёту: ZIP-целостность обоих FCStd; SHA-256 совпадает с
журналом; `doc.FileName` рабочего документа не изменился;
`project_state.json` обновлён; scratch-документ закрыт.

### `team-v2-final-acceptance`

Каталог: `<CAD_WORKSPACE>/team-v2-final-acceptance/`

Содержимое по отчёту: 4 FCStd-ревизии, `revision_log.json`,
`project_state.json`, `acceptance_report.json`.

Тест: исходная модель `10×20×30`, объём 6000; изменённая `12×20×35`,
объём 8400; Shape valid; 4 ревизии; before-snapshot открыт для проверки
и содержал `10×20×30`, затем закрыт; текущая модель осталась изменённой.
Пользовательские CAD-файлы не затронуты.

Эти проверки выполнены прямым MCP fallback, а не полностью агентским
циклом. Они доказывают работу helper в scratch-сценариях, но не снимают
текущую проблему записи в Workspace для FreeCAD.

### XYZ Calibration Cube

Для cube test helper не смог создать каталог из-за прав; before/after
ревизии не созданы; FCStd/STL остались в `<TEMP_DIR>`; последний отчёт
указывал, что документ открыт в FreeCAD и связан с файлом из `<TEMP_DIR>`. Не
закрывать/удалять временные файлы до проверки постоянной копии.

------------------------------------------------------------------------

# 11. LibreChat Skills

В доступной истории этого чата нет подтверждённого исследования или
внедрения LibreChat Skills. Не найдены созданные `SKILL.md`, папки
Skills, reference-файлы, скрипты внутри Skills, назначения Skills
агентам, настройки Selected Skills / All или runtime-проверки.

Следующие Skills перечислены пользователем как
проектируемые/интересующие, а не как уже созданные: - CAD Project &
Revision Management; - FreeCAD Document Lifecycle; - CAD Task
Orchestration; - FreeCAD Inspection & Geometry Analysis; - FreeCAD
Parametric Modeling; - Independent CAD Verification.

Будущий этап: проверить реальную поддержку Skills в LibreChat
`v0.8.9-rc1`, формат `SKILL.md`, дополнительные reference files/scripts,
Selected Skills vs All и назначение конкретным агентам. Результат такого
исследования в доступной истории отсутствует.

------------------------------------------------------------------------

# 12. Дополнительные MCP и инструменты

В доступной истории нет законченного сравнительного исследования: -
Filesystem MCP; - FreeCAD Robust MCP Server; - FreeCAD Hybrid MCP; -
AgentCAD.

Они перечислены пользователем как темы, которые нужно восстановить, если
обсуждались ранее. Конкретные выводы о возможностях, версиях,
совместимости и выборе в доступной истории отсутствуют.

**Принцип пользователя:** существующий рабочий MCP Bridge не следует
заменять без отдельного исследования и проверки. Подтверждён только
FreeCAD MCP Bridge `v0.1.30`; новые MCP-серверы не считаются
установленными.

------------------------------------------------------------------------

# 13. LibreChat Admin, настройки endpoint и артефакты

## 13.1. Основные конфиги

  -----------------------------------------------------------------------------------------------------------------------
  Файл/путь                                                        Назначение              Статус
  ---------------------------------------------------------------- ----------------------- ------------------------------
  `<LIBRECHAT_CONFIG_ROOT>/docker-compose.yml`            основной Compose        существует по отчёту
                                                                   LibreChat               

  `<LIBRECHAT_CONFIG_ROOT>/docker-compose.override.yml`   локальные overrides     существует по отчёту

  `<LIBRECHAT_CONFIG_ROOT>/librechat.yaml`                основной YAML LibreChat существует;
                                                                                           `contextUsage`/`contextCost`
                                                                                           включены

  `<CONTAINER_APP_ROOT>/.env`                                                      секреты/переменные      существовал; root-only mode
                                                                   LibreChat внутри        0600 в одном аудите
                                                                   контейнера              

  `<CONTAINER_APP_ROOT>/data/.env.temp`                                            временные credentials   найден; постоянный volume; не
                                                                                           менялся

  `<FREECAD_CONFIG_ROOT>/.config/FreeCAD/v1-1/user.cfg`                          активный GUI профиль    существовал; MCP-группа
                                                                   FreeCAD                 исправлялась

  `<CAD_AGENT_HOME>/bin/cad_revision.py`                       revision helper         установлен; исходник
                                                                                           недоступен в текущем чате
  -----------------------------------------------------------------------------------------------------------------------

Точный host path bind mount для `<CONTAINER_APP_ROOT>/.env`, сертификатов и токена не
зафиксирован.

## 13.2. Резервные копии LibreChat

1.  `<LIBRECHAT_CONFIG_ROOT>/backups/pre-v0.8.9-rc1-20261116T133121Z/`
    --- MongoDB archive, `.env`, `librechat.yaml`, Compose;
    `mongorestore --dryRun` прошёл.
2.  `<LIBRECHAT_CONFIG_ROOT>/backups/pre-registration-disable-20261116T130030Z-docker-compose.override.yml`.
3.  `<LIBRECHAT_CONFIG_ROOT>/backups/pre-creds-rotation-20261116T142516Z/`.
4.  `<LIBRECHAT_CONFIG_ROOT>/backups/cad-agent-team-v2-pre-20261116T184823Z/agents-expanded.json`
    --- backup четырёх агентов, checksum проверен.
5.  `<LIBRECHAT_CONFIG_ROOT>/backups/context-ui-20261116T201054Z/`.

## 13.3. Backup FreeCAD profile

Сообщалось, что backup `user.cfg` создан до изменения MCP-группы, но
точный путь и имя backup в доступном чате не приведены.

## 13.4. Секреты

Не включены: EZ AI API key, `CREDS_KEY`, `CREDS_IV`, `JWT_SECRET`,
`JWT_REFRESH_SECRET`, MCP Bearer token, TLS private key, browser
cookies/session credentials. Указаны только имена переменных и пути,
если известны.

------------------------------------------------------------------------

# 14. Реестр проблем

  -----------------------------------------------------------------------------------------
  ID                Проблема             Диагностика и действия           Последний статус
  ----------------- -------------------- -------------------------------- -----------------
  P-01              Первичная            API не мог читать root-only      решено;
                    регистрация          `.env`; переменные внесены в     регистрация затем
                    LibreChat не         environment API                  закрыта
                    отображалась                                          

  P-02              MongoDB 8 не         VM переведена на `cpu: host`;    решено
                    поддерживался        AVX/AVX2 подтверждены            
                    виртуальным CPU                                       

  P-03              Pull Docker images   повторные pull из официальных    образы получены
                    timeout/reset        registry                         

  P-04              Несовместимость      backup, ротация ключа/IV,        API работает;
                    длины CREDS_KEY с v3 пересоздан API                   ciphertext не
                    decrypt                                               анализировался до
                                                                          конца;
                                                                          пользователь
                                                                          подтвердил
                                                                          рабочий чат

  P-05              LibreChat session    Computer исправил; точный diff   пользователь
                    терялась после       отсутствует                      сообщил, что
                    refresh                                               исправлено

  P-06              EZ AI/Coordinator    пустые unfinished assistant      нестабильность
                    генерации зависали   messages, no tool_calls, abort;  наблюдалась,
                                         затем успешные Subagent-запуски  wire-level
                                                                          причина не
                                                                          локализована

  P-07              Trace Chat           временный trace не перехватил    raw outbound
                    Completions пустой   нужный путь; файл восстановлен,  payload
                                         checksum совпал, trace удалён    неизвестен

  P-08              Thinking/reasoning   customParams/paramDefinitions    не решено/не
                    control не работал   отсутствуют; EZ AI reasoning     исследовано
                    ожидаемым образом    format не подтверждён            

  P-09              Стоимость моделей не contextUsage/contextCost         частично
                    отображается         включены; tokenConfig            
                    достоверно           отсутствует, тарифы неизвестны   

  P-10              Bridge не запускался встроенный autostart не найден;  startup macro не
                    автоматически        пользователь включает MCP On/Off внедрён

  P-11              Ask требовал Allow   пользователь вручную переключил  решено для
                    для вызовов          Unrestricted; PermissionMode=1   подтверждений
                                         подтверждён                      отдельных вызовов

  P-12              GUI profile          активный user.cfg проверен;      решено
                    отличался от         правка при работающем GUI была   
                    headless state       перезаписана; исправлено при     
                                         остановленном GUI                

  P-13              Revision helper не   `<CAD_WORKSPACE>`   блокирует
                    может писать в CAD   root:root 0755; FreeCAD UID 1000 постоянное
                    Workspace                                             сохранение cube
                                                                          project

  P-14              XYZ cube revisions   файлы в `<TEMP_DIR>`; mkdir в          не решено
                    не созданы           Workspace PermissionError        

  P-15              Builder закрыл и     Undo history потеряна, геометрия процессуальное
                    переоткрыл документ  не изменилась                    замечание

  P-16              Skills setup не      в доступной истории нет          будущая работа
                    подтверждён          созданных Skills                 
  -----------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 15. Хронология

Даты основаны на именах backup и timestamps из отчётов. Не все ранние
сообщения доступны.

## 15.1. Инфраструктура

Подготовлена dedicated VM; CAD/Docker data перенесены на HDD; `<HOST_DATA_ROOT>`
смонтирован по UUID `<UUID_REDACTED>`; Docker Root
Dir и containerd root переведены на HDD; старый NVMe disk `scsi1` удалён
после проверки; после reboot FreeCAD, Docker и containerd поднялись
штатно.

## 15.2. LibreChat v0.8.7 → v0.8.8

Подготовлен официальный v0.8.7. Из-за отсутствия AVX использовался
MongoDB 4.4.18 override. Пользователь разрешил CPU host; AVX/AVX2
подтверждены. Проект переключён на официальный v0.8.8 и MongoDB 8.0.20.
Pull из официальных registry давал timeout/reset; повторные загрузки
завершились. Полный Compose запущен; FreeCAD продолжил работать.

## 15.3. Регистрация

`.env` содержал `ALLOW_REGISTRATION=true`, но API возвращал false из-за
UID 1000 и прав `root:root 0600` на `<CONTAINER_APP_ROOT>/.env`. Environment override
включил регистрацию. Пользователь зарегистрировался, получил ADMIN;
затем регистрация закрыта.

## 15.4. EZ AI

Создан custom endpoint `ez-ai`; Base URL подтверждён как
`https://api.ez-ai.ru/v1`; пользователь увидел список моделей. Были
попытки изучить reasoning, customParams и capabilities. Полный
авторизованный GET `/v1/models` не подтверждён. Пользователь вручную
отправил запрос и получил ответ через провайдера.

## 15.5. LibreChat v0.8.9-rc1

Создан backup `pre-v0.8.9-rc1-20261116T133121Z`; выполнен переход на
официальный tag v0.8.9-rc1; обновлён Admin Panel image; API и frontend
работают на v0.8.9-rc1. Включены `contextUsage` и `contextCost`.

## 15.6. Credentials

Обнаружена проблема длины старого CREDS_KEY; создан backup
`pre-creds-rotation-20261116T142516Z`; CREDS_KEY/CREDS_IV ротированы;
пересоздан только API; старый EZ AI ciphertext не трогали; пользователь
подтвердил рабочий обычный чат.

## 15.7. Создание CAD Agent Team

Созданы четыре агента через `POST /api/agents`; настроены Subagents
связи; сначала всем назначались три MCP tools; затем внедрён CAD Agent
Team v2: существующие агенты обновлены, backup `agents-expanded.json`,
явный toolset MVP --- два MCP tools, `execute_python_file` исключён из
явного назначения.

## 15.8. MCP Bridge

Bridge v0.1.30 установлен; создана сеть `cad_mcp`; закреплены IP
FreeCAD/API; настроены TLS, SAN и Bearer token; исправлен активный GUI
`user.cfg`; Bridge включён вручную; пользователь выбрал Unrestricted;
handshake и tools/list подтверждены.

## 15.9. Scratch и revision tests

Helper `<CAD_AGENT_HOME>/bin/cad_revision.py` установлен;
`team-v2-scratch` прошёл before/after ZIP и SHA checks;
`team-v2-final-acceptance` содержит 4 ревизии и acceptance report. Эти
тесты выполнялись прямым MCP fallback, а не всеми агентами.

## 15.10. Subagents

Были зависшие Coordinator попытки без tool_calls. Позднее состоялся
успешный Coordinator → Analyst запуск в
`<UUID_REDACTED>`; скриншот показал дочернюю панель
Analyst; MongoDB анализ подтвердил настоящий subagent tool call, child
execution и возврат результата.

## 15.11. XYZ Calibration Cube

Coordinator поручил Builder создать куб 20×20×20 мм; Builder создал
геометрию и STL; Reviewer независимо проверил; revision step
заблокирован правами. Последние пути ---
`<TEMP_DIR>/xyz-calibration-cube-test/`. Проект в
`<CAD_WORKSPACE>/xyz-calibration-cube-test` не создан.
Последнее предложенное действие --- исправить права только целевой папки
и завершить сохранение/ревизии; результат пока не сообщён.

------------------------------------------------------------------------

# 16. Принятые решения и отклонённые варианты

## 16.1. Принято

1.  Использовать LibreChat как интерфейс и оркестратор.
2.  Использовать EZ AI custom endpoint.
3.  Сохранить четыре роли: Coordinator, Analyst, Builder, Reviewer.
4.  Использовать настоящие Subagents, а не имитацию делегации текстом.
5.  Coordinator --- основная точка входа пользователя.
6.  Analyst --- read-only.
7.  Builder --- изменение геометрии.
8.  Reviewer --- независимая проверка.
9.  Не вызывать Analyst автоматически перед каждой задачей, если
    состояние модели достоверно известно и не менялось.
10. Сохранять предыдущие версии; не спрашивать пользователя перед каждым
    обычным изменением внутри выделенного проекта, если механизм ревизий
    работает.
11. Использовать существующий FreeCAD MCP Bridge v0.1.30; не заменять
    без отдельного исследования.
12. Пользователь вручную выбрал Unrestricted.
13. Сохранять существующих владельцев Workspace при проектировании ACL.
14. Не использовать chmod 777 и не делать бездумный рекурсивный chown.
15. Не менять пользовательские CAD-документы во время scratch tests.
16. Не выполнять платные генерации при инвентаризации EZ AI без
    отдельного разрешения.

## 16.2. Отклонено или не применялось

-   Сторонние Docker registry mirrors --- не использовались.
-   Прямое редактирование MongoDB вместо штатного Agent API/Builder ---
    не применялось.
-   Замена FreeCAD MCP Bridge --- не выполнялась.
-   `chmod 777` --- не применялся.
-   Рекурсивный `chown` всего Workspace --- не применялся.
-   Переход Coordinator на Haiku --- только предложение.
-   `tokenConfig` с неподтверждёнными тарифами --- не добавлялся.
-   Reasoning-параметры EZ AI наугад --- не добавлялись.
-   Startup macro для автоматического запуска Bridge --- не внедрён.

------------------------------------------------------------------------

# 17. Незавершённая работа

## 17.1. Блокирующая

1.  Исправить права на целевую папку проекта XYZ Calibration Cube.
2.  Перенести FCStd/STL из `<TEMP_DIR>` в постоянный Workspace.
3.  Завершить ревизии и project metadata.
4.  Подтвердить, что Builder может создавать новые проекты и ревизии без
    ручного обхода.

## 17.2. Проверки агентов

После завершения прав: 1. Builder меняет существующую модель в отдельном
тестовом проекте. 2. Система создаёт новую ревизию. 3. Reviewer
независимо проверяет изменение. 4. Coordinator собирает отчёт. 5. Затем
выполнить полный цикл Coordinator → Analyst (только если нужен свежий
анализ) → Builder → Reviewer.

## 17.3. Workspace ACL

Нужно определить UID/GID FreeCAD; проверить host/container mapping;
проверить filesystem и mount; сделать backup текущих ACL; выбрать
ACL-политику, сохраняющую владельцев; включить чтение/запись/execute для
существующей структуры; настроить наследование default ACL; проверить
новые файлы/каталоги от имени FreeCAD; проверить доступ всех агентов
через общий процесс/контейнер.

Глобальные ACL не подтверждены как выполненные.

## 17.4. EZ AI

-   получить полный авторизованный GET `/v1/models`;
-   подтвердить точные model IDs;
-   выяснить доступность Claude Opus 5.5 и DeepSeek V4 Pro;
-   выяснить Chat Completions vs Responses API;
-   проверить streaming/tool calling нужных моделей;
-   установить reasoning parameter format;
-   получить реальные тарифы EZ AI;
-   только после этого настраивать `tokenConfig`;
-   не проводить платные генерации без согласования.

## 17.5. Skills

Изучить поддержку Skills в LibreChat v0.8.9-rc1; Selected Skills vs All;
структуру `SKILL.md`, reference files и scripts; назначения агентам;
создать шесть перечисленных специализированных Skills; подтвердить
загрузку runtime.

## 17.6. Автозапуск Bridge

Решить, нужен ли startup macro; проверить безопасность и поведение после
перезапуска FreeCAD; не путать автозапуск Bridge с Unrestricted
permission mode.

------------------------------------------------------------------------

# 18. Рекомендуемая последовательность продолжения

1.  Не трогать работающие сервисы; не перезапускать FreeCAD/API без
    причины.
2.  Проверить UID/GID FreeCAD и mount mapping. UID 1000 подтверждён; GID
    неизвестен.
3.  Закрыть точечный permission blocker: создать отдельную папку и дать
    доступ только ей; не менять весь Workspace наугад.
4.  Сохранить существующий куб. Не перестраивать геометрию. Скопировать
    файлы из `<TEMP_DIR>`, проверить hash, затем создать корректную baseline
    revision. Не выдавать новый snapshot за историческую ревизию до
    создания куба.
5.  Прочитать исходник `cad_revision.py`, установить фактический API
    helper.
6.  Проверить ревизии Reviewer: FCStd, STL, hash, ZIP, project_state и
    revision log.
7.  Провести Builder → Reviewer test на изменении существующей модели.
8.  Проверить полный цикл Coordinator; не менять модели до получения
    новых доказательств.
9.  Отдельным этапом исследовать ACL всего Workspace с backup.
10. Отдельным этапом исследовать Skills.
11. Отдельным этапом завершить EZ AI inventory/protocol/pricing.

------------------------------------------------------------------------

# 19. Перечень доступных материалов

## 19.1. Три доступных вложения

  ------------------------------------------------------------------------------
  Файл                           Содержание              Назначение
  ------------------------------ ----------------------- -----------------------
  `image(20261116-163301).png`   первоначальное окно     исходный GUI state:
                                 FreeCAD MCP Bridge      loopback, пустые TLS
                                 Preferences             fields, Ask default,
                                                         token controls

  `image(20261116-193525).png`   зависший Coordinator,   визуальное
                                 spinner около 41 s      свидетельство зависания

  `image(20261116-210043).png`   успешная панель         визуальное
                                 Coordinator + Analyst   свидетельство реального
                                                         Subagent child panel
  ------------------------------------------------------------------------------

## 19.2. Упомянутые серверные файлы, оригиналы которых здесь недоступны

-   `<LIBRECHAT_CONFIG_ROOT>/docker-compose.yml`
-   `<LIBRECHAT_CONFIG_ROOT>/docker-compose.override.yml`
-   `<LIBRECHAT_CONFIG_ROOT>/librechat.yaml`
-   `.env` LibreChat (контейнерный путь `<CONTAINER_APP_ROOT>/.env`; секреты не
    экспортировать)
-   `<CONTAINER_APP_ROOT>/data/.env.temp` (секреты не экспортировать)
-   `<FREECAD_CONFIG_ROOT>/.config/FreeCAD/v1-1/user.cfg`
-   backup `user.cfg` (имя/путь неизвестны)
-   сертификат MCP (путь неизвестен)
-   TLS private key (не экспортировать)
-   защищённый Bearer token file (путь неизвестен; не экспортировать)
-   `<CAD_AGENT_HOME>/bin/cad_revision.py`
-   `<LIBRECHAT_CONFIG_ROOT>/backups/pre-v0.8.9-rc1-20261116T133121Z/`
-   `<LIBRECHAT_CONFIG_ROOT>/backups/pre-registration-disable-20261116T130030Z-docker-compose.override.yml`
-   `<LIBRECHAT_CONFIG_ROOT>/backups/pre-creds-rotation-20261116T142516Z/`
-   `<LIBRECHAT_CONFIG_ROOT>/backups/cad-agent-team-v2-pre-20261116T184823Z/agents-expanded.json`
-   `<LIBRECHAT_CONFIG_ROOT>/backups/context-ui-20261116T201054Z/`
-   `<CAD_WORKSPACE>/team-v2-scratch/`
-   `<CAD_WORKSPACE>/team-v2-final-acceptance/`
-   `<TEMP_DIR>/xyz-calibration-cube-test/XYZ_Calibration_Cube.FCStd`
-   `<TEMP_DIR>/xyz-calibration-cube-test/XYZ_Calibration_Cube.stl`

Это пути из отчётов, а не утверждение, что файлы доступны из текущего
ChatGPT runtime.

## 19.3. Что включено в передаваемый ZIP

-   этот Markdown handoff;
-   три исходных скриншота;
-   manifest с перечнем вложений и SHA-256.

**Не включены:** серверные конфиги, MongoDB backup, ключи, токены,
cookies, private keys, FCStd/STL, потому что их оригиналы не были
доступны в текущем чате.

------------------------------------------------------------------------

# 20. Что новому чату необходимо знать в первую очередь

1.  Проект уже не на стадии первичной связки LibreChat и FreeCAD.
    Основная инфраструктура поднята.
2.  LibreChat API/frontend последней известной версии `v0.8.9-rc1`.
3.  dedicated VM работает с `cpu: host`; AVX/AVX2 доступны; MongoDB `8.0.20`.
4.  LibreChat API: `<LAN_HOST_IP>:3080`; Admin Panel: `<LAN_HOST_IP>:3000`.
5.  FreeCAD container: `cad-freecad`, IP `<FREECAD_CONTAINER_IP>`; HTTPS
    `<LAN_HOST_IP>:3001`.
6.  Docker network `cad_mcp`; LibreChat API `<LIBRECHAT_CONTAINER_IP>`.
7.  FreeCAD MCP Bridge `v0.1.30`, listener `<FREECAD_CONTAINER_IP>:39280`, LAN
    publish `<LAN_HOST_IP>:39280`.
8.  TLS и Bearer auth работают; handshake `initialize=200`, initialized
    `202`, tools/list `200`.
9.  MCP tools: `execute_python`, `execute_python_file`,
    `get_output_page`; explicit agent assignment v2 ---
    `execute_python_mcp_freecad` и `get_output_page_mcp_freecad`.
10. Пользователь вручную включил Unrestricted; active GUI `user.cfg`
    показывал `PermissionMode=1`.
11. Bridge сам не стартует при запуске FreeCAD; пользователь включает
    его кнопкой MCP On/Off. Startup macro не реализован.
12. Созданы четыре агента. Analyst ID `<ANALYST_AGENT_ID>`;
    Builder ID `<BUILDER_AGENT_ID>`; Reviewer ID
    `<REVIEWER_AGENT_ID>`; Coordinator ID redacted in this public release.
13. Coordinator model `anthropic/claude-sonnet-5.5`; специалисты
    `deepseek/deepseek-v4.1-flash`.
14. Coordinator Subagents: enabled, allowSelf false, shareFiles true,
    three child agent IDs (per-install IDs redacted).
15. Настоящий Coordinator → Analyst Subagent запуск подтверждён MongoDB
    и скриншотом. Один из последних успешных запусков завершился
    примерно за 7 секунд.
16. Analyst выполнил четыре последовательных MCP вызова в отдельном
    тесте.
17. Builder создал корректный XYZ Calibration Cube 20×20×20 мм.
18. Reviewer независимо подтвердил один Solid, Shape valid, объём 8000
    мм³, STL 12 facets и корректную целостность.
19. Cube FCStd/STL по последнему отчёту находятся в
    `<TEMP_DIR>/xyz-calibration-cube-test/`; SHA-256 приведены в разделе 5.6.
20. **Главный текущий блокер:** `<CAD_WORKSPACE>`
    принадлежит `root:root`, mode `0755`; FreeCAD UID 1000 не может
    создавать там проекты. GID пока неизвестен.
21. Не делать `chmod 777` и не выполнять рекурсивный `chown`. Сначала
    проверить UID/GID и решить ACL/ownership точечно.
22. `cad_revision.py` существует по
    `<CAD_AGENT_HOME>/bin/cad_revision.py`; его исходник нужно
    прочитать на VM, так как точный API здесь неизвестен.
23. Scratch revision tests ранее проходили, но текущий XYZ cube project
    не имеет постоянных before/after revisions.
24. Skills не подтверждены как созданные или назначенные.
25. EZ AI обычная генерация работает, но полный авторизованный каталог
    моделей, тарифы, Responses API и reasoning format не подтверждены.
26. `contextUsage` и `contextCost` включены в `librechat.yaml`;
    `tokenConfig` отсутствует, потому что тарифы EZ AI неизвестны.
27. Сессия после refresh, по сообщению пользователя, уже исправлена;
    детали неизвестны.
28. Не менять модели, промпты, MCP, Compose и не перезапускать сервисы
    без конкретной необходимости.
29. Следующая задача --- завершить постоянное сохранение уже созданного
    куба и ревизии, затем проверить Builder → Reviewer на изменении
    существующей модели.
30. Этот handoff основан только на доступной истории этого чата и трёх
    скриншотах; новые факты нужно подтверждать чтением исходных файлов
    на VM.

------------------------------------------------------------------------

## Приложение A. Ссылки, уже встречавшиеся в чате

-   LibreChat Docker: https://www.librechat.ai/docs/local/docker
-   LibreChat releases:
    https://github.com/LibreChat-AI/LibreChat/releases
-   LibreChat upgrade guide:
    https://www.librechat.ai/docs<FREECAD_CONFIG_ROOT>uration/upgrade
-   LibreChat config changelog:
    https://www.librechat.ai/changelog<FREECAD_CONFIG_ROOT>_v1.3.18
-   LibreChat v0.8.9-rc1 release notes:
    https://www.librechat.ai/changelog/v0.8.9-rc1
-   LibreChat custom endpoint:
    https://www.librechat.ai/docs<FREECAD_CONFIG_ROOT>uration/librechat_yaml/object_structure/custom_endpoint
-   LibreChat token usage:
    https://www.librechat.ai/docs<FREECAD_CONFIG_ROOT>uration/token_usage
-   LibreChat Admin Panel:
    https://www.librechat.ai/docs/features/admin_panel
-   LibreChat Agents API:
    https://www.librechat.ai/docs/features/agents_api
-   FreeCAD MCP Bridge: https://github.com/CREATeNG/freecad-mcp-bridge

Ссылки сохранены как ссылки, встречавшиеся в переписке; их актуальность
в рамках архивного извлечения заново не проверялась.

------------------------------------------------------------------------

**Конец handoff.**
