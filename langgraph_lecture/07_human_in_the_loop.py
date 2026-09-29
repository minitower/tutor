"""
Урок 7. Human-in-the-loop: подтверждение действий человеком

===========================================================================
ЗАЧЕМ ЭТО НУЖНО
===========================================================================
Некоторые инструменты слишком рискованны, чтобы разрешать модели вызывать
их без контроля: перевод денег, отправка письма клиенту, удаление данных.
LangGraph позволяет ОСТАНОВИТЬ выполнение графа прямо посреди узла,
дождаться решения человека, а потом ПРОДОЛЖИТЬ выполнение с того же места
-- как будто мы поставили точку останова (breakpoint) в блок-схеме.

===========================================================================
КАК ЭТО РАБОТАЕТ: interrupt() и Command(resume=...)
===========================================================================
    1. Внутри узла вызывается interrupt(payload) -- любые данные, которые
       нужно показать человеку (например, что за инструмент и с какими
       аргументами хочет вызвать модель).
    2. Выполнение графа приостанавливается. graph.invoke(...) при этом не
       падает с ошибкой -- он просто возвращает состояние, где будет ключ
       "__interrupt__" со сведениями о том, на чём остановились.
    3. Мы показываем payload человеку (в реальном приложении -- в UI),
       получаем его решение.
    4. Возобновляем граф: graph.invoke(Command(resume=решение), config=...)
       -- ВАЖНО: обязательно с тем же thread_id/config, что и раньше,
       потому что состояние на паузе хранится в checkpointer'е.
    5. Функция interrupt() в этот момент как бы "возвращает" значение
       resume, и код узла продолжает выполняться с этого места.

Это ОБЯЗАТЕЛЬНО требует checkpointer -- без сохранённого состояния
LangGraph не сможет понять, откуда продолжать выполнение.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск (интерактивный -- в терминале нужно будет ответить да/нет):
    python 07_human_in_the_loop.py
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def send_money(to: str, amount: int) -> str:
    """Отправляет денежный перевод указанному получателю."""
    return f"Перевод выполнен: {amount} руб. получателю {to}."


TOOLS = [send_money]


def build_graph():
    llm_with_tools = get_llm().bind_tools(TOOLS)

    def agent_node(state: State) -> dict:
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    def human_review(state: State) -> Command[Literal["tools", "agent"]]:
        last_message = state["messages"][-1]
        tool_call = last_message.tool_calls[0]

        # interrupt() приостанавливает граф и "передаёт наружу" payload.
        # То, что вернёт эта функция при возобновлении -- это то, что мы
        # передадим в Command(resume=...).
        decision = interrupt(
            {
                "question": (
                    f"Разрешить вызов инструмента '{tool_call['name']}' "
                    f"с аргументами {tool_call['args']}?"
                ),
                "tool_call": tool_call,
            }
        )

        if decision == "approve":
            return Command(goto="tools")

        # Если человек отклонил вызов -- НЕ выполняем инструмент, а сразу
        # кладём в историю ToolMessage с отказом и возвращаемся к модели,
        # чтобы она смогла отреагировать (например, извиниться и уточнить).
        rejection = ToolMessage(
            content="Пользователь отклонил выполнение этого действия.",
            tool_call_id=tool_call["id"],
        )
        return Command(goto="agent", update={"messages": [rejection]})

    def route_after_agent(state: State) -> str:
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "human_review"
        return END

    builder = StateGraph(State)
    builder.add_node("agent", agent_node)
    builder.add_node("human_review", human_review)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent", route_after_agent, {"human_review": "human_review", END: END}
    )
    builder.add_edge("tools", "agent")

    # checkpointer ОБЯЗАТЕЛЕН для работы interrupt()/Command(resume=...).
    return builder.compile(checkpointer=InMemorySaver())


def ask_human(question: str) -> str:
    print(f"\n[Нужно подтверждение] {question}")
    answer = input("Разрешить? (да/нет): ").strip().lower()
    return "approve" if answer in ("да", "yes", "y", "д") else "reject"


def main():
    graph = build_graph()
    config = {"configurable": {"thread_id": "hil-demo"}}

    result = graph.invoke(
        {"messages": [HumanMessage("Переведи 5000 рублей Ивану")]},
        config=config,
    )

    # Пока в состоянии есть незакрытые interrupt'ы -- продолжаем спрашивать
    # человека и возобновлять граф. В реальном приложении на этом месте
    # был бы, например, HTTP-запрос, ожидающий клика в UI.
    while result.get("__interrupt__"):
        pending = result["__interrupt__"][0]
        decision = ask_human(pending.value["question"])
        result = graph.invoke(Command(resume=decision), config=config)

    print("\n=== Итоговая история диалога ===")
    for msg in result["messages"]:
        msg.pretty_print()


if __name__ == "__main__":
    main()
