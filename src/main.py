import os
from typing import Any
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder
from commands import BOT_COMMANDS, HANDLERS
from db.helpers import reinit_if_no_db
from errors import error_handler

TELEGRAM_KEY_PATH = 'TELEGRAM_API_KEY'
TELEGRAM_TOKEN = os.environ[TELEGRAM_KEY_PATH]

type _ = Any  # pyright: ignore [reportExplicitAny]


async def on_bot_start(app: Application[Bot, _, _, _, _, _]):
    print('Bot iniciado.')
    await reinit_if_no_db()
    print('Base de datos funcional.')
    _ = await app.bot.delete_my_commands()
    _ = await app.bot.set_my_commands(BOT_COMMANDS)
    print(
        'Inicialización terminada. Para obtener autocompletado de comandos, reinicie su aplicación de Telegram.'
    )
    print('(Ctrl+C, o el equivalente de su SO para desactivar bot.)')


def dev():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .post_init(on_bot_start)  # pyright: ignore [reportUnknownMemberType]
        .build()
    )

    for handler in HANDLERS:
        app.add_handler(handler)
    app.add_error_handler(error_handler, block=True) # pyright: ignore [reportUnknownArgumentType]
    print('Iniciando bot...')
    app.run_polling()


if __name__ == '__main__':
    dev()
