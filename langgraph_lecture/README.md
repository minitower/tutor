# Лекция: LangGraph, ReAct-агенты и мультиагентные системы

Практическая лекция на Python (комментарии и объяснения на русском) о
построении агентов с помощью [LangGraph](https://github.com/langchain-ai/langgraph):
от базовых графов до мультиагентных систем и human-in-the-loop.

## Установка

```bash
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и впишите свой ключ
[OpenRouter](https://openrouter.ai/keys):

```
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=anthropic/claude-sonnet-4.5
```

`.env` подхватывается автоматически (через `python-dotenv`) -- ничего
дополнительно активировать не нужно. Можно и без файла `.env`, задав те же
переменные напрямую в окружении:

```bash
export OPENROUTER_API_KEY=sk-or-v1-...      # Linux / macOS
$env:OPENROUTER_API_KEY = "sk-or-v1-..."    # PowerShell
```

Файл `01_graph_basics.py` не требует API-ключа -- с него удобно начать,
чтобы проверить, что всё установилось.

## Структура лекции

| Файл | Тема | Ключевые понятия LangGraph |
|---|---|---|
| [`01_graph_basics.py`](01_graph_basics.py) | Основы: State, узлы, рёбра | `StateGraph`, `add_node`, `add_edge`, условные рёбра, `compile()`, `invoke`/`stream` |
| [`02_tools_and_conditional_edges.py`](02_tools_and_conditional_edges.py) | Инструменты и цикл ReAct | `@tool`, `bind_tools`, `ToolNode`, `tools_condition` |
| [`03_react_agent_from_scratch.py`](03_react_agent_from_scratch.py) | ReAct-агент руками, без prebuilt | ручной роутер, ручная обработка нескольких tool_calls, лимит шагов |
| [`04_react_agent_prebuilt.py`](04_react_agent_prebuilt.py) | Готовый агент и память | `create_agent`, `checkpointer`, `thread_id`, `stream_mode="messages"` |
| [`05_multi_agent_supervisor.py`](05_multi_agent_supervisor.py) | Мультиагент: супервизор | `Command(goto=...)`, `with_structured_output`, роутинг через LLM |
| [`06_multi_agent_handoff_swarm.py`](06_multi_agent_handoff_swarm.py) | Мультиагент: handoff / swarm | `Command(graph=Command.PARENT)`, `InjectedState`, `InjectedToolCallId` |
| [`07_human_in_the_loop.py`](07_human_in_the_loop.py) | Подтверждение действий человеком | `interrupt()`, `Command(resume=...)`, пауза/возобновление графа |
| [`08_dynamic_agent_factory.py`](08_dynamic_agent_factory.py) | Динамическое создание агентов ("agent-as-a-tool") | агент как инструмент, мета-агент, лимит глубины/бюджета, белый список инструментов |

Дополнительно: [`exercises.md`](exercises.md) -- практические задания к
каждому уроку и финальный учебный проект.

## Рекомендуемый порядок изучения

Уроки написаны как последовательность -- каждый следующий опирается на
понятия из предыдущего:

1. **Урок 1** -- поймите, что граф это просто функции + правила переходов
   между ними, без всякой связи с LLM.
2. **Урок 2** -- добавляем LLM и инструменты, знакомимся с готовыми
   кирпичиками `ToolNode`/`tools_condition`.
3. **Урок 3** -- разбираем эти кирпичики "по кости", строя тот же цикл
   вручную. Это самый важный урок для понимания внутренностей.
4. **Урок 4** -- возвращаемся к готовым решениям (`create_agent`), но уже
   осознанно понимая, что происходит внутри, и добавляем память.
5. **Уроки 5-6** -- от одного агента переходим к системе из нескольких:
   сначала централизованный супервизор, потом равноправные агенты с
   передачей управления друг другу.
6. **Урок 7** -- учимся безопасно встраивать в агента точки, где решение
   принимает человек.
7. **Урок 8** -- идём дальше фиксированного набора агентов: LLM сама решает,
   какого агента создать и с какими инструментами, через обычный вызов
   инструмента. Разбираем, какие ограничения обязательны, чтобы это не
   превратилось в неконтролируемый "форк-бомб" из агентов.

## Важное замечание про версии API

LangGraph и экосистема LangChain развиваются очень быстро. Эта лекция
написана и проверена на:

- `langgraph == 1.2.11`
- `langchain == 1.4.0`
- `langchain-core == 1.6.2`
- `langchain-openai == 1.x` (используется как OpenAI-совместимый клиент для OpenRouter)

Одна из самых частых причин, по которой старые статьи/видео про LangGraph
перестают работать "как написано": функция построения готового ReAct-агента
раньше называлась `create_react_agent` и лежала в `langgraph.prebuilt`.
Начиная с LangGraph 1.0 она объявлена устаревшей (ещё работает, но будет
удалена в 2.0) в пользу `create_agent` из пакета `langchain.agents` -- в
этой лекции (урок 4 и далее) используется именно новый вариант. Подробности
и разница в параметрах -- в комментариях в начале `04_react_agent_prebuilt.py`.

Если что-то в коде расходится с официальной документацией на момент, когда
вы это читаете -- доверяйте документации: `pip show langgraph langchain`
покажет установленную версию, а `python -c "import langgraph.prebuilt as m;
help(m)"` -- актуальный набор функций.

## Модель

Все примеры ходят к LLM через [OpenRouter](https://openrouter.ai/) --
единый OpenAI-совместимый API поверх множества провайдеров и моделей
(`common/llm.py`). Какую модель использовать, задаётся СТРОКОЙ в `.env`
(`OPENROUTER_MODEL`), без изменения кода:

```
OPENROUTER_MODEL=anthropic/claude-sonnet-4.5      # по умолчанию в этой лекции
OPENROUTER_MODEL=openai/gpt-4o
OPENROUTER_MODEL=google/gemini-2.5-pro
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
OPENROUTER_MODEL=deepseek/deepseek-chat
```

Полный и актуальный список моделей (и их id в нужном формате
"провайдер/модель") -- на https://openrouter.ai/models. Для мультиагентных
примеров и урока 8 (динамическая фабрика агентов) лучше выбирать модель с
хорошей поддержкой вызова инструментов (tool calling) -- это отмечено на
странице модели на OpenRouter значком "Tools".

Можно также передать модель прямо в коде, не трогая `.env`:
`get_llm(model="openai/gpt-4o-mini")`.

## Частые проблемы

- **Кракозябры вместо русского текста в консоли Windows.** Все скрипты
  вызывают `ensure_utf8_console()` в начале, но если проблема всё же
  возникла -- выполните в PowerShell `chcp 65001` перед запуском.
- **`ImportError: Install grandalf to draw graphs`.** Нужен пакет
  `grandalf` (есть в `requirements.txt`) -- без него просто не отображается
  ASCII-схема графа, на остальную логику это не влияет.
- **`RuntimeError: Не найден OPENROUTER_API_KEY`.** Смотрите раздел
  "Установка" выше -- скорее всего, не создан `.env` или ключ вписан в
  неправильный файл (должен называться именно `.env`, не `.env.example`).
- **Модель "не умеет" вызывать инструменты / агент никогда не вызывает
  tools.** Не каждая модель на OpenRouter одинаково хорошо поддерживает
  tool calling -- проверьте на https://openrouter.ai/models, что у выбранной
  модели есть значок "Tools", и попробуйте, например,
  `anthropic/claude-sonnet-4.5` или `openai/gpt-4o`.
