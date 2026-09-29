"""
Общая точка создания LLM для всех примеров лекции.

Зачем отдельный модуль? Чтобы в каждом файле-примере не дублировать
настройку модели и чтобы было легко переключиться на другую модель
или другого провайдера в одном месте.

===========================================================================
OPENROUTER
===========================================================================
Все примеры ходят к LLM через OpenRouter (https://openrouter.ai/) --
это единый OpenAI-совместимый API, за которым скрываются десятки
провайдеров и моделей (Anthropic, OpenAI, Google, Meta, DeepSeek и т.д.).
Практический плюс для учебных целей: один ключ, один эндпоинт, а модель,
которую использует агент, выбирается СТРОКОЙ в .env -- не нужно менять
код или зависимости, чтобы попробовать другую модель или другого
провайдера.

Технически мы просто используем langchain_openai.ChatOpenAI, но с
base_url, указывающим на OpenRouter, и именем модели в формате
"провайдер/модель" (это формат именования моделей OpenRouter).

===========================================================================
НАСТРОЙКА ЧЕРЕЗ .env
===========================================================================
1. Скопируйте .env.example в .env (в корне папки лекции) и впишите свой
   ключ OpenRouter (https://openrouter.ai/keys):
       OPENROUTER_API_KEY=sk-or-v1-...
2. При желании укажите там же модель:
       OPENROUTER_MODEL=anthropic/claude-sonnet-4.5
   Полный список моделей и их актуальные id: https://openrouter.ai/models
   Если переменную не задать -- используется DEFAULT_MODEL из этого файла.
3. .env подхватывается автоматически (через python-dotenv) при первом
   вызове get_llm() -- отдельно ничего запускать не нужно.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain_openai import ChatOpenAI

try:
    from dotenv import load_dotenv

    # .env лежит в корне папки лекции, то есть на уровень выше common/.
    _ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
    # override=False -- если переменная уже задана в окружении (например,
    # в CI или явным export), .env её не перезатирает.
    load_dotenv(dotenv_path=_ENV_PATH, override=False)
except ImportError:
    # python-dotenv не обязателен: можно обойтись обычными переменными
    # окружения (export / $env:...), просто тогда .env не подхватится сам.
    pass

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Используется, если в .env не указан OPENROUTER_MODEL. Формат имени --
# "провайдер/модель", как на https://openrouter.ai/models
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"


def get_llm(model: str | None = None, temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """Создаёт объект чат-модели LangChain поверх OpenRouter.

    Параметры
    ---------
    model: имя модели в формате "провайдер/модель" (например,
        "openai/gpt-4o" или "meta-llama/llama-3.3-70b-instruct").
        Если не передано -- берётся из переменной окружения
        OPENROUTER_MODEL, а если и её нет -- из DEFAULT_MODEL.
    temperature: температура генерации. Для агентов, которые вызывают
        инструменты, обычно ставят 0 -- нам важна предсказуемость, а не
        креативность.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Не найден OPENROUTER_API_KEY. Скопируйте .env.example в .env "
            "(в корне папки лекции) и впишите туда свой ключ с "
            "https://openrouter.ai/keys, либо задайте переменную окружения "
            "вручную, например:\n"
            "  export OPENROUTER_API_KEY=sk-or-v1-...   (Linux/macOS)\n"
            "  $env:OPENROUTER_API_KEY='sk-or-v1-...'    (PowerShell)"
        )

    resolved_model = model or os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)

    return ChatOpenAI(
        model=resolved_model,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        temperature=temperature,
        # Необязательные заголовки, которые OpenRouter рекомендует
        # присылать: они используются только для атрибуции приложения в
        # статистике OpenRouter и ни на что в самой лекции не влияют.
        default_headers={
            "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", "https://localhost"),
            "X-Title": os.environ.get("OPENROUTER_APP_NAME", "LangGraph Lecture"),
        },
        **kwargs,
    )
