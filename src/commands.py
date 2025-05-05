"""
Collection of constants regarding command handlers.
"""

from collections.abc import Coroutine
from typing import Any, Callable, TypedDict

from telegram import BotCommand, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from handlers.ai import ai_handler
from handlers.count import count_handler
from handlers.location import location_handler
from handlers.start import start_handler
from handlers.weather import weather_handler


class CommandOptions(TypedDict):
    command: str
    description: str
    callback: Callable[
        [Update, ContextTypes.DEFAULT_TYPE],
        Coroutine[Any, Any, None],  # pyright: ignore [reportExplicitAny]
    ]


SLASH_COMMANDS: list[CommandOptions] = [
    {
        "command": "ai",
        "description": "🤖 Obtén un mensaje de IA basado en la información de este chat.",
        "callback": ai_handler,
    },
    {
        'callback': start_handler,
        'command': 'start',
        'description': '👋 Bienvenida',
    },
    {
        'callback': count_handler,
        'command': 'count',
        'description': '#️⃣¡ Contar de 1 en 1, hasta 999!',
    },
    {
        'callback': weather_handler,
        'command': 'weather',
        'description': '🌤️ Obtén información del tiempo en una ubicación.',
    },
]

BOT_COMMANDS: list[BotCommand] = [
    BotCommand(sc['command'], sc['description']) for sc in SLASH_COMMANDS
]

HANDLERS = [
    CommandHandler(sc['command'], sc['callback']) for sc in SLASH_COMMANDS
] + [
    MessageHandler(filters.LOCATION, location_handler),
]
