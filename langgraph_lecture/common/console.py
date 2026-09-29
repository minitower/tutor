"""
Небольшая утилита для корректного вывода кириллицы в консоли Windows.

Проблема: стандартная консоль Windows (cmd.exe / старый PowerShell) часто
использует кодировку CP1251 или CP866, а не UTF-8, поэтому print() с
русским текстом может превращаться в "кракозябры". Вызов
ensure_utf8_console() в начале скрипта решает это программно, без
необходимости менять настройки системы.
"""

import sys


def ensure_utf8_console() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            # На некоторых окружениях reconfigure недоступен -- не критично,
            # просто продолжаем как есть.
            pass
