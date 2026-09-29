"""
Урок 2. Инструменты (tools) и условные рёбра: строительные блоки ReAct

===========================================================================
ЧТО ТАКОЕ ReAct
===========================================================================
ReAct (Reason + Act) -- это простой, но мощный паттерн работы агента:

    1. Модель СМОТРИТ на историю сообщений и РАССУЖДАЕТ, что делать дальше.
    2. Если для ответа не хватает данных -- модель РЕШАЕТ вызвать инструмент
       (например, поиск, калькулятор, обращение к API).
    3. Инструмент выполняется, его результат добавляется в историю.
    4. Модель снова смотрит на (уже расширенную) историю -- и так по кругу,
       пока не решит, что готова дать финальный ответ.

В LangGraph это буквально маленький граф с ЦИКЛОМ:

              +-------+          tool_calls есть           +-------+
    START --> | agent | ------------------------------->   | tools |
              +-------+                                    +-------+
                  ^                                             |
                  |                    результат инструмента     |
                  +---------------------------------------------+
                  |
                  | tool_calls нет (модель ответила текстом)
                  v
                 END

В этом уроке мы соберём именно этот граф руками, используя готовые
"кирпичики" LangGraph:
    - ToolNode        -- узел, который сам выполняет инструменты,
                          на которые указала модель;
    - tools_condition -- готовая функция-роутер: смотрит, есть ли в
                          последнем сообщении tool_calls, и решает,
                          идти ли в узел "tools" или сразу в END.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 02_tools_and_conditional_edges.py
"""

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


# ---------------------------------------------------------------------------
# Состояние агента почти всегда одно и то же: список сообщений.
# add_messages -- это "редьюсер": вместо того чтобы ЗАМЕНЯТЬ список
# сообщений при каждом обновлении state, LangGraph будет ДОПИСЫВАТЬ в него
# новые сообщения (и умеет корректно обновлять сообщение по id).
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------------------------
# Инструменты -- обычные python-функции с декоратором @tool.
# Докстринг ВАЖЕН: именно его модель видит как описание инструмента и
# по нему решает, когда и как его вызывать.
# ---------------------------------------------------------------------------
@tool
def get_weather(city: str) -> str:
    """Возвращает текущую погоду в указанном городе.

    Используй этот инструмент, когда пользователь спрашивает про погоду.
    """
    # Заглушка вместо реального обращения к API погоды -- фокус урока на
    # механике графа, а не на интеграциях.
    fake_db = {
        "москва": "+20°C, солнечно",
        "лондон": "+14°C, дождь",
        "дубай": "+38°C, ясно",
    }
    return fake_db.get(city.lower(), f"Нет данных о погоде в городе {city}")


@tool
def calculator(expression: str) -> str:
    """Вычисляет простое арифметическое выражение, например '23 * 7 + 1'."""
    try:
        # eval здесь безопасен для учебного примера (только числа и операторы),
        # в проде так делать не стоит -- используйте безопасный парсер выражений.
        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed:
            return "Ошибка: выражение содержит недопустимые символы"
        return str(eval(expression))
    except Exception as exc:  # noqa: BLE001 -- учебный пример
        return f"Ошибка вычисления: {exc}"


tools = [get_weather, calculator]


def build_graph():
    llm = get_llm()
    # bind_tools "рассказывает" модели, какие инструменты у неё есть, и в
    # каком формате (JSON schema) вызывать каждый. После этого модель сама
    # решает, вызывать инструмент или нет -- мы её к этому не принуждаем.
    llm_with_tools = llm.bind_tools(tools)

    def call_model(state: AgentState) -> dict:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "agent")
    # tools_condition читает последнее AIMessage: если у него есть
    # tool_calls -> вернёт "tools", иначе -> вернёт END.
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


def main():
    graph = build_graph()

    questions = [
        "Какая погода в Дубае?",
        "Сколько будет (23 + 19) * 2?",
        "Просто скажи привет, без инструментов.",
    ]

    for question in questions:
        print(f"\n=== Вопрос: {question} ===")
        result = graph.invoke({"messages": [HumanMessage(question)]})
        for msg in result["messages"]:
            msg.pretty_print()


if __name__ == "__main__":
    main()
