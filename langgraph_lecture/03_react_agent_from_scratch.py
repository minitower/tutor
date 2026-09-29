"""
Урок 3. ReAct-агент "из первых принципов"

===========================================================================
В прошлом уроке мы уже фактически построили ReAct-агента, использовав
готовые ToolNode и tools_condition. В этом уроке мы напишем ИХ ЛОГИКУ
руками, без "магии" prebuilt-модулей -- чтобы до конца понимать, что
происходит внутри, когда в уроке 4 мы перейдём на create_agent().

Зачем это нужно, если в LangGraph уже есть готовая функция?
    - Готовый create_agent() отлично подходит для 80% случаев,
      но когда потребуется НЕСТАНДАРТНОЕ поведение (особая логика выбора
      инструмента, ограничение числа шагов, кастомная обработка ошибок
      инструмента и т.д.) -- вам придётся написать граф самим, ровно как
      здесь.
    - Понимание внутренностей -- лучшая защита от ситуации "код работает,
      но я не понимаю, почему".

Мы напишем:
    1. Узел agent_node -- вызывает LLM с инструментами.
    2. Узел tools_node -- вручную находит нужный python-инструмент по
       имени и исполняет его для КАЖДОГО tool_call в последнем сообщении
       (модель может попросить вызвать сразу несколько инструментов).
    3. Роутер should_continue -- аналог tools_condition, но написанный
       руками.
    4. Ограничение на число шагов (max_steps) -- то, чего нет "из коробки"
       в prebuilt-версии, но легко добавляется в своём графе.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 03_react_agent_from_scratch.py
"""

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    steps: int  # счётчик шагов -- своя добавка поверх стандартного состояния


@tool
def search_docs(query: str) -> str:
    """Ищет ответ в базе знаний компании (заглушка для учебного примера)."""
    fake_kb = {
        "отпуск": "Отпуск оформляется через HR-портал за 2 недели до даты начала.",
        "больничный": "Больничный лист нужно загрузить в личный кабинет в течение 3 дней.",
    }
    for key, value in fake_kb.items():
        if key in query.lower():
            return value
    return "По этому запросу ничего не найдено в базе знаний."


@tool
def escalate_to_human(reason: str) -> str:
    """Передаёт вопрос живому сотруднику поддержки, если агент не справился."""
    return f"Вопрос передан специалисту поддержки. Причина: {reason}"


TOOLS = [search_docs, escalate_to_human]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}
MAX_STEPS = 4


def build_graph():
    llm_with_tools = get_llm().bind_tools(TOOLS)

    def agent_node(state: AgentState) -> dict:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response], "steps": state.get("steps", 0) + 1}

    def tools_node(state: AgentState) -> dict:
        last_message = state["messages"][-1]
        tool_messages = []
        # Модель могла попросить вызвать НЕСКОЛЬКО инструментов за один шаг
        # (parallel tool calls) -- обрабатываем их все.
        for tool_call in last_message.tool_calls:
            tool_fn = TOOLS_BY_NAME[tool_call["name"]]
            try:
                result = tool_fn.invoke(tool_call["args"])
            except Exception as exc:  # noqa: BLE001 -- учебный пример
                result = f"Ошибка при вызове инструмента: {exc}"
            tool_messages.append(
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])
            )
        return {"messages": tool_messages}

    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]

        # Наша собственная логика, которой нет в готовом tools_condition:
        # жёсткий лимит на число шагов, чтобы агент не мог зациклиться
        # бесконечно (например, если инструмент всегда возвращает ошибку,
        # а модель раз за разом пытается его перевызвать).
        if state.get("steps", 0) >= MAX_STEPS:
            return "stop_forced"

        if getattr(last_message, "tool_calls", None):
            return "call_tools"

        return "finish"

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tools_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {"call_tools": "tools", "finish": END, "stop_forced": END},
    )
    builder.add_edge("tools", "agent")

    return builder.compile()


def main():
    graph = build_graph()

    for question in [
        "Как оформить отпуск?",
        "У меня сломался принтер, что делать?",
    ]:
        print(f"\n=== Вопрос: {question} ===")
        result = graph.invoke({"messages": [HumanMessage(question)], "steps": 0})
        for msg in result["messages"]:
            msg.pretty_print()
        print(f"(сделано шагов: {result['steps']})")


if __name__ == "__main__":
    main()
