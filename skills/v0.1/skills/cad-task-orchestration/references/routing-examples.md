# Dispatch examples

1. "Как бы сделать нависание на противоположной грани?" → brainstorming, no tools unless existing geometry matters.
2. "Какой сейчас размер отверстия?" → use last trusted measurement if unchanged; if uncertain → Analyst.
3. "Нанеси три буквы на X/Y/Z грани, вырежи их и обнови STL" → Builder; Reviewer checks feature/mesh. **Not** a simple Coordinator-only adjustment.
4. "Увеличь один известный параметр ширины" → Builder when it mutates CAD; a direct Coordinator edit is a narrowly justified exception only if policy explicitly permits and proper checkpoint/review still occurs.
5. "Вот новый FCStd, разберись, почему ломается" → Analyst inspection first; if repair requested → Builder and then Reviewer.
6. "Закончили?" → answer with revision evidence; no invented completion.
7. "READY" → ordinary language-only response. If stuck, diagnose upstream service; no MCP.
