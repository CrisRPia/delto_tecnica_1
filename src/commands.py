from collections.abc import Coroutine
from typing import Any, Callable, TypedDict

from telegram import BotCommand, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

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
        'callback': default_response,
        'command': 'start',
        'description': 'Bienvenida',
    },
    {
        'callback': count_response.count_response,
        'command': 'count',
        'description': '¡Contar de 1 en 1, hasta 999!',
    },
    {
        'callback': weather_request_response,
        'command': 'weather',
        'description': 'Obtén información del tiempo en tu ubicación.',
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
