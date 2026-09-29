"""
Урок 5. Мультиагентная система: паттерн "супервизор" (supervisor)

===========================================================================
ЗАЧЕМ НУЖНО НЕСКОЛЬКО АГЕНТОВ
===========================================================================
Один агент с десятком инструментов и длинным системным промптом рано или
поздно начинает "путаться": промпт разрастается, инструменты пересекаются
по смыслу, модели сложнее решить, что использовать. Практический выход --
разбить систему на НЕСКОЛЬКИХ узкоспециализированных агентов и добавить
координатора, который решает, кому передать текущий вопрос.

===========================================================================
ПАТТЕРН SUPERVISOR
===========================================================================
Это самый распространённый и предсказуемый способ построить мультиагентную
систему в LangGraph:

                     +-------------+
        +----------> | supervisor  | <----------+
        |            +-------------+             |
        |             /            \\             |
        | Command    /              \\   Command   |
        | (goto)    v                v  (goto)    |
   +-----------+          +-------------+
   | researcher |          |    coder    |
   +-----------+          +-------------+

    - supervisor -- узел с LLM, который смотрит на диалог и с помощью
      structured output решает: "сейчас нужен researcher", "нужен coder"
      или "можно закончить (FINISH)".
    - Каждый worker-агент (researcher, coder) -- это ЦЕЛЫЙ ReAct-агент
      (мы используем create_agent из урока 4) внутри одного узла.
    - После работы worker'а управление ВСЕГДА возвращается супервизору --
      это гарантирует, что решение "что делать дальше" принимается в одном
      месте, а не размазано по всей системе.

Технически переходы между узлами делаются через langgraph.types.Command:
узел возвращает Command(goto="имя_узла", update={...}) -- это одновременно
и обновление состояния, и явное указание, куда идти дальше. Это удобнее
классических conditional_edges, когда переходов много и они завязаны на
результат работы LLM, а не на простое условие.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 05_multi_agent_supervisor.py
"""

from typing import Annotated, Literal, TypedDict

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Command
from pydantic import BaseModel, Field

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


class State(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------------------------
# Инструменты для worker-агентов (заглушки для учебного примера).
# ---------------------------------------------------------------------------
@tool
def web_search(query: str) -> str:
    """Ищет информацию в интернете по запросу."""
    return (
        f"Результаты поиска по запросу '{query}': LangGraph -- библиотека "
        "для построения агентов и мультиагентных систем поверх LangChain, "
        "разработана командой LangChain в 2024 году."
    )


@tool
def run_python(code: str) -> str:
    """Выполняет короткий фрагмент python-кода и возвращает результат."""
    try:
        allowed = set("0123456789+-*/(). ")
        expression = code.strip()
        if not set(expression) <= allowed:
            return "Ошибка: в учебном примере разрешена только арифметика"
        return str(eval(expression))
    except Exception as exc:  # noqa: BLE001 -- учебный пример
        return f"Ошибка выполнения: {exc}"


# ---------------------------------------------------------------------------
# Структурированный ответ супервизора: строго "researcher", "coder" или
# "FINISH". with_structured_output заставляет модель вернуть JSON,
# который сразу превращается в pydantic-объект -- не нужно парсить текст.
# ---------------------------------------------------------------------------
class RouteDecision(BaseModel):
    next: Literal["researcher", "coder", "FINISH"] = Field(
        description=(
            "Кого вызвать следующим. researcher -- если нужно найти "
            "информацию; coder -- если нужно что-то посчитать или "
            "написать код; FINISH -- если на вопрос уже есть полный ответ."
        )
    )


SUPERVISOR_PROMPT = (
    "Ты -- супервизор, который управляет двумя агентами: researcher и "
    "coder. researcher ищет информацию, coder считает и пишет код. "
    "Посмотри на диалог и реши, кого вызвать следующим, либо закончи "
    "(FINISH), если ответ уже дан."
)


def build_graph():
    llm = get_llm()
    router_llm = llm.with_structured_output(RouteDecision)

    researcher_agent = create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="Ты -- агент-исследователь. Только ищи факты, не выполняй код.",
    )
    coder_agent = create_agent(
        model=llm,
        tools=[run_python],
        system_prompt="Ты -- агент-программист. Только считай/пиши код, не ищи в интернете.",
    )

    def supervisor(state: State) -> Command[Literal["researcher", "coder", "__end__"]]:
        messages = [{"role": "system", "content": SUPERVISOR_PROMPT}] + state["messages"]
        decision = router_llm.invoke(messages)
        print(f"[supervisor] решение: {decision.next}")
        if decision.next == "FINISH":
            return Command(goto=END)
        return Command(goto=decision.next)

    def researcher_node(state: State) -> Command[Literal["supervisor"]]:
        result = researcher_agent.invoke({"messages": state["messages"]})
        last = result["messages"][-1]
        return Command(
            update={"messages": [AIMessage(content=last.content, name="researcher")]},
            goto="supervisor",
        )

    def coder_node(state: State) -> Command[Literal["supervisor"]]:
        result = coder_agent.invoke({"messages": state["messages"]})
        last = result["messages"][-1]
        return Command(
            update={"messages": [AIMessage(content=last.content, name="coder")]},
            goto="supervisor",
        )

    builder = StateGraph(State)
    builder.add_node("supervisor", supervisor)
    builder.add_node("researcher", researcher_node)
    builder.add_node("coder", coder_node)
    builder.add_edge(START, "supervisor")
    # Обратите внимание: рёбра researcher -> supervisor и coder -> supervisor
    # отдельно не объявляются -- переход задаётся прямо в Command(goto=...),
    # который возвращает каждый узел.

    return builder.compile()


def main():
    graph = build_graph()

    question = (
        "Что такое LangGraph и сколько будет 12 * 8, если умножить результат "
        "на 2?"
    )
    print(f"=== Вопрос: {question} ===\n")
    result = graph.invoke(
        {"messages": [HumanMessage(question)]},
        # На случай зацикливания супервизора ставим разумный лимит шагов.
        config={"recursion_limit": 15},
    )

    print("\n=== Полная история диалога ===")
    for msg in result["messages"]:
        speaker = getattr(msg, "name", None) or type(msg).__name__
        print(f"[{speaker}] {msg.content}")


if __name__ == "__main__":
    main()
