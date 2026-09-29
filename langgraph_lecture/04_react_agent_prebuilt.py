"""
Урок 4. Готовый ReAct-агент: create_agent + память (checkpointer)

===========================================================================
В уроках 2-3 мы вручную собрали граф "agent -> tools -> agent -> ...".
Это ровно то, что под капотом делает готовая фабрика агента -- она
возвращает уже скомпилированный граф с такой же структурой, плюс немного
полезных возможностей "из коробки":
    - системный промпт (system_prompt=...);
    - память между вызовами (checkpointer=...);
    - структурированный финальный ответ (response_format=...);
    - middleware -- хуки до/после вызова модели и вызова инструментов.

ВАЖНО ПРО ИМЕНА ФУНКЦИИ (актуально на момент написания лекции):
    - Раньше (и в большинстве статей/видео в интернете) эта функция
      называлась create_react_agent и импортировалась из
      langgraph.prebuilt.
    - Начиная с LangGraph 1.0 она официально помечена как deprecated и
      переехала в пакет langchain (`pip install langchain`) под именем
      create_agent: from langchain.agents import create_agent.
    - Разница в основном в двух местах: параметр системного промпта
      теперь называется system_prompt (было prompt), и вместо
      pre_model_hook/post_model_hook используется единый механизм
      middleware. Логика графа (agent -> tools -> agent) не изменилась.
    - Если вы встретите в старом туториале `from langgraph.prebuilt import
      create_react_agent` -- это тот же самый паттерн, просто устаревший
      способ его получить. Он ещё работает, но будет удалён в LangGraph 2.0.

===========================================================================
ПАМЯТЬ И thread_id
===========================================================================
LLM сам по себе не помнит предыдущие сообщения -- каждый invoke() это
независимый запрос. "Память" в LangGraph -- это checkpointer: компонент,
который после каждого шага графа сохраняет state (то есть в первую очередь
список messages) под неким ключом thread_id. При следующем вызове с тем же
thread_id граф сначала подгружает сохранённое состояние, а потом добавляет
к нему новые сообщения.

Это значит:
    - один thread_id = один диалог (например, один чат с одним пользователем);
    - разные thread_id = независимые, ничего не знающие друг о друге диалоги;
    - InMemorySaver хранит всё в оперативной памяти процесса (пропадает при
      перезапуске) -- для продакшена есть SqliteSaver / PostgresSaver и т.д.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 04_react_agent_prebuilt.py
"""

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


@tool
def get_user_balance(user_id: str) -> str:
    """Возвращает баланс счёта пользователя по его id."""
    fake_balances = {"u1": "15 000 руб.", "u2": "-500 руб. (задолженность)"}
    return fake_balances.get(user_id, "Пользователь не найден")


def build_agent():
    llm = get_llm()
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[get_user_balance],
        # system_prompt задаёт системную инструкцию -- поведение и
        # "личность" агента.
        system_prompt=(
            "Ты -- вежливый ассистент службы поддержки банка. "
            "Отвечай кратко, по-русски. Если нужен баланс пользователя -- "
            "используй инструмент get_user_balance."
        ),
        checkpointer=checkpointer,
    )
    return agent


def main():
    agent = build_agent()

    # thread_id объединяет несколько вызовов в один диалог с памятью.
    config = {"configurable": {"thread_id": "client-42"}}

    print("=== Сообщение 1 ===")
    result = agent.invoke(
        {"messages": [HumanMessage("Привет! Меня зовут Алексей, мой id u1.")]},
        config=config,
    )
    result["messages"][-1].pretty_print()

    print("\n=== Сообщение 2 (проверяем память: агент должен помнить id) ===")
    result = agent.invoke(
        {"messages": [HumanMessage("Какой у меня баланс?")]},
        config=config,
    )
    result["messages"][-1].pretty_print()

    print("\n=== Сообщение 3 (проверяем память: агент должен помнить имя) ===")
    result = agent.invoke(
        {"messages": [HumanMessage("Как меня зовут?")]},
        config=config,
    )
    result["messages"][-1].pretty_print()

    print("\n=== Новый диалог (другой thread_id -- памяти о клиенте НЕТ) ===")
    other_config = {"configurable": {"thread_id": "client-99"}}
    result = agent.invoke(
        {"messages": [HumanMessage("Как меня зовут?")]},
        config=other_config,
    )
    result["messages"][-1].pretty_print()

    print("\n=== Стриминг ответа по токенам/шагам ===")
    for chunk, metadata in agent.stream(
        {"messages": [HumanMessage("Какой у меня баланс, повтори кратко?")]},
        config=config,
        stream_mode="messages",
    ):
        if chunk.content:
            print(chunk.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
