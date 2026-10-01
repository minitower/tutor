# Модуль 4 — Skills: навыки агента

## Цели обучения
- Писать, тестировать и безопасно применять skills — переиспользуемые процедуры агента

## Ключевые концепции
- Skill = папка с `SKILL.md` (frontmatter + инструкции) и вспомогательными файлами; progressive disclosure в три уровня
- Кто вызывает: `/имя` или модель по `description`; `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context: fork`, `paths`, `hooks`
- Аргументы, динамический контекст, скрипты; расположение (personal / project / plugin / enterprise)
- Skill vs. CLAUDE.md vs. hook vs. MCP vs. subagent; открытый стандарт Agent Skills
- Безопасность (`allowed-tools`, сторонние skills, правила `Skill(...)`) и тестирование (срабатывание, baseline с/без)

## Лабораторная работа
Упакуйте повторяющуюся процедуру в skill, составьте набор запросов «должен / не должен срабатывать», сравните с baseline без skill и оформите заметку по безопасности.

## Результат
Папка skill, набор из 10 запросов с таблицей результатов и заметка по безопасности.
