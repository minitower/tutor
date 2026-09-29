"""
Урок 6. Мультиагентная система: паттерн "handoff / swarm"

===========================================================================
СУПЕРВИЗОР VS SWARM
===========================================================================
В уроке 5 всеми переходами управлял ОДИН узел-супервизор: агенты сами
никогда не решали, кому передать разговор -- решение всегда возвращалось
наверх. Это просто и предсказуемо, но добавляет "прослойку" на каждый шаг.

Паттерн "handoff" (в LangChain-экосистеме также называют "swarm") устроен
иначе: агенты РАВНОПРАВНЫ и могут передавать разговор ДРУГ ДРУГУ напрямую,
если считают это нужным -- через обычный вызов инструмента.

              transfer_to_coder()
   +------------+  ------------->   +---------+
   | researcher |                   |  coder  |
   +------------+  <-------------   +---------+
              transfer_to_researcher()

Как это работает технически:
    1. Для каждого агента создаём "инструмент передачи" (handoff tool) --
       по сути это просто ещё один @tool, который, вместо того чтобы
       вернуть текст, возвращает langgraph.types.Command.
    2. Command(goto=<имя другого агента>, update=..., graph=Command.PARENT)
       говорит LangGraph: "не оставайся внутри текущего под-агента,
       поднимись на уровень выше (в родительский граф) и перейди в узел
       с указанным именем". Это ключевой трюк, который отличает handoff
       от обычного вызова инструмента.
    3. Каждый агент-узел -- это самостоятельный create_agent(...) с
       собственным набором инструментов, включая инструменты передачи
       управления другим агентам.

Когда выбирать какой паттерн:
    - Supervisor -- когда нужен предсказуемый, легко управляемый и
      логируемый процесс (например, воронка поддержки с чёткими этапами).
    - Handoff/swarm -- когда агенты по сути равноправные специалисты и
      естественнее, чтобы, например, "агент-исследователь", поняв, что
      дальше нужен код, сам передавал эстафету "агенту-программисту",
      без лишнего централизованного диспетчера.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 06_multi_agent_handoff_swarm.py
"""

from typing import Annotated

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


def make_handoff_tool(*, agent_name: str):
    """Фабрика инструментов передачи управления другому агенту.

    InjectedState и InjectedToolCallId -- специальные аннотации LangGraph:
    их значения модель НЕ придумывает и не передаёт сама, LangGraph
    подставляет их автоматически (текущее состояние графа и id вызова
    инструмента соответственно). Модели для вызова этого инструмента
    вообще не нужно указывать никаких аргументов.
    """
    tool_name = f"transfer_to_{agent_name}"

    # description передаём явным параметром, а не докстрингом: докстрока
    # должна быть литеральной строкой (известной на этапе компиляции), а
    # нам нужно подставить в неё agent_name из аргумента функции.
    @tool(tool_name, description=f"Передать разговор агенту '{agent_name}', когда его специализация подходит лучше.")
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = ToolMessage(
            content=f"Разговор передан агенту {agent_name}.",
            name=tool_name,
            tool_call_id=tool_call_id,
        )
        return Command(
            # graph=Command.PARENT -- переход происходит не внутри текущего
            # под-агента, а в родительском графе, который объединяет всех
            # агентов (см. builder ниже).
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )

    return handoff_tool


@tool
def web_search(query: str) -> str:
    """Ищет информацию в интернете по запросу."""
    return (
        f"По запросу '{query}': LangGraph поддерживает паттерн swarm, где "
        "агенты передают друг другу управление напрямую через инструменты."
    )


@tool
def write_code(task: str) -> str:
    """Пишет короткий фрагмент кода для решения задачи (заглушка)."""
    return f"# решение для: {task}\nprint('готово')"


def build_graph():
    llm = get_llm()

    transfer_to_coder = make_handoff_tool(agent_name="coder")
    transfer_to_researcher = make_handoff_tool(agent_name="researcher")

    researcher = create_agent(
        model=llm,
        tools=[web_search, transfer_to_coder],
        system_prompt=(
            "Ты -- агент-исследователь. Ищи факты через web_search. "
            "Если пользователь просит написать код -- вызови "
            "transfer_to_coder вместо того, чтобы пытаться сделать это самому."
        ),
        name="researcher",
    )
    coder = create_agent(
        model=llm,
        tools=[write_code, transfer_to_researcher],
        system_prompt=(
            "Ты -- агент-программист. Пиши код через write_code. "
            "Если нужно поискать факты в интернете -- вызови "
            "transfer_to_researcher вместо того, чтобы придумывать факты самому."
        ),
        name="coder",
    )

    # Родительский граф: узлами являются ЦЕЛЫЕ агенты (каждый из них --
    # уже скомпилированный подграф). Явные рёбра между researcher и coder
    # не нужны -- переходы задаются через Command(goto=..., graph=PARENT)
    # внутри handoff-инструментов.
    builder = StateGraph(MessagesState)
    builder.add_node("researcher", researcher)
    builder.add_node("coder", coder)
    builder.add_edge(START, "researcher")  # с кого начинаем разговор по умолчанию

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


def main():
    graph = build_graph()
    config = {"configurable": {"thread_id": "swarm-demo"}}

    question = (
        "Расскажи, что такое паттерн swarm в LangGraph, а потом напиши "
        "функцию на python, которая складывает два числа."
    )
    print(f"=== Вопрос: {question} ===\n")
    result = graph.invoke(
        {"messages": [HumanMessage(question)]},
        config=config | {"recursion_limit": 25},
    )

    print("=== Полная история диалога ===")
    for msg in result["messages"]:
        speaker = getattr(msg, "name", None) or type(msg).__name__
        print(f"[{speaker}] {msg.content}")


if __name__ == "__main__":
    main()
