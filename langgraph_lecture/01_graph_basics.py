"""
Урок 1. Основы LangGraph: State, узлы (nodes), рёбра (edges)

===========================================================================
ИДЕЯ LANGGRAPH
===========================================================================
LangChain даёт вам "кубики" (модели, промпты, инструменты). LangGraph даёт
вам способ соединить эти кубики в ГРАФ выполнения -- как блок-схему:
    - узлы (nodes)  -- это шаги, обычные python-функции (или Runnable);
    - рёбра (edges) -- определяют, какой узел выполняется следующим;
    - state (состояние) -- общий "рюкзак" данных, который передаётся
      от узла к узлу и который каждый узел может дополнять.

В отличие от простой цепочки (LangChain Chain), граф может:
    - ветвиться (условные переходы -- conditional edges);
    - зацикливаться (агент может несколько раз вызывать инструменты);
    - хранить состояние между вызовами (память, checkpoints);
    - объединять несколько агентов в одну систему.

Именно поэтому LangGraph -- стандартный способ строить агентов в экосистеме
LangChain: ReAct-агент -- это просто граф с циклом "модель -> инструмент ->
модель -> ...", а мультиагентная система -- это граф, где узлами являются
целые агенты.

Запуск:
    python 01_graph_basics.py
(для этого файла API-ключ не нужен -- он не обращается к LLM)
"""

from typing import TypedDict

from common.console import ensure_utf8_console

ensure_utf8_console()


# ---------------------------------------------------------------------------
# Шаг 1. Опишем состояние графа.
#
# Состояние -- это обычный TypedDict (или pydantic-модель). Каждый узел
# получает на вход текущее состояние и возвращает СЛОВАРЬ С ОБНОВЛЕНИЯМИ.
# LangGraph сам аккуратно "вливает" эти обновления в общее состояние.
# ---------------------------------------------------------------------------
class State(TypedDict):
    topic: str          # тема, с которой мы начинаем
    joke: str            # сюда положим шутку
    improved_joke: str   # сюда -- улучшенную версию
    is_funny: bool        # признак "прошло ли качество проверку"


# ---------------------------------------------------------------------------
# Шаг 2. Узлы -- обычные функции. Никакой магии: вход -- state, выход --
# частичное обновление state.
# ---------------------------------------------------------------------------
def generate_joke(state: State) -> dict:
    print(f"[generate_joke] придумываю шутку про: {state['topic']}")
    # В реальном примере здесь был бы вызов LLM: llm.invoke(...)
    joke = f"Почему {state['topic']} перешёл дорогу? Чтобы попасть в LangGraph!"
    return {"joke": joke}


def check_quality(state: State) -> dict:
    print(f"[check_quality] оцениваю шутку: {state['joke']!r}")
    # Условная "проверка качества". В реальности -- отдельный вызов LLM
    # с промптом-судьёй (LLM-as-judge) или простая эвристика.
    is_funny = "LangGraph" in state["joke"]
    return {"is_funny": is_funny}


def improve_joke(state: State) -> dict:
    print("[improve_joke] шутка не очень смешная, улучшаю...")
    improved = state["joke"] + " (а если серьёзно -- граф действительно помогает!)"
    return {"improved_joke": improved}


def finalize(state: State) -> dict:
    final_text = state.get("improved_joke") or state["joke"]
    print(f"[finalize] итоговая шутка: {final_text}")
    return {}


# ---------------------------------------------------------------------------
# Шаг 3. Условная маршрутизация (conditional edge).
#
# Функция-роутер смотрит на state и возвращает ИМЯ следующего узла.
# Это и есть механизм ветвления графа -- ключевая вещь для агентов:
# именно так работает переход "модель решила вызвать инструмент -> идём
# в узел с инструментами" или "модель решила закончить -> идём в END".
# ---------------------------------------------------------------------------
def route_after_check(state: State) -> str:
    if state["is_funny"]:
        return "finalize"
    return "improve_joke"


def build_graph():
    from langgraph.graph import StateGraph, START, END

    builder = StateGraph(State)

    # add_node(имя_узла, функция)
    builder.add_node("generate_joke", generate_joke)
    builder.add_node("check_quality", check_quality)
    builder.add_node("improve_joke", improve_joke)
    builder.add_node("finalize", finalize)

    # START и END -- специальные псевдо-узлы: вход и выход графа.
    builder.add_edge(START, "generate_joke")
    builder.add_edge("generate_joke", "check_quality")

    # add_conditional_edges(откуда, роутер, [необязательная карта имя->узел])
    builder.add_conditional_edges(
        "check_quality",
        route_after_check,
        {"finalize": "finalize", "improve_joke": "improve_joke"},
    )
    builder.add_edge("improve_joke", "finalize")
    builder.add_edge("finalize", END)

    # compile() превращает описание графа в исполняемый объект (Runnable),
    # у которого есть invoke / stream / ainvoke, как и у любого Runnable
    # в LangChain.
    return builder.compile()


def main():
    graph = build_graph()

    # Полезно на этапе обучения: текстовое представление структуры графа.
    # (нужен пакет grandalf: pip install grandalf -- если его нет, просто
    # пропускаем картинку и идём дальше)
    print("=== Структура графа (ASCII) ===")
    try:
        print(graph.get_graph().draw_ascii())
    except ImportError:
        print("(пропущено: для картинки нужен пакет 'grandalf' -- "
              "pip install grandalf)")
    print()

    print("=== Прогон 1 ===")
    result = graph.invoke({"topic": "питон"})
    print("Финальное состояние:", result)

    print("\n=== Прогон 2 (stream -- видно каждый шаг) ===")
    for step in graph.stream({"topic": "рекурсия"}):
        print("шаг графа ->", step)


if __name__ == "__main__":
    main()
