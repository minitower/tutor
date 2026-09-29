"""
Урок 8. Динамическое создание агентов: "агент как инструмент" и мета-агент

===========================================================================
ЧЕМ ЭТО ОТЛИЧАЕТСЯ ОТ УРОКОВ 5-6
===========================================================================
В supervisor (урок 5) и handoff (урок 6) набор агентов ФИКСИРОВАН на этапе
написания кода: мы заранее создали researcher, coder и явно прописали, как
они связаны в графе. Модель выбирает МЕЖДУ существующими агентами, но не
может завести нового.

В этом уроке агент сам, во время выполнения, решает создать НОВОГО,
специально заточенного под задачу под-агента -- через обычный вызов
инструмента. Схема с точки зрения графа предельно проста:

    START -> [оркестратор: create_agent] -> tools -> [оркестратор] -> ...

...но один из инструментов оркестратора, create_specialist_agent, ВНУТРИ
СЕБЯ вызывает create_agent(...) и .invoke(...) -- то есть строит и
запускает целый ReAct-агент как часть выполнения одного шага. Никакого
нового узла StateGraph для этого не требуется: с точки зрения графа это
просто "ещё один инструмент", просто он оказывается очень мощным.

Это и называют паттерном "agent-as-a-tool" или, в более общем виде,
"мета-агентом" / "фабрикой агентов": LLM выбирает не только ЧТО сделать,
но и КАКОЙ агент для этого нужен -- его роль (системный промпт) и набор
инструментов.

===========================================================================
ПОЧЕМУ ЭТО ОПАСНО БЕЗ ОГРАНИЧЕНИЙ (и что с этим делать)
===========================================================================
Если ничего не ограничивать, у вас есть риск получить:
    1. Рекурсивный "форк-бомб" агентов -- созданный агент тоже получает
       доступ к create_specialist_agent и создаёт следующего, тот -- ещё
       одного, и так далее.
    2. Неконтролируемый расход токенов/денег -- каждый созданный агент
       может сам сделать несколько обращений к LLM.
    3. Повышение привилегий -- если разрешить модели давать новым агентам
       ЛЮБЫЕ инструменты (в том числе критичные вроде send_money из урока 7),
       модель может обойти ограничения, которые вы наложили на оркестратора,
       просто "делегировав" опасное действие новому агенту.

Поэтому в этом уроке добавлены три конкретных предохранителя:
    - MAX_DEPTH -- максимальная глубина вложенности (агент создал агента,
      который создал агента -- и не более того).
    - Budget.remaining -- общий лимит на число созданных агентов за один
      запуск оркестратора.
    - TOOL_REGISTRY (белый список) -- новому агенту можно выдать только
      инструменты из заранее одобренного набора, а не произвольные строки.

Нужен OPENROUTER_API_KEY (см. .env.example в корне папки лекции).
Запуск:
    python 08_dynamic_agent_factory.py
"""

import contextvars
from dataclasses import dataclass
from typing import List

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from common.console import ensure_utf8_console
from common.llm import get_llm

ensure_utf8_console()

MAX_DEPTH = 2
MAX_TOTAL_SPECIALISTS = 4

# contextvars.ContextVar, а не обычная переменная, потому что глубина
# должна корректно отслеживаться даже при вложенных вызовах (специалист
# создаёт специалиста) в рамках одного и того же вызова Python-функций.
_current_depth = contextvars.ContextVar("agent_factory_depth", default=0)


@dataclass
class SpawnBudget:
    """Общий 'кошелёк' на число агентов, которые можно создать за один запуск."""

    remaining: int = MAX_TOTAL_SPECIALISTS


# ---------------------------------------------------------------------------
# Белый список инструментов, которые разрешено выдавать создаваемым
# агентам. Это обычные @tool из предыдущих уроков -- ничего нового.
# ---------------------------------------------------------------------------
@tool
def web_search(query: str) -> str:
    """Ищет информацию в интернете по запросу."""
    return (
        f"По запросу '{query}': LangGraph -- библиотека для построения "
        "графов агентов поверх LangChain."
    )


@tool
def calculator(expression: str) -> str:
    """Вычисляет простое арифметическое выражение."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Ошибка: выражение содержит недопустимые символы"
    try:
        return str(eval(expression))
    except Exception as exc:  # noqa: BLE001 -- учебный пример
        return f"Ошибка вычисления: {exc}"


@tool
def write_code(task: str) -> str:
    """Пишет короткий фрагмент python-кода для решения задачи (заглушка)."""
    return f"# решение для: {task}\ndef solution():\n    pass"


TOOL_REGISTRY = {
    "web_search": web_search,
    "calculator": calculator,
    "write_code": write_code,
}


def make_create_specialist_agent_tool(llm, tool_registry: dict, budget: SpawnBudget):
    """Фабрика инструмента 'создать специализированного агента'.

    Возвращает @tool, который принимает от LLM три параметра:
        role_description -- системный промпт нового агента (кто он);
        task              -- конкретная задача, которую он должен решить;
        tool_names        -- список имён инструментов ИЗ TOOL_REGISTRY.

    Внутри тела инструмента мы сами, руками, вызываем create_agent(...) --
    то есть новый агент существует ровно столько, сколько выполняется этот
    один вызов инструмента, и не более того.
    """
    available = ", ".join(sorted(tool_registry))
    description = (
        "Создаёт нового специализированного агента и сразу поручает ему "
        "задачу, возвращая его финальный ответ. Используй, когда для части "
        "запроса пользователя нужен агент с особой ролью и/или своим "
        f"набором инструментов. tool_names -- список имён из: {available}."
    )

    @tool(description=description)
    def create_specialist_agent(
        role_description: str, task: str, tool_names: List[str]
    ) -> str:
        # --- Предохранитель 1: общий бюджет на число созданных агентов ---
        if budget.remaining <= 0:
            return (
                "Отказано: достигнут лимит на количество агентов, "
                "которые можно создать в рамках одного запроса."
            )

        # --- Предохранитель 2: глубина вложенности ---
        depth = _current_depth.get()
        if depth >= MAX_DEPTH:
            return (
                "Отказано: превышена допустимая глубина вложенности "
                "агентов (агент не может создавать агентов бесконечно)."
            )

        # --- Предохранитель 3: белый список инструментов ---
        selected_tools = []
        unknown_names = []
        for name in tool_names:
            if name in tool_registry:
                selected_tools.append(tool_registry[name])
            else:
                unknown_names.append(name)
        if unknown_names:
            return (
                f"Отказано: неизвестные инструменты {unknown_names}. "
                f"Доступны только: {available}."
            )

        budget.remaining -= 1
        print(
            f"[фабрика] создаю агента (глубина {depth + 1}, "
            f"осталось бюджета {budget.remaining}): {role_description!r}"
        )

        specialist = create_agent(
            model=llm,
            tools=selected_tools,
            system_prompt=role_description,
        )

        # Увеличиваем глубину ТОЛЬКО на время работы этого специалиста --
        # если он сам вызовет create_specialist_agent, тот увидит depth+1.
        token = _current_depth.set(depth + 1)
        try:
            result = specialist.invoke(
                {"messages": [HumanMessage(task)]},
                # У каждого специалиста свой небольшой лимит шагов -- он не
                # может зависнуть в цикле дольше, чем оркестратор.
                config={"recursion_limit": 8},
            )
        finally:
            _current_depth.reset(token)

        return result["messages"][-1].content

    return create_specialist_agent


def build_orchestrator():
    llm = get_llm()
    budget = SpawnBudget()
    create_specialist_agent_tool = make_create_specialist_agent_tool(
        llm, TOOL_REGISTRY, budget
    )

    # Обратите внимание: у самого оркестратора НЕТ инструментов для поиска,
    # вычислений и т.д. -- только один инструмент, которым он делегирует
    # всю реальную работу специалистам. Это намеренное архитектурное
    # решение: оркестратор занимается только планированием и сборкой ответа.
    orchestrator = create_agent(
        model=llm,
        tools=[create_specialist_agent_tool],
        system_prompt=(
            "Ты -- оркестратор. У тебя нет инструментов для прямого решения "
            "задачи. Для каждой самостоятельной части запроса пользователя "
            "вызови create_specialist_agent, указав:\n"
            "  - role_description: чёткая роль нового агента;\n"
            "  - task: конкретная под-задача для него;\n"
            "  - tool_names: только нужные инструменты из списка "
            f"{', '.join(sorted(TOOL_REGISTRY))}.\n"
            "Затем собери финальный ответ пользователю из результатов "
            "работы специалистов."
        ),
    )
    return orchestrator, budget


def main():
    orchestrator, budget = build_orchestrator()

    question = (
        "Найди, что такое LangGraph, посчитай 15 * 24, и напиши функцию "
        "на python, которая проверяет число на простоту."
    )
    print(f"=== Вопрос: {question} ===\n")
    result = orchestrator.invoke(
        {"messages": [HumanMessage(question)]},
        config={"recursion_limit": 20},
    )

    print("\n=== Полная история диалога ===")
    for msg in result["messages"]:
        msg.pretty_print()

    print(f"\n(создано специализированных агентов: "
          f"{MAX_TOTAL_SPECIALISTS - budget.remaining} из {MAX_TOTAL_SPECIALISTS})")


if __name__ == "__main__":
    main()
