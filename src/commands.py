from collections.abc import Coroutine
from typing import Any, Callable, TypedDict

from telegram import BotCommand, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from ai_response import ai_response
import count_response
from default_response import default_response
import location_response
from weather_response import weather_request_response


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
        "callback": ai_response,
    },
    {
        'callback': default_response,
        'command': 'start',
        'description': '👋 Bienvenida',
    },
    {
        'callback': count_response.count_response,
        'command': 'count',
        'description': '#️⃣¡ Contar de 1 en 1, hasta 999!',
    },
    {
        'callback': weather_request_response,
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
    MessageHandler(filters.LOCATION, location_response.location_response),
]
